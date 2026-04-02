import sys
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget,
    QPushButton, QLineEdit, QFormLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QDoubleValidator

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
import osdag_gui.resources.resources_rc

class BoundsSelectorDialog(QDialog):
    def __init__(self, title: str, default: list, parent=None):
        super().__init__(parent)
        # Extract values from list: [upper_bound, lower_bound, step]
        if len(default) >= 3:
            upper_bound = default[1]
            lower_bound = default[0]
            step_value = default[2]
        elif len(default) >= 2:
            upper_bound = default[1]
            lower_bound = default[0]
            step_value = 0.1
        else:
            upper_bound = 1.0
            lower_bound = 0.0
            step_value = 0.1
        
        # Ensure lower_bound is at least 0
        lower_bound = max(0.0, lower_bound)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setObjectName("BoundsSelectorDialog")
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        
        # Set fixed size for the dialog
        self.setFixedSize(320, 220)
        
        # Main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(1, 1, 1, 1)
        mainLayout.setSpacing(0)

        # Custom title bar
        self.titleBar = CustomTitleBar()
        self.titleBar.setTitle("Select Bound: " + title)
        mainLayout.addWidget(self.titleBar)

        # Content widget
        contentWidget = QWidget(self)
        contentWidget.setObjectName("ContentWidget")
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setContentsMargins(20, 20, 20, 20)
        contentLayout.setSpacing(12)

        # Form layout for inputs
        formLayout = QFormLayout()
        formLayout.setSpacing(12)
        formLayout.setContentsMargins(0, 0, 0, 0)
        
        # Lower bound input (restricted to 0 minimum)
        self.lowerBoundLineEdit = QLineEdit(self)
        self.lowerBoundLineEdit.setObjectName("LowerBoundLineEdit")
        self.lowerBoundLineEdit.setText(f"{lower_bound:.2f}")
        self.lowerBoundLineEdit.setFixedHeight(30)
        # Set validator for numeric input (minimum 0)
        lower_validator = QDoubleValidator(0.0, 999999.0, 2, self)
        lower_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.lowerBoundLineEdit.setValidator(lower_validator)

        lowerLabel = QLabel("Lower Bound:", self)
        formLayout.addRow(lowerLabel, self.lowerBoundLineEdit)

        # Upper bound input (above lower bound)
        # Upper bound must be > 0 and > lower bound
        upper_min = max(0.01, lower_bound + 0.01)
        # Ensure initial upper bound is valid
        if upper_bound <= lower_bound or upper_bound <= 0:
            upper_bound = max(upper_min, 1.0)
        
        self.upperBoundLineEdit = QLineEdit(self)
        self.upperBoundLineEdit.setObjectName("UpperBoundLineEdit")
        self.upperBoundLineEdit.setText(f"{upper_bound:.2f}")
        self.upperBoundLineEdit.setFixedHeight(30)
        # Set validator for numeric input - allow any positive number while typing
        # We'll validate against lower bound in _validateUpperBound
        # Use a permissive validator that only checks for positive numbers
        upper_validator = QDoubleValidator(0.0, 999999.0, 2, self)
        upper_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.upperBoundLineEdit.setValidator(upper_validator)

        upperLabel = QLabel("Upper Bound:", self)
        formLayout.addRow(upperLabel, self.upperBoundLineEdit)

        # Step input
        # Step must be > 0 and < (upper_bound - lower_bound)
        step_max = max(0.01, upper_bound - lower_bound - 0.01) if upper_bound > lower_bound else 0.01
        # Use provided step value if valid, otherwise use default
        if step_value > 0 and step_value < (upper_bound - lower_bound):
            default_step = step_value
        else:
            default_step = min(step_max, 0.1) if step_max > 0 else 0.01
        
        self.stepLineEdit = QLineEdit(self)
        self.stepLineEdit.setObjectName("StepLineEdit")
        self.stepLineEdit.setText(f"{default_step:.2f}")
        self.stepLineEdit.setFixedHeight(30)
        # Set validator for numeric input
        step_validator = QDoubleValidator(0.01, step_max, 2, self)
        step_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.stepLineEdit.setValidator(step_validator)

        stepLabel = QLabel("Increment:", self)
        formLayout.addRow(stepLabel, self.stepLineEdit)

        # Connect lower bound changes to update upper bound minimum
        self.lowerBoundLineEdit.textChanged.connect(self._updateUpperBoundMinimum)
        # Connect upper bound changes to validate against lower bound
        # Use both textChanged and editingFinished for better responsiveness
        self.upperBoundLineEdit.textChanged.connect(self._validateUpperBoundOnChange)
        self.upperBoundLineEdit.editingFinished.connect(self._validateUpperBound)
        # Connect bounds changes to update step maximum
        self.lowerBoundLineEdit.textChanged.connect(self._updateStepMaximum)
        self.upperBoundLineEdit.textChanged.connect(self._updateStepMaximum)
        self.upperBoundLineEdit.editingFinished.connect(self._updateStepMaximum)
        # Connect step changes to validate
        self.stepLineEdit.editingFinished.connect(self._validateStep)

        contentLayout.addLayout(formLayout)

        # Button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(6)
        buttonLayout.setContentsMargins(0, 8, 0, 0)
        buttonLayout.addStretch()

        # Cancel button
        self.cancelButton = QPushButton("Cancel", self)
        self.cancelButton.setFixedHeight(30)
        self.cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(self.cancelButton, alignment=Qt.AlignmentFlag.AlignRight)

        # OK button
        self.okButton = QPushButton("OK", self)
        self.okButton.setFixedHeight(30)
        self.okButton.clicked.connect(self.accept)
        buttonLayout.addWidget(self.okButton, alignment=Qt.AlignmentFlag.AlignRight)

        contentLayout.addLayout(buttonLayout)
        mainLayout.addWidget(contentWidget)

        # Store bounds result
        self.bounds = None

    def _validateUpperBoundOnChange(self, text):
        """Validate upper bound on text change - only act if text is a complete valid number"""
        if not text or not text.strip():
            return
        
        # Only validate if the text represents a complete valid number
        try:
            upper_value = float(text.strip())
            lower_text = self.lowerBoundLineEdit.text()
            try:
                lower_value = float(lower_text) if lower_text else 0.0
            except ValueError:
                lower_value = 0.0
            
            # If upper bound is less than or equal to lower bound, adjust lower bound
            if upper_value > 0 and upper_value <= lower_value:
                new_lower = max(0.0, upper_value - 0.01)
                self.lowerBoundLineEdit.blockSignals(True)
                self.lowerBoundLineEdit.setText(f"{new_lower:.2f}")
                self.lowerBoundLineEdit.blockSignals(False)
        except ValueError:
            # Not a complete number yet, ignore
            pass

    def _validateUpperBound(self):
        """Validate upper bound when editing is finished - if smaller than lower bound, adjust lower bound"""
        # Get current lower bound value
        try:
            lower_text = self.lowerBoundLineEdit.text()
            lower_value = float(lower_text) if lower_text else 0.0
        except ValueError:
            lower_value = 0.0
        
        # Get current upper bound value
        upper_text = self.upperBoundLineEdit.text().strip()
        
        # Check if text is empty or invalid
        if not upper_text:
            # If empty, set to minimum valid value
            upper_value = max(0.01, lower_value + 0.01)
            self.upperBoundLineEdit.blockSignals(True)
            self.upperBoundLineEdit.setText(f"{upper_value:.2f}")
            self.upperBoundLineEdit.blockSignals(False)
            return
        
        try:
            upper_value = float(upper_text)
        except ValueError:
            # If invalid input, set to minimum valid value
            upper_value = max(0.01, lower_value + 0.01)
            self.upperBoundLineEdit.blockSignals(True)
            self.upperBoundLineEdit.setText(f"{upper_value:.2f}")
            self.upperBoundLineEdit.blockSignals(False)
            return
        
        # Upper bound must be > 0
        if upper_value <= 0:
            upper_value = 0.01
            self.upperBoundLineEdit.blockSignals(True)
            self.upperBoundLineEdit.setText(f"{upper_value:.2f}")
            self.upperBoundLineEdit.blockSignals(False)
        
        # If upper bound is less than or equal to lower bound, adjust lower bound downward
        if upper_value <= lower_value:
            # Calculate new lower bound: upper - 0.01, but not less than 0
            new_lower = max(0.0, upper_value - 0.01)
            # Block signals to avoid triggering validation
            self.lowerBoundLineEdit.blockSignals(True)
            self.lowerBoundLineEdit.setText(f"{new_lower:.2f}")
            self.lowerBoundLineEdit.blockSignals(False)
        
        # Update step maximum when bounds change
        self._updateStepMaximum()

    def _updateUpperBoundMinimum(self, lower_text):
        """Update upper bound minimum when lower bound changes"""
        try:
            lower_value = float(lower_text) if lower_text else 0.0
        except ValueError:
            lower_value = 0.0
        
        # Upper bound must be > 0 and > lower bound
        new_min = max(0.01, lower_value + 0.01)
        
        # Update validator
        upper_validator = QDoubleValidator(new_min, 999999.0, 2, self)
        upper_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.upperBoundLineEdit.setValidator(upper_validator)
        
        # If current upper bound is less than new minimum, adjust it
        try:
            current_upper_text = self.upperBoundLineEdit.text()
            current_upper = float(current_upper_text) if current_upper_text else new_min
            if current_upper <= new_min:
                # Block signals to avoid triggering validation
                self.upperBoundLineEdit.blockSignals(True)
                self.upperBoundLineEdit.setText(f"{new_min:.2f}")
                self.upperBoundLineEdit.blockSignals(False)
        except ValueError:
            self.upperBoundLineEdit.blockSignals(True)
            self.upperBoundLineEdit.setText(f"{new_min:.2f}")
            self.upperBoundLineEdit.blockSignals(False)
        
        # Update step maximum when bounds change
        self._updateStepMaximum()

    def _updateStepMaximum(self, *args):
        """Update step maximum when bounds change"""
        # Get current bounds
        try:
            lower_text = self.lowerBoundLineEdit.text()
            lower_value = float(lower_text) if lower_text else 0.0
        except ValueError:
            lower_value = 0.0
        
        try:
            upper_text = self.upperBoundLineEdit.text()
            upper_value = float(upper_text) if upper_text else max(0.01, lower_value + 0.01)
        except ValueError:
            upper_value = max(0.01, lower_value + 0.01)
        
        # Calculate maximum step value
        if upper_value > lower_value:
            step_max = upper_value - lower_value - 0.01  # Ensure step is strictly less than range
            step_max = max(0.01, step_max)
        else:
            step_max = 0.01
        
        # Update validator
        step_validator = QDoubleValidator(0.01, step_max, 2, self)
        step_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.stepLineEdit.setValidator(step_validator)
        
        # If current step is greater than new maximum, adjust it
        try:
            current_step_text = self.stepLineEdit.text()
            current_step = float(current_step_text) if current_step_text else 0.01
            if current_step >= step_max:
                self.stepLineEdit.blockSignals(True)
                self.stepLineEdit.setText(f"{step_max:.2f}")
                self.stepLineEdit.blockSignals(False)
        except ValueError:
            self.stepLineEdit.blockSignals(True)
            self.stepLineEdit.setText(f"{step_max:.2f}")
            self.stepLineEdit.blockSignals(False)

    def _validateStep(self):
        """Validate step when editing is finished - ensure it's less than (upper - lower)"""
        # Get current bounds
        try:
            lower_text = self.lowerBoundLineEdit.text()
            lower_value = float(lower_text) if lower_text else 0.0
        except ValueError:
            lower_value = 0.0
        
        try:
            upper_text = self.upperBoundLineEdit.text()
            upper_value = float(upper_text) if upper_text else max(0.01, lower_value + 0.01)
        except ValueError:
            upper_value = max(0.01, lower_value + 0.01)
        
        # Get current step value
        step_text = self.stepLineEdit.text().strip()
        
        if not step_text:
            step_max = max(0.01, upper_value - lower_value - 0.01) if upper_value > lower_value else 0.01
            self.stepLineEdit.setText(f"{step_max:.2f}")
            return
        
        try:
            step_value = float(step_text)
        except ValueError:
            step_max = max(0.01, upper_value - lower_value - 0.01) if upper_value > lower_value else 0.01
            self.stepLineEdit.setText(f"{step_max:.2f}")
            return
        
        # Calculate maximum step value
        if upper_value > lower_value:
            step_max = upper_value - lower_value - 0.01
            step_max = max(0.01, step_max)
        else:
            step_max = 0.01
        
        # Step must be > 0
        if step_value <= 0:
            self.stepLineEdit.setText(f"{step_max:.2f}")
            return
        
        # Step must be < (upper - lower)
        if step_value >= (upper_value - lower_value):
            self.stepLineEdit.setText(f"{step_max:.2f}")

    def getBounds(self):
        """Return the selected bounds as a list [upper_bound, lower_bound, step] or None if cancelled"""
        if self.bounds is not None:
            return self.bounds
        return None

    def accept(self):
        """Override accept to store bounds before closing"""
        # Get values from text fields
        try:
            lower_text = self.lowerBoundLineEdit.text()
            lower = max(0.0, float(lower_text) if lower_text else 0.0)
        except ValueError:
            lower = 0.0
        
        try:
            upper_text = self.upperBoundLineEdit.text()
            upper = float(upper_text) if upper_text else max(0.01, lower + 0.01)
        except ValueError:
            upper = max(0.01, lower + 0.01)
        
        # Validate that upper bound is greater than 0
        if upper <= 0:
            upper = max(0.01, lower + 0.01)
        
        # Validate that upper bound is greater than lower bound
        if upper <= lower:
            upper = lower + 0.01
        
        # Get step value
        try:
            step_text = self.stepLineEdit.text()
            step = float(step_text) if step_text else 0.01
        except ValueError:
            step = 0.01
        
        # Validate step
        if step <= 0:
            step = 0.01
        
        # Step must be less than (upper - lower)
        step_max = upper - lower - 0.01 if upper > lower else 0.01
        step_max = max(0.01, step_max)
        if step >= (upper - lower):
            step = step_max
        
        # Return as list [upper_bound, lower_bound, step]
        self.bounds = [lower, upper, step]
        super().accept()

    def exec(self):
        """Override exec to return bounds tuple"""
        super().exec()
        return self.getBounds()


# For testing
# if __name__ == "__main__":
#     from PySide6.QtWidgets import QApplication
    
#     app = QApplication(sys.argv)
#     dialog = BoundsSelectorDialog("Diameter", default=[100.0, 0.0, 0.1])
#     result = dialog.exec()
#     if result:
#         print(f"Selected bounds: Upper = {result[0]}, Lower = {result[1]}, Step = {result[2]}")
#     else:
#         print("Dialog was cancelled")
