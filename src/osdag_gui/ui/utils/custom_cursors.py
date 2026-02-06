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
    Create a sharp, high-quality upright pointing hand cursor.
    
    This creates the classic hand cursor with index finger pointing up,
    black fill with white border - rendered at high resolution for sharpness.
    
    Args:
        size: Size of the cursor in pixels (default 40)
        
    Returns:
        QPixmap with transparent background and hand cursor drawn
    """
    # Exact match to user's pixel art reference
    # 0 = transparent, 1 = white (border), 2 = black (fill)
    cursor_data = [
        "00000000000111100000000000000000",
        "00000000001222100000000000000000",
        "00000000001222100000000000000000",
        "00000000001222100000000000000000",
        "00000000001222100000000000000000",
        "00000000001222100000000000000000",
        "00000000001222111100000000000000",
        "00000000001222222100000000000000",
        "00000000001222222111100000000000",
        "00000001111222222222100000000000",
        "00000012221222222222111000000000",
        "00000012222222222222221000000000",
        "00000001222222222222221000000000",
        "00000000122222222222221000000000",
        "00000000122222222222221000000000",
        "00000000012222222222221000000000",
        "00000000012222222222221000000000",
        "00000000001222222222221000000000",
        "00000000001222222222221000000000",
        "00000000000122222222210000000000",
        "00000000000122222222210000000000",
        "00000000000111111111100000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
        "00000000000000000000000000000000",
    ]
    
    # Render at high resolution (4x) to ensure no gaps, then scale down for sharpness
    native_size = 32
    high_res_scale = 4  # 4x resolution for super sharp rendering
    high_res_size = native_size * high_res_scale
    
    high_res_pixmap = QPixmap(high_res_size, high_res_size)
    high_res_pixmap.fill(Qt.transparent)
    
    painter = QPainter(high_res_pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)  # No AA at high-res
    
    # Colors: White border, Black fill for clear visibility
    border_color = QColor(255, 255, 255, 255)  # White border
    fill_color = QColor(0, 0, 0, 255)          # Black fill
    
    # Draw each pixel at high resolution (4x4 pixels per original pixel)
    for y, row in enumerate(cursor_data):
        for x, pixel in enumerate(row):
            if pixel == '1':  # Border
                painter.fillRect(
                    x * high_res_scale, 
                    y * high_res_scale,
                    high_res_scale, 
                    high_res_scale,
                    border_color
                )
            elif pixel == '2':  # Fill
                painter.fillRect(
                    x * high_res_scale, 
                    y * high_res_scale,
                    high_res_scale, 
                    high_res_scale,
                    fill_color
                )
    
    painter.end()
    
    # Scale down to target size with smooth transformation for sharp, clean result
    from PySide6.QtCore import Qt as QtCore
    pixmap = high_res_pixmap.scaled(
        size, size,
        QtCore.AspectRatioMode.KeepAspectRatio,
        QtCore.TransformationMode.SmoothTransformation
    )
    
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
        size: Cursor size in pixels (default 32)
        
    Returns:
        QCursor with upright pointing hand
    """
    # The hotspot is at the tip of the pointing finger
    hotspot_x = int(size * 10 / 32)  # Centered on finger tip
    hotspot_y = 0  # At the very top
    
    pixmap = _create_pointing_hand_pixmap(size)
    return QCursor(pixmap, hotspot_x, hotspot_y)


def should_use_custom_cursor() -> bool:
    """
    Check if we should use custom cursors.
    
    Returns True for all platforms to ensure consistent cursor appearance.
    """
    return True


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
        # Get cursor size from environment or use default
        size = int(os.environ.get("XCURSOR_SIZE", "40"))
        return get_pointing_hand_cursor(size)
    
    return QCursor(cursor_shape)


# Convenience function
def pointing_hand_cursor() -> QCursor:
    """Get the pointing hand cursor (custom on Linux, standard elsewhere)."""
    return get_cursor(Qt.CursorShape.PointingHandCursor)
