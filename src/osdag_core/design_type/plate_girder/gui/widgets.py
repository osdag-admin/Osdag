from PySide6.QtWidgets import QListWidget, QListWidgetItem
import re

class My_ListWidget(QListWidget):
    def addItems(self, Iterable, p_str=None):
        super().addItems(Iterable)
        self.sortItems()

    def addItem(self, *__args):
        super().addItem(My_ListWidgetItem(__args[0]))
        self.sortItems()

class My_ListWidgetItem(QListWidgetItem):
    def __lt__(self, other):
        try:
            self_text = str(re.sub("[^0-9.]", "", self.text()))
            other_text = str(re.sub("[^0-9.]", "", other.text()))
            return float(self_text) < float(other_text)
        except Exception:
            return super().__lt__(other)
