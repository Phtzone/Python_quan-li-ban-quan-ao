from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ImageDropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.image_path = None
        self.setText("Kéo thả ảnh JPG vào đây")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed gray;")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".jpg"):
                self.image_path = file_path
                self.setPixmap(QPixmap(self.image_path).scaledToWidth(200))
                print(f"Đã chọn ảnh: {self.image_path}")
    def clear_image(self):
        self.clear()
        self.setText("Kéo thả ảnh JPG vào đây")
        self.image_path = None
