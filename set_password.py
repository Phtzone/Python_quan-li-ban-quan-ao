import hashlib
import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QCheckBox, QHBoxLayout, QApplication, QMessageBox
)
from PySide6.QtGui import QIcon, QPixmap
import sys
from PySide6.QtCore import Qt
import datetime

def hash_password_with_salt(password: str, salt: bytes) -> str:
    return hashlib.sha256(salt + password.encode('utf-8')).hexdigest()

class SetPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon("icon/logo.png"))
        self.setWindowTitle("Tạo mật khẩu mới")
        self.setFixedSize(300, 300)
        layout = QVBoxLayout(self)

        # Thêm hình ảnh logo phía trên
        self.logo_label = QLabel()
        pixmap = QPixmap("icon/logo.png")
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setFixedSize(100, 100)
        self.logo_label.setScaledContents(True)
        layout.addWidget(self.logo_label, alignment=Qt.AlignHCenter)

        self.label = QLabel("<b>Nhập mật khẩu mới:</b>")
        layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Mật khẩu mới")
        layout.addWidget(self.password_input)

        self.password_confirm = QLineEdit()
        self.password_confirm.setEchoMode(QLineEdit.Password)
        self.password_confirm.setPlaceholderText("Nhập lại mật khẩu")
        layout.addWidget(self.password_confirm)

        self.show_password_checkbox = QCheckBox("Hiện mật khẩu")
        self.show_password_checkbox.toggled.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        button_layout = QHBoxLayout()
        self.button = QPushButton("Xác nhận")
        self.button.clicked.connect(self.set_password)
        button_layout.addStretch()
        button_layout.addWidget(self.button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.success = False

    def toggle_password_visibility(self, checked):
        mode = QLineEdit.Normal if checked else QLineEdit.Password
        self.password_input.setEchoMode(mode)
        self.password_confirm.setEchoMode(mode)

    def set_password(self):
        password = self.password_input.text()
        confirm = self.password_confirm.text()
        if len(password) < 6:
            self.error_label.setText("Mật khẩu phải có ít nhất 6 ký tự.")
            return
        if password != confirm:
            self.error_label.setText("Mật khẩu nhập lại không khớp.")
            return
        reply = QMessageBox.question(
            self,
            "Xác nhận đổi mật khẩu",
            "Bạn có chắc chắn muốn đổi mật khẩu không?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            salt = os.urandom(16)
            hashed = hash_password_with_salt(password, salt)
            with open("password.hash", "w") as f:
                f.write(f"{salt.hex()}:{hashed}")

            # Tính hash của file password.hash và lưu vào log/hash.log
            with open("password.hash", "rb") as f:
                file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            with open("log/hash.log", "w") as log_file:
                log_file.write(file_hash)

            self.success = True
            self.accept()
        else:
            self.success = False
            self.reject()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = SetPasswordDialog()
    if dlg.exec() and dlg.success:
        print("Đã tạo mật khẩu mới thành công!")
    else:
        print("Chưa tạo mật khẩu.")