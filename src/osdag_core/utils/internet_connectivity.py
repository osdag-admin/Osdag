from PySide6.QtCore import QObject, QTimer, Signal, QEventLoop, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class InternetConnectivity(QObject):
    online_status_changed = Signal(bool)  

    def __init__(self, check_interval_ms=5000, parent=None):
        super().__init__(parent)
        self._manager = QNetworkAccessManager(self)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._check_once)
        self._is_online = None 
        self._check_interval = check_interval_ms

    def start_monitoring(self):
        """
        Start periodic monitoring. Always know the current connectivity without manually checking.
        Feasible for Osdag Web Application.

        Check every `self._check_interval` milliseconds.

        """
        self._timer.start(self._check_interval)
        self._check_once() 

    def stop_monitoring(self):
        """Stop periodic monitoring."""
        self._timer.stop()

    def is_online(self, timeout_ms=5000) -> bool:
        """
        Synchronous one-time check. Returns True if internet is available.

        Notify when the online status changes (from offline → online or online → offline).
        Connect this to any slot/function to react to connectivity changes.

        returns
        ---

        bool:
            `True` if internet is available, `False` otherwise.
        """
        loop = QEventLoop()
        reply = self._manager.get(QNetworkRequest(QUrl("http://www.google.com")))
        reply.finished.connect(loop.quit)

        # Quit the loop after timeout
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)
        timer.start(timeout_ms)

        loop.exec() 

        success = reply.error() == QNetworkReply.NoError if reply.isFinished() else False

        reply.deleteLater()
        timer.deleteLater()
        return success


    def _check_once(self):
        """Internal async check (used by timer - Internal usage)."""
        reply = self._manager.get(QNetworkRequest(QUrl("http://www.google.com")))
        reply.finished.connect(lambda: self._handle_reply(reply))

    def _handle_reply(self, reply):
        """Handle the network reply and emit signal if status changed (Internal usage)."""
        success = reply.error() == QNetworkReply.NoError
        if success != self._is_online:
            self._is_online = success
            self.online_status_changed.emit(success)
        reply.deleteLater()

