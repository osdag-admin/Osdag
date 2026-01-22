import os
import sys
import time
import faulthandler
import threading
import traceback
import signal
import collections
import threading


class CrashLogger:
    """
    OSDAG CRASH LOG FORMAT — HOW TO READ IT
    =====================================

    Each crash file is a time-resolved "black box" of the application.
    It records WHAT Osdag was doing, WHY the log was written, and
    WHAT actually failed.

    The file is divided into four conceptual layers:

    -------------------------------------------------
    1) HEADER
    -------------------------------------------------
    Example:
        == O S D A G   C R A S H ==
        Reason: PYTHON EXCEPTION

    This tells you *what triggered the dump/log*.

    Possible values:
        PYTHON EXCEPTION     → Unhandled Python error
        FREEZE DETECTED     → GUI stopped responding
        NATIVE CRASH SIGNAL → Segfault / abort from C/C++ (Qt, OCC, etc.)

    This answers: "Did the app crash, freeze, or throw an exception?"


    -------------------------------------------------
    2) LAST EXECUTION (Timeline)
    -------------------------------------------------
    Example:
        [15:30:53] flexure_purlin.py:design_beam:1144
        [15:30:56] template_page.py:finished_loading:1514
        [15:31:04] output_dock.py:open_summary_popup:352

    These are NOT a stack trace.
    They are a *time-series* sampled from the main thread.

    Each line shows:
        [timestamp] file : function : line

    Read it top → bottom as:
        "What the program was doing over time just before the crash"

    This lets you reconstruct:
        • user actions
        • UI transitions
        • CAD rendering
        • background design calculations

    This answers: "What sequence of events led to the failure?"


    -------------------------------------------------
    3) PYTHON EXCEPTION
    -------------------------------------------------
    Example:
        AttributeError: 'Flexure_Purlin' object has no attribute 'report_column'

    This is the *logical failure* that killed the program.

    It is a normal Python traceback giving:
        • exact file
        • exact function
        • exact line
        • full call stack

    This answers: "What bug was triggered?"


    -------------------------------------------------
    4) NATIVE STACK
    -------------------------------------------------
    This shows what *every thread* (Qt, OCC, watchdog, sampler, GUI)
    was doing at the moment the crash was recorded.

    Important parts:
        "Current thread" → where Python crashed
        Other threads    → whether CAD, GPU, or background workers were active

    This answers:
        "Was this a UI bug, a threading issue, or a native crash?"


    -------------------------------------------------
    HOW TO DEBUG USING THIS FILE
    -------------------------------------------------

    1) Start with "Reason"
    → Was it a freeze, a Python exception, or a native crash?

    2) Look at "Python exception"
    → This is usually the real bug.

    3) Use "Last execution" to see
    → what the user did just before it happened
    → which module and UI were involved.

    4) Use "Native stack" to confirm
    → whether Qt, OCC, or background threads contributed.

    This turns "Osdag crashed" into:
        "Which user action + which module + which thread + which line failed"
    """

    def __init__(self, verbose=False, buffer_size=400, on_crash=None):
        """
        Initialize crash logger.

        :param verbose: If True, record full stack traces in the past buffer.
                        Default False, only record top frame.
        :param buffer_size: Number of past execution lines to keep in buffer.

        :param on_crash: Optional callback function to call after a crash is dumped.

        """
        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.dir = os.path.join(app_dir, "data", "app_crashes")
        self.buffer = collections.deque(maxlen=buffer_size)
        self.last_heartbeat = time.time()
        self.dumped = False
        self.lock = threading.Lock()
        self.verbose = verbose  
        self.on_crash = on_crash


    def start(self):
        os.makedirs(self.dir, exist_ok=True)

        # Python crash
        faulthandler.enable()
        sys.excepthook = self._on_exception
        self._start_sampler()

        # Watchdog for freezes
        # self._start_watchdog()

        # Native crash signals
        for sig in (signal.SIGABRT, signal.SIGSEGV, signal.SIGFPE, signal.SIGILL):
            signal.signal(sig, self._on_signal)

    # -----------------------
    # Past buffer
    # -----------------------

    def _record(self, msg):
        ts = time.strftime("%H:%M:%S")
        with self.lock:
            self.buffer.append(f"[{ts}] {msg}")

    # -----------------------
    # Python execution tracer
    # -----------------------

    def _start_sampler(self):
        def sampler():
            while True:
                time.sleep(0.2)
                try:
                    frames = sys._current_frames()
                    main = frames.get(threading.main_thread().ident)
                    if main:
                        self._record_stack(main)
                except Exception:
                    pass

        threading.Thread(target=sampler, daemon=True).start()

    def _record_stack(self, frame):
        if self.verbose:
            while frame:
                code = frame.f_code
                self._record(f"{code.co_filename}:{code.co_name}:{frame.f_lineno}")
                frame = frame.f_back
        else:
            code = frame.f_code
            self._record(f"{code.co_filename}:{code.co_name}:{frame.f_lineno}")


    # -----------------------
    # Freeze detection
    # -----------------------

    def _start_watchdog(self):
        def watchdog():
            while True:
                time.sleep(1)
                if time.time() - self.last_heartbeat > 5:
                    self._dump("FREEZE DETECTED")
                    break

        threading.Thread(target=watchdog, daemon=True).start()

        # heartbeat from main thread
        def heartbeat():
            while True:
                self.last_heartbeat = time.time()
                time.sleep(0.5)

        threading.Thread(target=heartbeat, daemon=True).start()

    # -----------------------
    # Crash handlers
    # -----------------------

    def _on_exception(self, exc_type, exc, tb):
        self._dump("PYTHON EXCEPTION", exc_type, exc, tb)

    def _on_signal(self, signum, frame):
        self._dump(f"NATIVE CRASH SIGNAL {signum}")
        os._exit(1)

    # -----------------------
    # Dump to disk
    # -----------------------

    def _dump(self, reason, exc_type=None, exc=None, tb=None):
        if self.dumped:
            return
        self.dumped = True
    
        path = os.path.join(self.dir, time.strftime("Crash-%Y-%m-%d_%H-%M-%S.log"))

        with open(path, "w") as f:
            f.write(f"== O S D A G   C R A S H ==\n")
            f.write(f"Reason: {reason}\n\n")

            f.write("== Last execution ==\n")
            with self.lock:
                snapshot = list(self.buffer)

            for line in snapshot:
                f.write(line + "\n")

            if exc_type:
                f.write("\n== Python exception ==\n")
                traceback.print_exception(exc_type, exc, tb, file=f)

            f.write("\n== Native stack ==\n")
            faulthandler.dump_traceback(file=f, all_threads=True)

            try:
                self.file.flush()
                os.fsync(self.file.fileno())
            except Exception:
                pass

            # Tell the UI something catastrophic happened
            if self.on_crash:
                try:
                    self.on_crash(reason, exc, path)
                except Exception:
                    pass

        

