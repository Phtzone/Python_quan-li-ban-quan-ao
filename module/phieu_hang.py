# file: functions/phieu_hang_functions.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame, QPushButton, QPushButton, QScrollArea, QLineEdit, QTabWidget, QTabBar, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from datetime import datetime
import os
import uuid
from database.connection import create_connection  # tùy cấu trúc folder
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import webbrowser
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from fuzzywuzzy import process, fuzz
import unidecode
import cv2
from pyzbar.pyzbar import decode

def load_products_to_scroll_area(ui, products=None):
    """Hiển thị sản phẩm ra khu vực scroll area, nhóm theo danh mục"""
    widget = ui.danh_sach_san_pham

    # Khởi tạo dict lưu số lượng tồn kho hiển thị nếu chưa có
    if not hasattr(ui, "ton_kho_hienthi"):
        ui.ton_kho_hienthi = {}

    # Nếu widget chưa có layout, tạo mới
    if widget.layout() is None:
        grid = QGridLayout()
        grid.setSpacing(10)
        widget.setLayout(grid)
    else:
        grid = widget.layout()
        # Xóa các widget cũ trong grid
        while grid.count():
            child = grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # Nếu không truyền vào danh sách sản phẩm → lấy toàn bộ từ DB (lấy cả danh mục)
    if products is None:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sp.id_san_pham, sp.ten_san_pham, sp.gia_san_pham, sp.so_luong_ton_kho, dm.id_danh_muc, dm.ten_danh_muc
            FROM danh_sach_san_pham sp
            JOIN danh_muc_san_pham dm ON sp.id_danh_muc = dm.id_danh_muc
        """)
        products = cursor.fetchall()
        cursor.close()
        conn.close()

    # Nhóm sản phẩm theo danh mục
    from collections import defaultdict
    grouped = defaultdict(list)
    for sp in products:
        id_danh_muc, ten_danh_muc = sp[4], sp[5]
        grouped[(id_danh_muc, ten_danh_muc)].append(sp)

    row = 0
    for (id_danh_muc, ten_danh_muc), sp_list in grouped.items():
        # Thêm label tên danh mục
        label = QLabel(f"{ten_danh_muc}")
        label.setStyleSheet("font-weight: bold; font-size: 15px; color: #1a237e;")
        grid.addWidget(label, row, 0, 1, 4)  # span 4 cột
        row += 1
        for i, sp in enumerate(sp_list):
            id_sp, ten, gia, ton_kho = sp[0], sp[1], sp[2], sp[3]
            ton_kho_hienthi = ui.ton_kho_hienthi.get(id_sp, ton_kho)
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFixedSize(130, 160)

            layout = QVBoxLayout(frame)
            layout.setAlignment(Qt.AlignTop)

            # Hiển thị hình ảnh sản phẩm
            image_path = os.path.join("image", f"{id_sp}.jpg")
            img_label = QLabel()
            pixmap = QPixmap(image_path)

            if not pixmap.isNull():
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                img_label.setPixmap(pixmap)
            else:
                img_label.setText("No image")
                img_label.setAlignment(Qt.AlignCenter)

            # Tên và giá
            ten_label = QLabel(ten)
            ten_label.setAlignment(Qt.AlignCenter)
            gia_label = QLabel(f"{gia:,} đ")
            gia_label.setStyleSheet("color: red")
            gia_label.setAlignment(Qt.AlignCenter)

            # Số lượng tồn kho (góc phải dưới)
            so_luong_label = QLabel(f"Tồn: {ton_kho_hienthi}")
            so_luong_label.setStyleSheet("color: #555; font-size: 11px;")
            so_luong_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
            frame.ton_kho_label = so_luong_label

            # Thêm label ID sản phẩm (góc trái dưới)
            id_label = QLabel(f"ID: {id_sp}")
            id_label.setStyleSheet("color: #888; font-size: 11px;")
            id_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

            # Layout ngang cho hàng dưới cùng
            bottom_layout = QHBoxLayout()
            bottom_layout.addWidget(id_label, alignment=Qt.AlignLeft)
            bottom_layout.addWidget(so_luong_label, alignment=Qt.AlignRight)

            # Thêm vào layout
            layout.addWidget(img_label)
            layout.addWidget(ten_label)
            layout.addWidget(gia_label)
            layout.addStretch()
            layout.addLayout(bottom_layout)

            # Gắn dữ liệu và sự kiện
            frame.data = {"id": id_sp, "ten": ten, "gia": gia}
            frame.mousePressEvent = lambda event, d=frame.data: add_product_to_current_tab(ui, d)

            # Thêm vào lưới
            col = i % 4
            grid.addWidget(frame, row, col)
            if col == 3:
                row += 1
        if (len(sp_list) % 4) != 0:
            row += 1  # sang dòng mới cho nhóm tiếp theo
        else:
            row += 0  # không tăng nếu đã đủ 4 cột
        # Lưu số lượng tồn kho hiển thị vào dict
        for sp in sp_list:
            id_sp, _, _, ton_kho = sp[0], sp[1], sp[2], sp[3]
            ui.ton_kho_hienthi[id_sp] = ui.ton_kho_hienthi.get(id_sp, ton_kho)


def create_phieu_hang_tab(ui):
    new_tab = QWidget()
    layout = QVBoxLayout(new_tab)

    scroll = QScrollArea()
    scroll.setFixedHeight(430)
    scroll.setWidgetResizable(True)
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)
    scroll.setWidget(scroll_content)
    # Đảm bảo scroll_content không bị co giãn dọc
    scroll_content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    tong_tien_label = QLabel("Tổng tiền: 0 đ")
    tong_tien_label.setStyleSheet("font-size: 18px; font-weight: bold;")
    tong_tien_label.setAlignment(Qt.AlignRight)

    khach_id_layout = QHBoxLayout()
    khach_id_label = QLabel("ID Khách hàng:")
    khach_id_input = QLineEdit()
    khach_id_input.setFixedWidth(100)
    khach_id_layout.addWidget(khach_id_label)
    khach_id_layout.addWidget(khach_id_input)
    khach_id_layout.addStretch()

    btn_thanh_toan = QPushButton("Thanh toán")
    khach_id_layout.addWidget(btn_thanh_toan)
    
    btn_xuat_phieu = QPushButton("Xuất phiếu hàng")
    khach_id_layout.addWidget(btn_xuat_phieu)

    # Thêm nút Quét QR
    btn_quet_qr = QPushButton("Quét QR")
    khach_id_layout.addWidget(btn_quet_qr)
    btn_quet_qr.clicked.connect(lambda: quet_qr_san_pham(ui))

    layout.addWidget(scroll)
    layout.addWidget(tong_tien_label)
    layout.addLayout(khach_id_layout)

    new_tab.setLayout(layout)

    tab_index = ui.tab_phieu_hang.count()
    close_button = QPushButton("✖")
    close_button.setStyleSheet("color: red; font-weight: bold;")
    close_button.setFixedSize(20, 20)

    # Thêm cờ trạng thái đã thanh toán
    new_tab.is_paid = False

    def close_tab():
        # Chỉ hoàn lại tồn kho nếu phiếu chưa thanh toán
        if not getattr(new_tab, "is_paid", False):
            products = getattr(new_tab, "products", {})
            for ten_sp, sp in products.items():
                so_luong = int(sp["so_luong_label"].text())
                id_sp = sp.get("id")
                if id_sp is not None and hasattr(ui, "ton_kho_hienthi"):
                    ui.ton_kho_hienthi[id_sp] += so_luong
                    update_ton_kho_label(ui, id_sp)
        ui.tab_phieu_hang.removeTab(ui.tab_phieu_hang.indexOf(new_tab))

    close_button.clicked.connect(close_tab)

    tab_title = f"Phiếu {tab_index + 1} "
    tab_widget = QWidget()
    tab_layout = QHBoxLayout(tab_widget)
    tab_layout.setContentsMargins(5, 0, 0, 0)
    tab_layout.addWidget(QLabel(tab_title))
    tab_layout.addWidget(close_button)
    tab_layout.addStretch()
    ui.tab_phieu_hang.addTab(new_tab, "")
    ui.tab_phieu_hang.setTabEnabled(tab_index, True)
    ui.tab_phieu_hang.setTabText(tab_index, "")
    ui.tab_phieu_hang.tabBar().setTabButton(tab_index, QTabBar.RightSide, tab_widget)
    ui.tab_phieu_hang.setCurrentIndex(tab_index)

    # Gắn layout & label vào tab widget để truy cập sau
    new_tab.scroll_layout = scroll_layout
    new_tab.tong_tien_label = tong_tien_label
    new_tab.products = {}  # dict lưu sản phẩm đã thêm
    new_tab.khach_id_input = khach_id_input

    # Gắn chức năng thanh toán
    btn_thanh_toan.clicked.connect(lambda: thanh_toan_phieu(new_tab))

    # Gắn chức năng xuất phiếu
    btn_xuat_phieu.clicked.connect(lambda: xuat_phieu_hang(new_tab))

    return new_tab


def add_product_to_current_tab(ui, product_data):
    tab_index = ui.tab_phieu_hang.currentIndex()
    tab = ui.tab_phieu_hang.widget(tab_index)

    layout = getattr(tab, "scroll_layout", None)
    if layout is None:
        print("Không tìm thấy scroll_layout")
        return

    ten_sp = product_data["ten"]
    gia_sp = product_data["gia"]
    id_sp = product_data.get("id")  # lấy id sản phẩm (nếu có)

    # Nếu sản phẩm đã có → tăng số lượng
    if ten_sp in tab.products:
        sp = tab.products[ten_sp]
        so_luong_label = sp["so_luong_label"]
        so_luong = int(so_luong_label.text()) + 1
        # Kiểm tra tồn kho hiển thị trước khi tăng
        if ui.ton_kho_hienthi.get(id_sp, 0) <= 0:
            QMessageBox.warning(tab, "Lỗi", "Sản phẩm đã hết hàng!")
            return
        so_luong_label.setText(str(so_luong))
        cap_nhat_tong_tien(tab)
        # Trừ tồn kho hiển thị
        ui.ton_kho_hienthi[id_sp] -= 1
        update_ton_kho_label(ui, id_sp)
        # Cập nhật lại chiều cao scroll_content
        update_scroll_content_height(tab)
        return

    # Kiểm tra tồn kho hiển thị trước khi thêm mới
    if ui.ton_kho_hienthi.get(id_sp, 0) <= 0:
        QMessageBox.warning(tab, "Lỗi", "Sản phẩm đã hết hàng!")
        return

    # Tạo widget sản phẩm mới nếu chưa có
    item = QWidget()
    item.setFixedHeight(60)
    item.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    item_layout = QHBoxLayout(item)

    # Ảnh sản phẩm
    image_label = QLabel()
    image_path = os.path.join("image", f"{id_sp}.jpg")
    pixmap = QPixmap(image_path)
    if not pixmap.isNull():
        pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
    else:
        image_label.setText("No\nImage")
        image_label.setAlignment(Qt.AlignCenter)

    image_label.setFixedSize(50, 50)

    ten = QLabel(ten_sp)
    ten.setFixedWidth(150)
    ten.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    gia = QLabel(f'{gia_sp:,} đ')
    gia.setStyleSheet("color: green")
    gia.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    btn_giam = QPushButton("-")
    btn_giam.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    so_luong_label = QLabel("1")
    so_luong_label.setFixedWidth(25)
    so_luong_label.setAlignment(Qt.AlignCenter)
    so_luong_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    btn_tang = QPushButton("+")
    btn_tang.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    btn_xoa = QPushButton("✖")
    btn_xoa.setStyleSheet("color: red; font-weight: bold;")
    btn_xoa.setFixedWidth(30)
    btn_xoa.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def xoa_san_pham():
        # Nếu phiếu đã thanh toán thì không cho xóa sản phẩm
        if getattr(tab, "is_paid", False):
            QMessageBox.warning(tab, "Lỗi", "Phiếu đã thanh toán, không thể xóa sản phẩm!")
            return
        # Xoá widget khỏi layout
        item.setParent(None)
        # Xoá khỏi dict
        del tab.products[ten_sp]
        cap_nhat_tong_tien(tab)
        # Tăng lại tồn kho hiển thị
        sl = int(so_luong_label.text())
        ui.ton_kho_hienthi[id_sp] += sl
        update_ton_kho_label(ui, id_sp)
        # Cập nhật lại chiều cao scroll_content
        update_scroll_content_height(tab)

    btn_xoa.clicked.connect(xoa_san_pham)

    def tang_so_luong():
        # Kiểm tra tồn kho hiển thị trước khi tăng
        if ui.ton_kho_hienthi.get(id_sp, 0) <= 0:
            QMessageBox.warning(tab, "Lỗi", "Sản phẩm đã hết hàng!")
            return
        sl = int(so_luong_label.text()) + 1
        so_luong_label.setText(str(sl))
        cap_nhat_tong_tien(tab)
        # Trừ tồn kho hiển thị
        ui.ton_kho_hienthi[id_sp] -= 1
        update_ton_kho_label(ui, id_sp)

    def giam_so_luong():
        sl = int(so_luong_label.text())
        if sl > 1:
            sl -= 1
            so_luong_label.setText(str(sl))
            cap_nhat_tong_tien(tab)
            # Tăng lại tồn kho hiển thị
            ui.ton_kho_hienthi[id_sp] += 1
            update_ton_kho_label(ui, id_sp)

    btn_tang.clicked.connect(tang_so_luong)
    btn_giam.clicked.connect(giam_so_luong)

    item_layout.addWidget(image_label)
    item_layout.addWidget(ten)
    item_layout.addWidget(gia)
    item_layout.addStretch()
    item_layout.addWidget(btn_giam)
    item_layout.addWidget(so_luong_label)
    item_layout.addWidget(btn_tang)
    item_layout.addWidget(btn_xoa) 
    layout.addWidget(item)

    # Lưu vào dict để kiểm tra lần sau, bổ sung id sản phẩm
    tab.products[ten_sp] = {
        "widget": item,
        "so_luong_label": so_luong_label,
        "gia": gia_sp,
        "id": id_sp,
    }

    cap_nhat_tong_tien(tab)
    # Trừ tồn kho hiển thị
    ui.ton_kho_hienthi[id_sp] -= 1
    update_ton_kho_label(ui, id_sp)
    # Cập nhật lại chiều cao scroll_content
    update_scroll_content_height(tab)

def cap_nhat_tong_tien(tab):
    tong = 0
    for sp in tab.products.values():
        gia = sp["gia"]
        sl = int(sp["so_luong_label"].text())
        tong += gia * sl
    tab.tong_tien_label.setText(f"Tổng tiền: {tong:,} đ")


def thanh_toan_phieu(tab):
    id_khach = tab.khach_id_input.text().strip()
    if not id_khach:
        QMessageBox.warning(tab, "Lỗi", "Vui lòng nhập ID khách hàng.")
        return

    # Kiểm tra id_khach có tồn tại trong database không
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM danh_sach_khach_hang WHERE id_khach_hang = %s", (id_khach,))
    khach_exists = cursor.fetchone()
    if not khach_exists:
        cursor.close()
        conn.close()
        QMessageBox.warning(tab, "Lỗi", "ID khách hàng chưa tồn tại. Vui lòng nhập thông tin khách hàng trước khi tạo phiếu hàng!")
        return
    # ---

    tong_text = tab.tong_tien_label.text()
    tong_tien = int(tong_text.split(":")[1].strip().replace(" đ", "").replace(",", ""))
    if tong_tien == 0:
        QMessageBox.warning(tab, "Lỗi", "Phiếu chưa có sản phẩm nào.")
        cursor.close()
        conn.close()
        return

    # Thêm đoạn này để xác nhận
    reply = QMessageBox.question(
        tab,
        "Xác nhận thanh toán",
        f"Hãy đảm bảo khách đã thanh toán số tiền {tong_tien:,} đ?",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply != QMessageBox.Yes:
        cursor.close()
        conn.close()
        return

    ngay_giao_dich = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Tạo id_hoa_don mới
        cursor.execute("SELECT MAX(id_hoa_don) FROM lich_su_hoa_don")
        max_id = cursor.fetchone()[0]
        id_hoa_don = 1 if max_id is None else max_id + 1

        # Thêm vào lich_su_hoa_don
        cursor.execute("""
            INSERT INTO lich_su_hoa_don (id_hoa_don, tong_gia_tri_hoa_don, id_khach_hang, loai_hoa_don, ngay_giao_dich)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_hoa_don, tong_tien, id_khach, "B", ngay_giao_dich))

        # Thêm các sản phẩm vào chi_tiet_hoa_don
        for ten_sp, sp in tab.products.items():
            sl = int(sp["so_luong_label"].text())
            id_sp = get_product_id_by_name(ten_sp)
            if id_sp:
                # Kiểm tra tồn kho
                cursor.execute("SELECT so_luong_ton_kho FROM danh_sach_san_pham WHERE id_san_pham = %s", (id_sp,))
                result = cursor.fetchone()
                if not result:
                    raise Exception(f"Sản phẩm '{ten_sp}' không tồn tại trong kho.")
                ton_kho = result[0]

                if ton_kho < sl:
                    raise Exception(f"Sản phẩm '{ten_sp}' không đủ tồn kho (còn {ton_kho})")

                # Ghi chi tiết hóa đơn
                cursor.execute("""
                    INSERT INTO chi_tiet_hoa_don (id_hoa_don, id_san_pham, so_luong)
                    VALUES (%s, %s, %s)
                """, (id_hoa_don, id_sp, sl))

                # Trừ tồn kho
                cursor.execute("""
                    UPDATE danh_sach_san_pham
                    SET so_luong_ton_kho = so_luong_ton_kho - %s
                    WHERE id_san_pham = %s
                """, (sl, id_sp))

        conn.commit()
        QMessageBox.information(tab, "Thành công", f"Đã lưu hóa đơn {id_hoa_don}")
        # Đánh dấu phiếu đã thanh toán
        tab.is_paid = True

    except Exception as e:
        conn.rollback()
        QMessageBox.critical(tab, "Lỗi", str(e))

    finally:
        cursor.close()
        conn.close()


def get_product_id_by_name(ten_sp):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_san_pham FROM danh_sach_san_pham WHERE ten_san_pham = %s", (ten_sp,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def generate_unique_id():
    while True:
        id_hoa_don = uuid.uuid4().hex[:8].upper()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM lich_su_hoa_don WHERE id_hoa_don = %s", (id_hoa_don,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result[0] == 0:
            return id_hoa_don

import re
import unidecode
from fuzzywuzzy import fuzz

def normalize_text(text):
    """Chuẩn hóa văn bản: xóa dấu, chữ thường, loại bỏ khoảng trắng thừa."""
    text = text.lower()
    text = unidecode.unidecode(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text):
    """Tách từ dựa trên khoảng trắng."""
    return text.split()

def filter_products(ui):
    raw_keyword = ui.search_input.text()
    keyword = normalize_text(raw_keyword)

    if not keyword:
        # Nếu không có từ khóa, hiển thị tất cả sản phẩm
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT sp.id_san_pham, sp.ten_san_pham, sp.gia_san_pham, sp.so_luong_ton_kho, dm.id_danh_muc, dm.ten_danh_muc
            FROM danh_sach_san_pham sp
            JOIN danh_muc_san_pham dm ON sp.id_danh_muc = dm.id_danh_muc
        """)
        all_products = cursor.fetchall()
        cursor.close()
        connection.close()
        load_products_to_scroll_area(ui, all_products)
        return

    keyword_tokens = set(tokenize(keyword))

    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT sp.id_san_pham, sp.ten_san_pham, sp.gia_san_pham, sp.so_luong_ton_kho, dm.id_danh_muc, dm.ten_danh_muc
            FROM danh_sach_san_pham sp
            JOIN danh_muc_san_pham dm ON sp.id_danh_muc = dm.id_danh_muc
        """)
        all_products = cursor.fetchall()

        search_results = []
        for product in all_products:
            product_id, product_name, price, stock, id_danh_muc, ten_danh_muc = product
            normalized_name = normalize_text(product_name)
            name_tokens = set(tokenize(normalized_name))
            normalized_id = normalize_text(str(product_id))

            # So khớp: chỉ cần 1 token trong keyword nằm trong tên sản phẩm
            token_overlap = keyword_tokens & name_tokens
            direct_match = keyword in normalized_name
            fuzzy_match = fuzz.partial_ratio(keyword, normalized_name) >= 70
            id_match = keyword in normalized_id  # Tìm theo id sản phẩm

            if direct_match or fuzzy_match or token_overlap or id_match:
                score = 0
                if id_match:
                    score += 200  # Ưu tiên cao nếu trùng ID
                if direct_match:
                    score += 100
                if token_overlap:
                    score += 80
                score += fuzz.ratio(keyword, normalized_name) * 0.4
                search_results.append((score, product))

        search_results.sort(reverse=True, key=lambda x: x[0])
        filtered_products = [product for score, product in search_results[:20]]
        load_products_to_scroll_area(ui, filtered_products)

    except Exception as e:
        print(f"Lỗi khi tìm kiếm: {str(e)}")
        load_products_to_scroll_area(ui, [])
    finally:
        cursor.close()
        connection.close()

def xuat_phieu_hang(tab):
    # Chỉ cho phép xuất phiếu hàng khi đã thanh toán
    if not getattr(tab, "is_paid", False):
        QMessageBox.warning(tab, "Lỗi", "Bạn chỉ có thể xuất phiếu hàng sau khi đã thanh toán!")
        return

    id_khach = tab.khach_id_input.text().strip()
    if not id_khach:
        QMessageBox.warning(tab, "Lỗi", "Vui lòng nhập ID khách hàng.")
        return

    # Lấy tên khách hàng từ DB
    ten_khach = ""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ten_khach_hang FROM danh_sach_khach_hang WHERE id_khach_hang = %s", (id_khach,))
        result = cursor.fetchone()
        if result:
            ten_khach = result[0]
        cursor.close()
        conn.close()
    except Exception as e:
        ten_khach = ""

    tong_text = tab.tong_tien_label.text()
    tong_tien = int(tong_text.split(":")[1].strip().replace(" đ", "").replace(",", ""))
    if tong_tien == 0:
        QMessageBox.warning(tab, "Lỗi", "Phiếu chưa có sản phẩm nào.")
        return

    # Lấy danh sách sản phẩm
    danh_sach = []
    for ten_sp, sp in tab.products.items():
        so_luong = int(sp["so_luong_label"].text())
        gia = sp["gia"]
        danh_sach.append((ten_sp, so_luong, gia, gia * so_luong))

    # Tạo file PDF
    output_dir = "phieu hang"
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.join(output_dir, f"phieu_hang_{id_khach}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    font_path = os.path.join("Font", "Roboto.ttf")
    font_bold_path = os.path.join("Font", "Roboto-Bold.ttf")
    pdfmetrics.registerFont(TTFont("Roboto", font_path))
    pdfmetrics.registerFont(TTFont("Roboto-Bold", font_bold_path))

    c.setFont("Roboto-Bold", 18)
    c.drawCentredString(width/2, height-50, "PHIẾU HÀNG")

    c.setFont("Roboto", 12)
    c.drawString(50, height-90, f"ID Khách hàng: {id_khach}")
    c.drawString(250, height-90, f"Tên khách hàng: {ten_khach}")
    c.drawString(50, height-130, f"Ngày: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    c.drawString(50, height-150, f"Tổng tiền: {tong_tien:,} đ")

    # Header bảng
    y = height-190
    c.setFont("Roboto-Bold", 12)
    c.drawString(50, y, "Tên SP")
    c.drawString(200, y, "Số lượng")
    c.drawString(300, y, "Giá")
    c.drawString(400, y, "Thành tiền")
    c.setFont("Roboto", 12)
    y -= 20

    for ten, sl, gia, thanh_tien in danh_sach:
        c.drawString(50, y, ten)
        c.drawString(200, y, str(sl))
        c.drawString(300, y, f"{gia:,} đ")
        c.drawString(400, y, f"{thanh_tien:,} đ")
        y -= 20

    c.save()

    # Mở file PDF vừa tạo
    webbrowser.open(os.path.abspath(file_name))
    QMessageBox.information(tab, "Thành công", f"Đã xuất phiếu hàng ra file PDF:\n{file_name}")

def update_ton_kho_label(ui, id_sp):
    """Cập nhật lại label tồn kho cho sản phẩm trên giao diện"""
    grid = ui.danh_sach_san_pham.layout()
    for i in range(grid.count()):
        frame = grid.itemAt(i).widget()
        if hasattr(frame, 'data') and frame.data['id'] == id_sp:
            if hasattr(frame, 'ton_kho_label'):
                frame.ton_kho_label.setText(f"Tồn: {ui.ton_kho_hienthi[id_sp]}")
            break

def update_scroll_content_height(tab):
    layout = getattr(tab, "scroll_layout", None)
    if layout is not None:
        parent = layout.parentWidget()
        count = layout.count()
        # 60 là chiều cao cố định của mỗi item, 5 là padding
        parent.setFixedHeight(count * 60 + 5)

def cap_nhat_danh_sach_san_pham(ui):
    # Lấy danh sách sản phẩm từ DB (lấy cả thông tin danh mục)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sp.id_san_pham, sp.ten_san_pham, sp.gia_san_pham, sp.so_luong_ton_kho, dm.id_danh_muc, dm.ten_danh_muc
        FROM danh_sach_san_pham sp
        JOIN danh_muc_san_pham dm ON sp.id_danh_muc = dm.id_danh_muc
    """)
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    # Tạo dict tồn kho hiển thị mới
    ton_kho_hienthi = {id_sp: ton_kho for id_sp, ten, gia, ton_kho, id_dm, ten_dm in products}

    # Trừ số lượng đã chọn trong các phiếu hàng chưa thanh toán
    for i in range(ui.tab_phieu_hang.count()):
        tab = ui.tab_phieu_hang.widget(i)
        if not getattr(tab, "is_paid", False):
            for sp in getattr(tab, "products", {}).values():
                id_sp = sp.get("id")
                so_luong = int(sp["so_luong_label"].text())
                if id_sp in ton_kho_hienthi:
                    ton_kho_hienthi[id_sp] -= so_luong

    # Gán lại tồn kho hiển thị
    ui.ton_kho_hienthi = ton_kho_hienthi

    # Load lại sản phẩm lên giao diện
    load_products_to_scroll_area(ui, products)

def quet_qr_san_pham(ui):
    cap = cv2.VideoCapture(0)
    found = False
    id_san_pham = None
    window_name = 'Quet QR'
    while not found:
        ret, frame = cap.read()
        if not ret:
            break
        for barcode in decode(frame):
            id_san_pham = barcode.data.decode('utf-8')
            found = True
            break
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
    cap.release()
    cv2.destroyAllWindows()
    if id_san_pham:
        # Tìm sản phẩm trong DB
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_san_pham, ten_san_pham, gia_san_pham, so_luong_ton_kho
            FROM danh_sach_san_pham WHERE id_san_pham = %s
        """, (id_san_pham,))
        sp = cursor.fetchone()
        cursor.close()
        conn.close()
        if sp:
            product_data = {"id": sp[0], "ten": sp[1], "gia": sp[2]}
            add_product_to_current_tab(ui, product_data)
        else:
            # Sửa ở đây: dùng QWidget cha, ví dụ ui nếu là QWidget, hoặc ui.centralwidget, hoặc tab hiện tại
            QMessageBox.warning(ui.parent() if hasattr(ui, 'parent') else None, 
                               "Lỗi", 
                               "Không có trong danh sách sản phẩm, Vui lòng quét lại!")
