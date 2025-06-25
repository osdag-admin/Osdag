
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QFileDialog, QHeaderView, QMessageBox
)
import matplotlib.pyplot as plt


class PlotInputWidget(QWidget):
    def __init__(self, plot_type="BM"):  # "BM" or "SF"
        super().__init__()

        self.plot_type = plot_type
        self.setWindowTitle(f"{'BMD' if plot_type == 'BM' else 'SFD'} Plotter")

        self.layout = QVBoxLayout(self)

        # Setup Table
        self.table = QTableWidget(5, 2)
        self.table.setHorizontalHeaderLabels(["Distance (m)", "BM (kNm)" if plot_type == "BM" else "SF (kN)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(QLabel(f"Enter Distance and {'Bending Moment' if plot_type == 'BM' else 'Shear Force'} values:"))
        self.layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.plot_btn = QPushButton(f"Plot {'BMD' if plot_type == 'BM' else 'SFD'}")
        # self.save_btn = QPushButton("Save as PNG")
        self.add_row_btn = QPushButton("Add Row")
        btn_layout.addWidget(self.add_row_btn)
        btn_layout.addWidget(self.plot_btn)
        # btn_layout.addWidget(self.save_btn)
        self.layout.addLayout(btn_layout)

        # Connections
        self.add_row_btn.clicked.connect(self.add_row)
        self.plot_btn.clicked.connect(self.plot_graph)
        # self.save_btn.clicked.connect(self.save_plot)

    def add_row(self):
        self.table.insertRow(self.table.rowCount())

    def get_data(self):
        x_vals = []
        y_vals = []

        for row in range(self.table.rowCount()):
            try:
                xi = float(self.table.item(row, 0).text())
                yi = float(self.table.item(row, 1).text())
                x_vals.append(xi)
                y_vals.append(yi)
            except (ValueError, AttributeError):
                continue

        if len(x_vals) < 2:
            QMessageBox.warning(self, "Invalid Input", "Please enter at least two valid data points.")
            return None, None

        # Sort by distance
        return zip(*sorted(zip(x_vals, y_vals)))

    def plot_graph(self):
        x, y = self.get_data()
        if x is None:
            return

        color = 'r' if self.plot_type == "BM" else 'b'
        title = "Bending Moment Diagram" if self.plot_type == "BM" else "Shear Force Diagram"
        ylabel = "BM (kNm)" if self.plot_type == "BM" else "SF (kN)"
        # plt.rcParams['home'] = 'none'
        fig, ax = plt.subplots(figsize=(8, 4))
        line, = ax.plot(x, y, color=color, linewidth=2, marker='o', label=title)

        # Draw vertical dashed lines from each point to X-axis
        for xi, yi in zip(x, y):
            ax.vlines(xi, 0, yi, colors=color, linestyles='dashed', alpha=0.6)

        ax.set_title(title)
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.axhline(0, color='black', linewidth=1)

        # Hover annotation
        annot = ax.annotate("", xy=(0,0), xytext=(15,15), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(ind):
            index = ind["ind"][0]
            x_val = x[index]
            y_val = y[index]
            annot.xy = (x_val, y_val)
            annot.set_text(f"x={x_val:.2f}\ny={y_val:.2f}")
            annot.get_bbox_patch().set_alpha(0.9)

        def hover(event):
            if event.inaxes == ax and event.xdata is not None:
                x_mouse = event.xdata

                # Find two x-values around the mouse (for interpolation)
                for i in range(len(x) - 1):
                    if x[i] <= x_mouse <= x[i + 1]:
                        # Linear interpolation
                        x1, x2 = x[i], x[i + 1]
                        y1, y2 = y[i], y[i + 1]

                        # Interpolated y value
                        slope = (y2 - y1) / (x2 - x1)
                        y_interp = y1 + slope * (x_mouse - x1)

                        # Update annotation
                        annot.xy = (x_mouse, y_interp)
                        annot.set_text(f"x={x_mouse:.2f}\ny={y_interp:.2f}")
                        annot.set_visible(True)
                        fig.canvas.draw_idle()
                        return

                annot.set_visible(False)
                fig.canvas.draw_idle()


        fig.canvas.mpl_connect("motion_notify_event", hover)
        plt.tight_layout()
        plt.legend()
        plt.show()
        

    def save_plot(self):
        x, y = self.get_data()
        if x is None:
            return

        fname, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png)")
        if fname:
            color = 'r' if self.plot_type == "BM" else 'b'
            title = "Bending Moment Diagram" if self.plot_type == "BM" else "Shear Force Diagram"
            ylabel = "BM (kNm)" if self.plot_type == "BM" else "SF (kN)"

            plt.figure(figsize=(8, 4))
            plt.plot(x, y, color=color, linewidth=2, marker='o')
            for xi, yi in zip(x, y):
                plt.vlines(xi, 0, yi, colors=color, linestyles='dashed', alpha=0.7)
            plt.axhline(0, color='black', linewidth=1)
            plt.title(title)
            plt.xlabel("Distance (m)")
            plt.ylabel(ylabel)
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(fname)
            plt.close()

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Paste):
            clipboard = QApplication.clipboard()
            text = clipboard.text()
            rows = text.strip().split("\n")
            current_row = self.table.currentRow()
            current_col = self.table.currentColumn()

            for r_idx, row_data in enumerate(rows):
                columns = row_data.split("\t")
                for c_idx, cell in enumerate(columns):
                    target_row = current_row + r_idx
                    target_col = current_col + c_idx
                    # Expand if necessary
                    if target_row >= self.table.rowCount():
                        self.table.insertRow(self.table.rowCount())
                    item = QTableWidgetItem(cell.strip())
                    self.table.setItem(target_row, target_col, item)
        else:
            super().keyPressEvent(event)
    def showEvent(self, event):
    # Clear table contents every time the widget is shown
        self.table.clearContents()
        self.table.setRowCount(5)  # Reset to default number of rows
        super().showEvent(event)



