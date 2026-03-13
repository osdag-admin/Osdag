"""
occ_navicube_sync.py  —  OCC ↔ NaviCubeOverlay synchronisation helper
═══════════════════════════════════════════════════════════════════════
Bridges an OCC V3d_View with a NaviCubeOverlay widget.

NaviCubeOverlay is a zero-dependency PySide6 widget.  This file is the
only place in the stack that imports OCC — keeping the widget itself
publishable as a pure-Qt library.

Usage
─────
    from osdag_gui.ui.components.navicube_overlay import NaviCubeOverlay
    from osdag_gui.ui.components.occ_navicube_sync import OCCNaviCubeSync

    navicube = NaviCubeOverlay(parent=tab_widget)
    navicube.show()

    # Call once your OCC view is ready (e.g. inside display_view_cube):
    sync = OCCNaviCubeSync(occ_view, navicube)

    # In your viewer's mousePressEvent / mouseReleaseEvent:
    sync.set_interaction_active(True)   # press
    sync.set_interaction_active(False)  # release

    # When the viewer is torn down:
    sync.teardown()

Camera direction convention
───────────────────────────
  push_camera receives the INWARD direction (eye → scene), which is
  exactly what OCC cam.Direction() returns — no sign flip needed.

  viewOrientationRequested emits the OUTWARD direction (−inward), which
  is what OCC V3d_View.SetProj(Vx,Vy,Vz) expects.
"""

import math
import numpy as np
from PySide6.QtCore import QTimer


class OCCNaviCubeSync:
    """
    Connects an OCC V3d_View to a NaviCubeOverlay.

    Responsibilities
    ────────────────
    · Polls the OCC camera every N ticks and calls navicube.push_camera()
    · Connects navicube.viewOrientationRequested → updates OCC camera
      atomically (SetEye + SetUp, single Redraw — no intermediate renders)
    · Forwards set_interaction_active() to the navicube for SLERP smoothing
    · Cleans itself up on teardown() with no dangling references

    Parameters
    ──────────
    view      OCC V3d_View instance (must already be initialised)
    navicube  NaviCubeOverlay instance
    """

    _TICK_MS           = 16   # poll interval (ms)
    _INTERACTION_TICKS = 1    # poll every tick during live drag (~16 ms lag)
    _IDLE_TICKS        = 4    # poll every 4 ticks when idle  (~64 ms lag)

    def __init__(self, view, navicube):
        self._view     = view
        self._navicube = navicube
        self._interaction_active = False
        self._tick_count = 0

        navicube.viewOrientationRequested.connect(self._on_orientation_requested)

        self._tmr = QTimer()
        self._tmr.timeout.connect(self._tick)
        self._tmr.start(self._TICK_MS)

    # ── public ──────────────────────────────────────────────────────

    def set_interaction_active(self, active: bool) -> None:
        """
        Call with True when the user starts dragging the camera,
        False when they release.  Forwarded to the navicube for
        SLERP smoothing and to the poll rate selector.
        """
        self._interaction_active = bool(active)
        self._tick_count = 0   # force an immediate camera read on state change
        if self._navicube is not None:
            self._navicube.set_interaction_active(active)

    def teardown(self) -> None:
        """
        Stop polling and disconnect all signals.
        Call this when the OCC view is being destroyed.
        """
        self._tmr.stop()
        try:
            if self._navicube is not None:
                self._navicube.viewOrientationRequested.disconnect(
                    self._on_orientation_requested
                )
        except Exception:
            pass
        self._view     = None
        self._navicube = None

    # ── internals ───────────────────────────────────────────────────

    def _tick(self) -> None:
        """Poll OCC camera and push state to the navicube."""
        if self._view is None or self._navicube is None:
            return

        poll_every = (
            self._INTERACTION_TICKS
            if self._interaction_active
            else self._IDLE_TICKS
        )
        self._tick_count += 1
        if self._tick_count < poll_every:
            return
        self._tick_count = 0

        try:
            cam = self._view.Camera()
            cd  = cam.Direction()
            cu  = cam.Up()
            # Direction() is already inward (eye→scene) — push as-is
            self._navicube.push_camera(
                cd.X(), cd.Y(), cd.Z(),
                cu.X(), cu.Y(), cu.Z(),
            )
        except Exception:
            pass  # OCC not yet ready or being torn down — skip silently

    def _on_orientation_requested(
        self,
        px: float, py: float, pz: float,
        ux: float, uy: float, uz: float,
    ) -> None:
        """
        Navicube face/button clicked: animate OCC camera to the new
        orientation.

        Uses cam.SetEye() + cam.SetUp() on the Camera handle directly
        (rather than view.SetProj + view.SetUp) to avoid OCC's internal
        ImmediateUpdate() triggering an intermediate render with the new
        direction but the old up-vector — which was the source of the
        per-frame flicker during animation.
        """
        if self._view is None:
            return

        mag = math.sqrt(px * px + py * py + pz * pz)
        if mag < 1e-6:
            return

        try:
            from OCC.Core.gp import gp_Dir, gp_Pnt
            cam    = self._view.Camera()
            center = cam.Center()
            eye    = cam.Eye()
            dist   = math.sqrt(
                (eye.X() - center.X()) ** 2 +
                (eye.Y() - center.Y()) ** 2 +
                (eye.Z() - center.Z()) ** 2
            )
            if dist < 1e-6:
                dist = 1.0
            scale = dist / mag
            # Move eye to new outward direction, keep center (focal point) fixed
            cam.SetEye(gp_Pnt(
                center.X() + px * scale,
                center.Y() + py * scale,
                center.Z() + pz * scale,
            ))
            cam.SetUp(gp_Dir(ux, uy, uz))
            self._view.Redraw()
        except Exception:
            # Fallback for older OCC / pythonocc builds without Camera handle API
            try:
                self._view.SetProj(px, py, pz)
                self._view.SetUp(ux, uy, uz)
                self._view.Redraw()
            except Exception:
                pass
