import hashlib
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox, QHBoxLayout
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def hash_password_with_salt(password: str, salt: bytes) -> str:
    return hashlib.sha256(salt + password.encode('utf-8')).hexdigest()

def read_password_hash() -> str:
    try:
        with open("password.hash", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def read_salt_and_hash():
    with open("password.hash", "r") as f:
        salt_hex, hash_value = f.read().strip().split(":")
        return bytes.fromhex(salt_hex), hash_value

def verify_password(password_input):
    # Kiểm tra integrity file password.hash
    with open("password.hash", "rb") as f:
        file_content = f.read()
    file_hash = hashlib.sha256(file_content).hexdigest()
    with open("log/hash.log") as log_file:
        saved_hash = log_file.read().strip()
    if file_hash != saved_hash:
        raise ValueError("Cảnh báo: File password.hash đã bị thay đổi hoặc bị thay thế!")

    # Tiếp tục kiểm tra mật khẩu như cũ
    salt_hex, hashed_password = file_content.decode().strip().split(":")
    salt = bytes.fromhex(salt_hex)
    hashed_input = hashlib.sha256(salt + password_input.encode('utf-8')).hexdigest()
    return hashed_input == hashed_password

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon("icon/logo.png"))
        self.setWindowTitle("Nhập mật khẩu")
        self.setFixedSize(350, 300)
        layout = QVBoxLayout(self)

        # Thêm hình ảnh logo phía trên
        self.logo_label = QLabel()
        pixmap = QPixmap("icon/logo.png")
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setFixedSize(100, 100)
        self.logo_label.setScaledContents(True)
        layout.addWidget(self.logo_label, alignment=Qt.AlignHCenter)

        self.label = QLabel("<b>Vui lòng nhập mật khẩu để tiếp tục:</b>")
        layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.show_password_checkbox = QCheckBox("Hiện mật khẩu")
        self.show_password_checkbox.toggled.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        button_layout = QHBoxLayout()
        self.button = QPushButton("Xác nhận")
        self.button.clicked.connect(self.check_password)
        button_layout.addStretch()
        button_layout.addWidget(self.button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.accepted = False
        self.password_hash = read_password_hash()

    def toggle_password_visibility(self, checked):
        self.password_input.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)

    def check_password(self):
        if not self.password_hash:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy file hash mật khẩu!")
            return
        try:
            if verify_password(self.password_input.text()):
                self.accepted = True
                self.accept()
            else:
                self.error_label.setText("Mật khẩu không đúng. Vui lòng thử lại.")
        except ValueError as e:
            QMessageBox.critical(self, "Lỗi", str(e))