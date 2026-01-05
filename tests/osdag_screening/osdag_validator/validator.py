class Validator:
    """
    Central validator used by CLI, GUI, FastAPI, Batch, and EXE.
    All logic lives here so every interface stays consistent.
    """

    # ---------- FU ----------
    def validate_fu(self, value: int) -> bool:
        try:
            v = int(value)
        except:
            return False
        # Typical steel ultimate strength ranges (MPa)
        return 300 <= v <= 700

    # ---------- FY ----------
    def validate_fy(self, value: int) -> bool:
        try:
            v = int(value)
        except:
            return False
        # Typical yield strength ranges (MPa)
        return 150 <= v <= 500

    # ---------- TF (plate thickness) ----------
    def validate_tf(self, value: float) -> bool:
        try:
            t = float(value)
        except:
            return False
        # Practical thicknesses (mm)
        return 1.0 <= t <= 100.0

    # ---------- Bolt ----------
    VALID_BOLT_SIZES = {"M16", "M20", "M24", "M27", "M30"}
    VALID_BOLT_GRADES = {"4.6", "8.8", "10.9"}

    def validate_bolt(self, size: str, grade: str) -> bool:
        if not size or not grade:
            return False
        size = size.strip().upper()
        grade = grade.strip()

        return (size in self.VALID_BOLT_SIZES) and (grade in self.VALID_BOLT_GRADES)

    # ---------- Plate (thickness x width check) ----------
    def validate_plate(self, thickness: float, width: float) -> bool:
        try:
            t = float(thickness)
            w = float(width)
        except:
            return False

        if not (1 <= t <= 100):
            return False
        if not (50 <= w <= 2000):
            return False

        return True
