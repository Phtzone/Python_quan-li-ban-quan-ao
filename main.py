import sys
import os
import subprocess
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout
from main_ui import Ui_MainWindow

# module import 
from module.menu import connect_menus_to_pages
from module.menu import connect_buttons_on_khach_hang
from module.menu import connect_buttons_on_hoa_don
from module.menu import connect_buttons_on_kho
from module.menu import connect_buttons_on_phieu_hang
from module.khach_hang import display_customers
from module.phieu_hang import load_products_to_scroll_area, cap_nhat_danh_sach_san_pham
from module.phieu_hang import create_phieu_hang_tab
from module.hoa_don import load_all_hoa_don
from module.kho import hien_thi_danh_sach_san_pham, load_danh_muc_vao_combobox
from module.kho import on_kho_table_row_selected
from module.bao_cao import khoi_tao_bao_cao
from database.connection import create_connection
from image_drop_label import ImageDropLabel
from password_dialog import PasswordDialog

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Load UI

        layout = QVBoxLayout(self.ui.centralwidget)
        self.ui.centralwidget.setLayout(layout)

        connect_menus_to_pages(self.ui)
        connect_buttons_on_khach_hang(self.ui)
        connect_buttons_on_hoa_don(self.ui)
        connect_buttons_on_kho(self.ui)
        connect_buttons_on_phieu_hang(self.ui)
        create_connection()

        # test
        display_customers(self.ui)
        load_all_hoa_don(self.ui)
        load_products_to_scroll_area(self.ui)
        hien_thi_danh_sach_san_pham(self.ui)
        load_danh_muc_vao_combobox(self.ui)
        self.ui.create_ticket_button.clicked.connect(lambda: create_phieu_hang_tab(self.ui))
        self.ui.cap_nhat.clicked.connect(lambda: cap_nhat_danh_sach_san_pham(self.ui))

        self.ui.kho_xoa_san_pham_button.setEnabled(False)
        self.ui.kho_table_widget.itemSelectionChanged.connect(lambda: on_kho_table_row_selected(self.ui))
        
        # Khởi tạo module báo cáo
        khoi_tao_bao_cao(self.ui)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Hiển thị dialog nhập mật khẩu
    password_dialog = PasswordDialog()
    if password_dialog.exec() == QDialog.Accepted and password_dialog.accepted:
        window = MyApp()
        window.setWindowIcon(QIcon("icon/logo.png"))
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit()
