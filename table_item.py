from PySide6.QtWidgets import QTableWidgetItem

class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return int(self.text() or 0) < int(other.text() or 0)
        except (ValueError, TypeError):
            # fallback: so sánh chuỗi an toàn, tránh gọi lại super().__lt__ để không bị đệ quy
            self_text = self.text() if self.text() is not None else ""
            other_text = other.text() if other.text() is not None else ""
            return self_text < other_text
