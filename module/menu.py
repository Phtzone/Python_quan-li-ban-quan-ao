from .khach_hang import add_customer_to_db
from .khach_hang import update_customer_in_db
from .khach_hang import delete_customer_from_db
from .khach_hang import show_purchase_history
from .khach_hang import handle_them_khach_moi
from .hoa_don import show_hoa_don_in_range
from .hoa_don import sort_hoa_don
from module.hoa_don import load_all_hoa_don
from .kho import handle_update_product
from .kho import on_kho_row_selected
from .kho import xoa_san_pham
from .kho import hien_thi_danh_sach_san_pham
from .kho import chuan_bi_them_moi_san_pham
from .kho import luu_san_pham_moi
from .kho import sap_xep_theo_so_luong_ton_kho
from .phieu_hang import filter_products
from module.khach_hang import filter_customers
from PySide6.QtCore import QDate
from module.khach_hang import on_customer_row_selected
from module.hoa_don import show_hoa_don_detail

# ... sau khi đã tạo xong ui ...


def connect_menus_to_pages(ui):
    """Gán sự kiện click cho từng menu để chuyển trang trong QStackedWidget"""

    ui.bao_cao_menu.mousePressEvent = lambda event: ui.stackedWidget.setCurrentIndex(ui.stackedWidget.indexOf(ui.bao_cao_screen))
    ui.hoa_don_menu.mousePressEvent = lambda event: ui.stackedWidget.setCurrentIndex(ui.stackedWidget.indexOf(ui.hoa_don_screen))
    ui.khach_hang_menu.mousePressEvent = lambda event: ui.stackedWidget.setCurrentIndex(ui.stackedWidget.indexOf(ui.khach_hang_screen))
    ui.phieu_hang_menu.mousePressEvent = lambda event: ui.stackedWidget.setCurrentIndex(ui.stackedWidget.indexOf(ui.phieu_hang_screen))
    ui.kho_menu.mousePressEvent = lambda event: ui.stackedWidget.setCurrentIndex(ui.stackedWidget.indexOf(ui.kho_screen))


def connect_buttons_on_phieu_hang(ui):
    # Gắn sự kiện cập nhật khi gõ hoặc thay đổi
    ui.search_input.textChanged.connect(lambda: filter_products(ui))

def connect_buttons_on_khach_hang(ui):
   # Kết nối các nút trong UI với các hàm
    ui.add_button.clicked.connect(lambda: add_customer_to_db(ui))
    ui.update_button.clicked.connect(lambda: update_customer_in_db(ui))
    ui.delete_button.clicked.connect(lambda: delete_customer_from_db(ui))
    ui.show_history_button.clicked.connect(lambda: show_purchase_history(ui))
    ui.search_khach_hang.textChanged.connect(lambda: filter_customers(ui))
    ui.tableWidget.verticalHeader().setVisible(False)
    ui.them_khach_moi.clicked.connect(lambda: handle_them_khach_moi(ui))
    ui.tableWidget.itemSelectionChanged.connect(lambda: on_customer_row_selected(ui))
    ui.add_button.setEnabled(False)


def connect_buttons_on_hoa_don(ui):
    ui.show_date_from_to_button.clicked.connect(lambda: show_hoa_don_in_range(ui))
    ui.refresh_hoa_don_button.clicked.connect(lambda: load_all_hoa_don(ui))
    ui.sort_from_small_to_big_button.clicked.connect(lambda: sort_hoa_don(ui, tang_dan=True))
    ui.sort_from_big_to_small_button.clicked.connect(lambda: sort_hoa_don(ui, tang_dan=False))
    ui.table_hoa_don.verticalHeader().setVisible(False)
    today = QDate.currentDate()
    thirty_days_ago = today.addDays(-30)
    ui.to_date_edit.setDate(today)
    ui.from_date_edit.setDate(thirty_days_ago)
    ui.table_hoa_don.itemSelectionChanged.connect(lambda: show_hoa_don_detail(ui))

def connect_buttons_on_kho(ui):
    ui.kho_chinh_sua_sua_button.clicked.connect(lambda: handle_update_product(ui))
    ui.kho_chinh_sua_button.clicked.connect(lambda: ui.kho_stackedWidget.setCurrentIndex(0))
    ui.kho_nhap_hang_button.clicked.connect(lambda: (
        ui.kho_stackedWidget.setCurrentIndex(1), 
        sap_xep_theo_so_luong_ton_kho(ui)))
    ui.kho_table_widget.itemSelectionChanged.connect(lambda: on_kho_row_selected(ui))
    ui.kho_xoa_san_pham_button.clicked.connect(lambda: xoa_san_pham(ui))
    ui.kho_tai_lai_san_pham_button.clicked.connect(lambda: hien_thi_danh_sach_san_pham(ui))
    ui.kho_them_moi_button.clicked.connect(lambda: chuan_bi_them_moi_san_pham(ui))
    ui.kho_save_button.clicked.connect(lambda: luu_san_pham_moi(ui))
    ui.kho_table_widget.verticalHeader().setVisible(False)