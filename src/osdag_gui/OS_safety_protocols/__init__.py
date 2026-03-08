"""
OS Safety Protocols Package for Osdag

This package provides cross-platform safety protocols for stable application startup:
- Environment configuration (GPU detection, Qt/OpenGL settings)
- Multiprocessing safety (spawn method initialization)
- OpenCASCADE memory protection and lifecycle management

Author: Nishi Kant Mandal
"""

from .environment_config import setup_environment
from .multiprocessing_safety import SafetyManager, ensure_safe_startup
from .occ_memory_manager import OCCMemoryManager, get_occ_memory_manager

__all__ = [
    'setup_environment',
    'SafetyManager', 
    'ensure_safe_startup',
    'OCCMemoryManager',
    'get_occ_memory_manager',
]
