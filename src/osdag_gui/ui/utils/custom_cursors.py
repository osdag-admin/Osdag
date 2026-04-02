"""
Custom Cursor Utility for Osdag GUI

Provides consistent cursor appearance across platforms by using custom cursor
images when the system cursor theme doesn't work properly with Qt.

This fixes the issue where Qt/xcb on Linux shows a tilted hand cursor instead
of the system's upright pointing hand cursor.
"""

import os
import platform
from functools import lru_cache

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QPixmap, QPainter, QColor


def _create_pointing_hand_pixmap(size: int = 40) -> QPixmap:
    """
    Create a classic pixelated upright pointing hand cursor.
    
    This creates the classic hand cursor with index finger pointing up,
    black fill with white border - matching the Windows/web cursor style.
    
    Args:
        size: Size of the cursor in pixels (default 40)
        
    Returns:
        QPixmap with transparent background and hand cursor drawn
    """
    # Larger 40x40 cursor design (no scaling, native size)
    # 0 = transparent, 1 = white (outline), 2 = black (fill)
    cursor_data = [
        "0000000000001111110000000000000000000000",
        "0000000000001222210000000000000000000000",
        "0000000000001222210000000000000000000000",
        "0000000000001222210000000000000000000000",
        "0000000000001222210000000000000000000000",
        "0000000000001222210000000000000000000000",
        "0000000000001222210000000000000000000000",
        "0000000000001222210000000000000000000000",
        "0000000000001222211111000000000000000000",
        "0000000000001222222221000000000000000000",
        "0000000000001222222221111100000000000000",
        "0000000011111222222222222100000000000000",
        "0000000122221222222222222111100000000000",
        "0000000122222222222222222222100000000000",
        "0000000012222222222222222222100000000000",
        "0000000001222222222222222222100000000000",
        "0000000001222222222222222222100000000000",
        "0000000001222222222222222222100000000000",
        "0000000000122222222222222222100000000000",
        "0000000000122222222222222222100000000000",
        "0000000000012222222222222222100000000000",
        "0000000000012222222222222222100000000000",
        "0000000000001222222222222222100000000000",
        "0000000000001222222222222221000000000000",
        "0000000000000122222222222221000000000000",
        "0000000000000122222222222221000000000000",
        "0000000000000011111111111110000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000",
    ]
    
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing, False)  # Keep pixelated look
    
    # Colors: White outline, Black fill
    outline_color = QColor(255, 255, 255, 255)  # White outline
    fill_color = QColor(0, 0, 0, 255)           # Black fill
    
    for y, row in enumerate(cursor_data):
        for x, pixel in enumerate(row):
            if pixel == '1':  # Outline
                painter.fillRect(x, y, 1, 1, outline_color)
            elif pixel == '2':  # Fill
                painter.fillRect(x, y, 1, 1, fill_color)
    
    painter.end()
    
    return pixmap


@lru_cache(maxsize=4)
def get_pointing_hand_cursor(size: int = 40) -> QCursor:
    """
    Get a custom pointing hand cursor.
    
    On Linux with Qt6, the standard PointingHandCursor often shows incorrectly
    as a tilted hand instead of the system's upright cursor. This function
    provides a custom cursor that always looks correct.
    
    The cursor is cached for performance.
    
    Args:
        size: Cursor size in pixels (default 40)
        
    Returns:
        QCursor with upright pointing hand
    """
    # The hotspot is at the tip of the pointing finger
    hotspot_x = 13  # Centered on finger tip (proportional to 40x40)
    hotspot_y = 0   # At the very top
    
    pixmap = _create_pointing_hand_pixmap(size)
    return QCursor(pixmap, hotspot_x, hotspot_y)


def should_use_custom_cursor() -> bool:
    """
    Check if we should use custom cursors.
    
    Returns True on Linux where Qt often fails to use the system cursor theme.
    """
    return platform.system() == "Linux"


def get_cursor(cursor_shape: Qt.CursorShape) -> QCursor:
    """
    Get a cursor, using custom implementation when needed.
    
    On Linux, PointingHandCursor is replaced with our custom upright hand.
    On other platforms, uses the standard Qt cursor.
    
    Args:
        cursor_shape: The Qt cursor shape to get
        
    Returns:
        QCursor for the requested shape
    """
    if cursor_shape == Qt.CursorShape.PointingHandCursor and should_use_custom_cursor():
        # Use fixed size of 40 for crisp rendering
        return get_pointing_hand_cursor(40)
    
    return QCursor(cursor_shape)


# Convenience function
def pointing_hand_cursor() -> QCursor:
    """Get the pointing hand cursor (custom on Linux, standard elsewhere)."""
    return get_cursor(Qt.CursorShape.PointingHandCursor)