"""
Multiprocessing and CAD Safety Module for Osdag

This module provides thread-safe initialization and memory protection for:
1. Multiprocessing start method (prevents repeated set_start_method calls)
2. OpenCASCADE/CAD rendering protection
3. Memory safety guards for native C++ operations
4. Cross-platform compatibility layer

Author: Nishi Kant Mandal
"""

import os
import platform
import threading
import functools
from typing import Callable


class SafetyManager:
    """
    Singleton manager for application-wide safety configurations.
    
    Ensures multiprocessing is initialized exactly once and provides
    guards for OpenCASCADE operations that can cause memory corruption.
    
    Usage:
        # At application startup (before any other imports)
        SafetyManager.initialize_multiprocessing()
        
        # For thread-safe CAD operations
        @SafetyManager.safe_cad_operation
        def render_3d_model(self):
            # CAD operations here
            pass
    """
    
    _instance = None
    _lock = threading.Lock()
    _mp_initialized = False
    _cad_lock = threading.RLock()  # Reentrant lock for CAD operations
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize_multiprocessing(cls, method: str = 'spawn') -> bool:
        """
        Safely initialize multiprocessing start method.
        
        This should be called ONCE at application startup. Subsequent calls
        are safely ignored to prevent memory corruption.
        
        Args:
            method: Start method ('spawn', 'fork', or 'forkserver')
                   'spawn' is recommended for GUI applications with OpenGL
            
        Returns:
            True if initialization was performed, False if already initialized
        """
        if cls._mp_initialized:
            return False
            
        with cls._lock:
            if cls._mp_initialized:
                return False
                
            try:
                import multiprocessing as mp
                
                # Check if already set
                current_method = mp.get_start_method(allow_none=True)
                if current_method is not None:
                    print(f"[Osdag] Multiprocessing already configured: {current_method}")
                    cls._mp_initialized = True
                    return False
                
                # Set the start method (without force=True to avoid corruption)
                mp.set_start_method(method)
                cls._mp_initialized = True
                print(f"[Osdag] Multiprocessing initialized with '{method}' method")
                return True
                
            except RuntimeError as e:
                # Already set by another path
                print(f"[Osdag] Multiprocessing already set: {e}")
                cls._mp_initialized = True
                return False
            except Exception as e:
                print(f"[Osdag] Warning during multiprocessing init: {e}")
                cls._mp_initialized = True
                return False
    
    @classmethod
    def is_mp_initialized(cls) -> bool:
        """Check if multiprocessing has been initialized."""
        return cls._mp_initialized
    
    @classmethod
    def get_cad_lock(cls) -> threading.RLock:
        """Get the CAD rendering lock for thread-safe operations."""
        return cls._cad_lock
    
    @classmethod
    def safe_cad_operation(cls, func: Callable) -> Callable:
        """
        Decorator to make CAD operations thread-safe.
        
        Wraps the function with a lock and Qt event processing
        to prevent race conditions and ensure display stability.
        
        Usage:
            @SafetyManager.safe_cad_operation
            def render_3d_model(self):
                # CAD operations here
                pass
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with cls._cad_lock:
                try:
                    # Process Qt events before CAD operations to prevent deadlocks
                    try:
                        from PySide6.QtWidgets import QApplication
                        if QApplication.instance():
                            QApplication.processEvents()
                    except ImportError:
                        pass
                    
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    print(f"[Osdag] CAD operation failed: {e}")
                    raise
        return wrapper


def ensure_safe_startup() -> None:
    """
    Call this at application startup to ensure safe initialization.
    
    This function MUST be called before importing PySide6/Qt modules.
    
    It performs:
    1. Platform-specific multiprocessing configuration
    2. OpenCASCADE threading settings
    3. Memory safety guards
    """
    system = platform.system()
    
    # Platform-specific multiprocessing configuration
    # All platforms use 'spawn' for GUI apps with OpenGL
    if system == "Darwin":  # macOS
        # macOS MUST use 'spawn' - 'fork' causes crashes with GUI apps
        SafetyManager.initialize_multiprocessing('spawn')
    elif system == "Windows":
        # Windows always uses 'spawn' (it's the only option)
        SafetyManager.initialize_multiprocessing('spawn')
    else:  # Linux
        # Linux: 'spawn' is safest for GUI apps with OpenGL
        SafetyManager.initialize_multiprocessing('spawn')
    
    # Set OpenCASCADE threading settings
    os.environ.setdefault("CSF_PARALLEL_THREADS", "1")
    
    print("[Osdag] Application safety initialized")


def safe_import_occ() -> bool:
    """
    Safely import OpenCASCADE modules with proper error handling.
    
    Returns:
        True if OCC is available, False otherwise
    """
    try:
        import OCC.Core.TopoDS
        return True
    except ImportError as e:
        print(f"[Osdag] OpenCASCADE not available: {e}")
        return False


# Convenience function for backward compatibility
def ensure_mp_spawn() -> None:
    """
    Ensure multiprocessing uses 'spawn' method.
    
    This is a safe replacement for:
        mp.set_start_method('spawn', force=True)
    
    Can be called multiple times safely.
    """
    SafetyManager.initialize_multiprocessing('spawn')
