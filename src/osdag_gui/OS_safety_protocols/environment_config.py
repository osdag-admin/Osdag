#!/usr/bin/env python3
"""
Cross-Platform Environment Configuration for Osdag

This module configures environment variables for optimal Qt/OpenGL performance
across Linux, macOS, and Windows platforms.

Features:
- Hardware GPU detection on Linux
- Qt platform backend configuration
- Software rendering fallback for VM/headless environments
- OpenCASCADE display backend settings

Author: Nishi Kant Mandal
"""

import os, sys
import platform

def _has_hardware_gl_support() -> bool:
    """
    Check if hardware OpenGL acceleration is available on Linux.
    
    Uses glxinfo to detect GPU capabilities. Falls back to True if detection
    fails (assumes hardware is available).
    
    Returns:
        True if hardware acceleration is available, False for software rendering
    """
    try:
        import subprocess
        result = subprocess.run(
            ["glxinfo", "-B"],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout.lower()
        
        # Check for hardware acceleration indicators
        if "accelerated: yes" in output:
            return True
        
        # Check for software renderer indicators
        if "llvmpipe" in output or "softpipe" in output or "swrast" in output:
            return False
        
        # Check for known GPU vendors
        if "intel" in output or "nvidia" in output or "amd" in output or "radeon" in output:
            return True
        
        # Check direct rendering support
        if "direct rendering: yes" in output:
            return True
            
        return True  # Default to hardware
        
    except FileNotFoundError:
        # glxinfo not installed - assume hardware is available
        return True
    except Exception:
        return True


def setup_environment() -> None:
    """
    Configure environment variables for optimal Qt/OpenGL performance.
    
    This function MUST be called before importing PySide6/Qt modules
    for the environment variables to take effect.
    
    Platform-specific configurations:
        Linux: X11 backend, hardware GPU detection, software fallback
        macOS: Metal layer support, desktop OpenGL
        Windows: Desktop OpenGL
    """
    # Setup Qt Environment
    # Use PySide6's own plugins directory, not conda's Qt6
    # This ensures compatibility between the pip-installed PySide6 and Qt runtime
    try:
        # Try to find PySide6 package location
        import importlib.resources
        from pathlib import Path
        
        # PySide6 package is in site-packages
        pyside6_plugins = None
        
        # First, check if we can import PySide6 to find its location
        import PySide6
        pyside6_path = Path(PySide6.__file__).parent
        candidate_plugins = pyside6_path / "plugins"
        
        if candidate_plugins.exists():
            pyside6_plugins = str(candidate_plugins)
        else:
            # Fallback: try common installation paths
            for potential_path in [
                Path(sys.prefix) / "lib" / "site-packages" / "PySide6" / "plugins",
                Path(sys.prefix) / "Lib" / "site-packages" / "PySide6" / "plugins",
            ]:
                if potential_path.exists():
                    pyside6_plugins = str(potential_path)
                    break
        
        if pyside6_plugins:
            os.environ["QT_PLUGIN_PATH"] = pyside6_plugins
            os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
                pyside6_plugins, "platforms"
            )
        else:
            # Ultimate fallback: use conda's Qt6 plugins
            qt_plugins = os.path.abspath(
                os.path.join(sys.executable, "..", "Library", "lib", "qt6", "plugins" )
            )
            os.environ["QT_PLUGIN_PATH"] = qt_plugins
            os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
                qt_plugins, "platforms"
            )
    except Exception as e:
        # If anything goes wrong, fall back to conda Qt6 path
        qt_plugins = os.path.abspath(
            os.path.join(sys.executable, "..", "Library", "lib", "qt6", "plugins" )
        )
        os.environ["QT_PLUGIN_PATH"] = qt_plugins
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
            qt_plugins, "platforms"
        )

    system = platform.system()
    
    if system == "Linux":
        _setup_linux_environment()
    elif system == "Darwin":
        _setup_macos_environment()
    elif system == "Windows":
        _setup_windows_environment()
    
    # Common settings for all platforms
    os.environ.setdefault("PYTHONOCC_DISPLAY_BACKEND", "pyside6")

def _setup_linux_environment() -> None:
    """Configure environment for Linux systems."""
    # Use X11/xcb for display
    if "DISPLAY" in os.environ:
        os.environ.setdefault("QT_QPA_PLATFORM", "xcb")
    
    # Qt OpenGL settings
    os.environ.setdefault("QT_OPENGL", "desktop")
    os.environ.setdefault("QT_QPA_NO_THREADED_GL", "1")
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")
    os.environ.setdefault("QT_SCALE_FACTOR", "1")
    
    # Detect hardware GPU support
    has_hardware_gpu = _has_hardware_gl_support()
    
    if has_hardware_gpu:
        print("[Osdag] Hardware GPU detected - using hardware acceleration")
    else:
        print("[Osdag] Hardware OpenGL not detected, using software rendering")
        os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
        os.environ.setdefault("MESA_GL_VERSION_OVERRIDE", "3.3")
        os.environ.setdefault("LIBGL_DRI3_DISABLE", "1")
    
    print("[Osdag] Linux environment configured: Using X11 backend")


def _setup_macos_environment() -> None:
    """Configure environment for macOS systems."""
    os.environ.setdefault("QT_MAC_WANTS_LAYER", "1")
    os.environ.setdefault("QT_OPENGL", "desktop")
    print("[Osdag] macOS environment configured")


def _setup_windows_environment() -> None:
    """Configure environment for Windows systems."""
    os.environ.setdefault("QT_OPENGL", "desktop")
    print("[Osdag] Windows environment configured")
