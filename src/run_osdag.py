#!/usr/bin/env python3
"""Cross-platform launcher for Osdag GUI."""

import os
import sys
import platform


def _has_hardware_gl_support():
    """Check if hardware OpenGL is available on Linux."""
    try:
        import subprocess
        result = subprocess.run(
            ["glxinfo", "-B"],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout.lower()
        
        if "accelerated: yes" in output:
            return True
        if "llvmpipe" in output or "softpipe" in output or "swrast" in output:
            return False
        if "intel" in output or "nvidia" in output or "amd" in output or "radeon" in output:
            return True
        if "direct rendering: yes" in output:
            return True
            
        return True
    except FileNotFoundError:
        return True
    except Exception:
        return True


def setup_environment():
    """Configure environment variables for optimal Qt/OpenGL performance."""
    
    system = platform.system()
    
    if system == "Linux":
        if "DISPLAY" in os.environ:
            os.environ.setdefault("QT_QPA_PLATFORM", "xcb")
        
        os.environ.setdefault("QT_OPENGL", "desktop")
        os.environ.setdefault("QT_QPA_NO_THREADED_GL", "1")
        os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")
        os.environ.setdefault("QT_SCALE_FACTOR", "1")
        
        has_hardware_gpu = _has_hardware_gl_support()
        
        if has_hardware_gpu:
            print("[INFO] Hardware GPU detected - using hardware acceleration")
        else:
            print("[INFO] Hardware OpenGL not detected, using software rendering")
            os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
            os.environ.setdefault("MESA_GL_VERSION_OVERRIDE", "3.3")
            os.environ.setdefault("LIBGL_DRI3_DISABLE", "1")
        
        print("[INFO] Linux environment configured: Using X11 backend")
        
    elif system == "Darwin":
        os.environ.setdefault("QT_MAC_WANTS_LAYER", "1")
        os.environ.setdefault("QT_OPENGL", "desktop")
        print("[INFO] macOS environment configured")
        
    elif system == "Windows":
        os.environ.setdefault("QT_OPENGL", "desktop")
        print("[INFO] Windows environment configured")
    
    os.environ.setdefault("PYTHONOCC_DISPLAY_BACKEND", "pyside6")


def main():
    """Launch Osdag GUI."""
    setup_environment()
    
    try:
        from osdag_gui.__main__ import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"[ERROR] Could not import osdag_gui: {e}")
        print("[INFO] Make sure you're in the correct directory and environment is activated")
        sys.exit(1)


if __name__ == "__main__":
    main()
