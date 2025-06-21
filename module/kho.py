from database.connection import create_connection  # Import hàm tạo kết nối từ connection.py
from mysql.connector import Error
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from datetime import datetime

import os
import shutil

from table_item import NumericTableWidgetItem


def hien_thi_danh_sach_san_pham(ui):
    """
    Truy vấn danh sách sản phẩm từ MySQL và hiển thị trong QTableWidget.
    :param table_widget: QTableWidget đã được tạo trong UI
    """
    # Tạo kết nối
    connection = create_connection()
    if connection is None:
        print("Không thể kết nối tới MySQL.")
        return

    try:
        cursor = connection.cursor()
        # Truy vấn lấy danh sách sản phẩm
        cursor.execute("""
            SELECT id_san_pham, ten_san_pham, id_danh_muc, gia_san_pham, 
                   so_luong_ton_kho, mo_ta_san_pham, gia_nhap_san_pham 
            FROM danh_sach_san_pham
        """)
        
        # Lấy tất cả kết quả từ truy vấn
        result = cursor.fetchall()
        
        # Đặt số lượng dòng và cột trong QTableWidget
        ui.kho_table_widget.setRowCount(len(result))  # Số dòng bằng số kết quả truy vấn
        ui.kho_table_widget.setColumnCount(7)  # Cột gồm 7 thuộc tính từ bảng danh_sach_san_pham
        
        # Đặt tiêu đề cho các cột (có thể thay đổi tùy theo bảng của bạn)
        ui.kho_table_widget.setHorizontalHeaderLabels([
            "ID Sản Phẩm", "Tên Sản Phẩm", "ID Danh Mục", "Giá Sản Phẩm", 
            "Số Lượng Tồn Kho", "Mô Tả Sản Phẩm", "Giá Nhập Sản Phẩm"
        ])
        
        # Hiển thị kết quả vào từng ô trong bảng
        for row_num, row_data in enumerate(result):
            for col_num, value in enumerate(row_data):
                if col_num == 4:  # Cột "Số Lượng Tồn Kho"
                    ui.kho_table_widget.setItem(row_num, col_num, NumericTableWidgetItem(str(value)))
                else:
                    ui.kho_table_widget.setItem(row_num, col_num, QTableWidgetItem(str(value)))

                
    except Error as e:
        print(f"Lỗi MySQL: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def handle_update_product(ui):
    id_sp = ui.kho_chinh_sua_id_san_pham_line_edit.text()
    ten_sp = ui.kho_chinh_sua_ten_san_pham_line_edit.text()
    id_danh_muc = ui.kho_chinh_sua_id_danh_muc_combobox.currentData()
    gia_sp = ui.kho_chinh_sua_gia_san_pham_line_edit.text()
    so_luong = ui.kho_chinh_sua_so_luong_ton_kho_line_edit.text()
    mo_ta = ui.kho_chinh_sua_mo_ta_san_pham_line_edit.text()
    image_label = ui.kho_chinh_sua_image_drop_label  # label kéo thả ảnh

    # Cập nhật thông tin sản phẩm trong MySQL
    from database.connection import create_connection
    conn = create_connection()
    cursor = conn.cursor()
    query = """
        UPDATE danh_sach_san_pham
        SET ten_san_pham=%s, id_danh_muc=%s, gia_san_pham=%s,
            so_luong_ton_kho=%s, mo_ta_san_pham=%s
        WHERE id_san_pham=%s
    """
    cursor.execute(query, (ten_sp, id_danh_muc, gia_sp, so_luong, mo_ta, id_sp))
    conn.commit()

    # Nếu có ảnh mới thì sao chép vào folder image/
    if image_label.image_path:
        image_folder = os.path.join(os.getcwd(), "image")
        os.makedirs(image_folder, exist_ok=True)
        new_image_path = os.path.join(image_folder, f"{id_sp}.jpg")
        shutil.copy(image_label.image_path, new_image_path)
        print(f"Đã cập nhật ảnh: {new_image_path}")

    QMessageBox.information(ui.centralwidget, "Thành công", "Đã cập nhật sản phẩm!")


def load_danh_muc_vao_combobox(ui):
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT id_danh_muc, ten_danh_muc FROM danh_muc_san_pham"
    cursor.execute(query)
    results = cursor.fetchall()

    combo = ui.kho_chinh_sua_id_danh_muc_combobox
    combo.clear()

    for id_danh_muc, ten_danh_muc in results:
        display_text = f"{id_danh_muc} : {ten_danh_muc}"
        # Hiển thị tên, lưu id
        combo.addItem(display_text, userData=id_danh_muc)

    cursor.close()
    conn.close()

def on_kho_table_row_selected(ui):
    ui.kho_chinh_sua_so_luong_ton_kho_line_edit.setDisabled(False)
    ui.kho_xoa_san_pham_button.setEnabled(True)


def on_kho_row_selected(ui):
    selected_items = ui.kho_table_widget.selectedItems()
    if not selected_items:
        return

    row = selected_items[0].row()

    id_san_pham = ui.kho_table_widget.item(row, 0).text()
    ten_san_pham = ui.kho_table_widget.item(row, 1).text()
    gia_san_pham = ui.kho_table_widget.item(row, 3).text()
    so_luong = ui.kho_table_widget.item(row, 4).text()
    mo_ta = ui.kho_table_widget.item(row, 5).text()
    id_danh_muc = int(ui.kho_table_widget.item(row, 2).text())

    current_tab = ui.kho_stackedWidget.currentIndex()

    if current_tab == 0:
        # Gán vào các line edit trong tab CHỈNH SỬA
        ui.kho_chinh_sua_id_san_pham_line_edit.setText(id_san_pham)
        ui.kho_chinh_sua_ten_san_pham_line_edit.setText(ten_san_pham)
        ui.kho_chinh_sua_gia_san_pham_line_edit.setText(gia_san_pham)
        ui.kho_chinh_sua_so_luong_ton_kho_line_edit.setText(so_luong)
        ui.kho_chinh_sua_mo_ta_san_pham_line_edit.setText(mo_ta)

        for i in range(ui.kho_chinh_sua_id_danh_muc_combobox.count()):
            if ui.kho_chinh_sua_id_danh_muc_combobox.itemData(i) == id_danh_muc:
                ui.kho_chinh_sua_id_danh_muc_combobox.setCurrentIndex(i)
                break

        # Hiển thị hình ảnh
        image_path = f"image/{id_san_pham}.jpg"
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            ui.kho_chinh_sua_image_drop_label.setPixmap(pixmap.scaled(
                ui.kho_chinh_sua_image_drop_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            ui.kho_chinh_sua_image_drop_label.clear()

    elif current_tab == 1:
        # Gán vào các line edit trong tab NHẬP HÀNG
        ui.kho_nhap_hang_id_san_pham_line_edit.setText(id_san_pham)
        ui.kho_nhap_hang_ten_san_pham_line_edit.setText(ten_san_pham)
        ui.kho_nhap_hang_so_luong_ton_kho_line_edit.setText(so_luong)

    # Hiển thị hình ảnh
        image_path = f"image/{id_san_pham}.jpg"
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            ui.kho_nhap_hang_image_drop_label.setPixmap(pixmap.scaled(
                ui.kho_nhap_hang_image_drop_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            ui.kho_nhap_hang_image_drop_label.clear()


def xoa_san_pham(ui):
    selected_items = ui.kho_table_widget.selectedItems()
    if not selected_items:
        QMessageBox.warning(ui, "Lỗi", "Vui lòng chọn một sản phẩm để xóa.")
        return

    selected_row = selected_items[0].row()
    id_san_pham = int(ui.kho_table_widget.item(selected_row, 0).text())

    confirm = QMessageBox.question(ui.centralwidget, "Xác nhận", f"Bạn có chắc muốn xóa sản phẩm ID {id_san_pham}?",
                                   QMessageBox.Yes | QMessageBox.No)
    if confirm != QMessageBox.Yes:
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM danh_sach_san_pham WHERE id_san_pham = %s", (id_san_pham,))
        conn.commit()

        # Xóa ảnh nếu có
        image_path = f"image/{id_san_pham}.jpg"
        if os.path.exists(image_path):
            os.remove(image_path)

        QMessageBox.information(ui.centralwidget, "Thành công", "Đã xóa sản phẩm.")
        ui.kho_xoa_san_pham_button.setEnabled(False)

    except Exception as e:
        QMessageBox.critical(ui.centralwidget, "Lỗi", str(e))
    finally:
        conn.close()

def chuan_bi_them_moi_san_pham(ui):
    # Lấy id_san_pham mới nhất
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id_san_pham) FROM danh_sach_san_pham")
    max_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    next_id = 1 if max_id is None else max_id + 1

    # Reset các ô nhập
    ui.kho_chinh_sua_id_san_pham_line_edit.setText(str(next_id))
    ui.kho_chinh_sua_ten_san_pham_line_edit.clear()
    ui.kho_chinh_sua_id_danh_muc_combobox.setCurrentIndex(0)
    ui.kho_chinh_sua_gia_san_pham_line_edit.clear()
    ui.kho_chinh_sua_so_luong_ton_kho_line_edit.clear()
    ui.kho_chinh_sua_mo_ta_san_pham_line_edit.clear()
    ui.kho_chinh_sua_image_drop_label.clear_image()

    # ❌ Vô hiệu hóa ô nhập số lượng tồn kho
    ui.kho_chinh_sua_so_luong_ton_kho_line_edit.setDisabled(True)

    # Chuyển sang tab chỉnh sửa
    ui.kho_stackedWidget.setCurrentWidget(ui.kho_chinh_sua_page)

def luu_san_pham_moi(ui):
    id_sp = ui.kho_chinh_sua_id_san_pham_line_edit.text()
    ten_sp = ui.kho_chinh_sua_ten_san_pham_line_edit.text()
    id_danh_muc = ui.kho_chinh_sua_id_danh_muc_combobox.currentData()
    gia_sp = ui.kho_chinh_sua_gia_san_pham_line_edit.text()
    so_luong = ui.kho_chinh_sua_so_luong_ton_kho_line_edit.text()
    mo_ta = ui.kho_chinh_sua_mo_ta_san_pham_line_edit.text()
    image_label = ui.kho_chinh_sua_image_drop_label

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO danh_sach_san_pham (id_san_pham, ten_san_pham, id_danh_muc, gia_san_pham, mo_ta_san_pham)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_sp, ten_sp, id_danh_muc, gia_sp, mo_ta))
        conn.commit()

        # Sao chép ảnh nếu có
        if image_label.image_path:
            image_folder = os.path.join(os.getcwd(), "image")
            os.makedirs(image_folder, exist_ok=True)
            new_image_path = os.path.join(image_folder, f"{id_sp}.jpg")
            shutil.copy(image_label.image_path, new_image_path)

        QMessageBox.information(ui.centralwidget, "Thành công", f"Đã thêm sản phẩm ID {id_sp}")
        hien_thi_danh_sach_san_pham(ui)

    except Exception as e:
        QMessageBox.critical(ui.centralwidget, "Lỗi", str(e))

    finally:
        cursor.close()
        conn.close()

def sap_xep_theo_so_luong_ton_kho(ui):
    # Giả sử cột số lượng tồn kho là cột 3
    ui.kho_table_widget.sortItems(4, Qt.AscendingOrder)


# def cap_nhat_combobox_de_xuat(ui):
#     ui.kho_nhap_hang_de_xuat_combobox.clear()
    
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT id_san_pham, ten_san_pham, so_luong_ton_kho
#         FROM danh_sach_san_pham
#         WHERE so_luong_ton_kho < 10
#         ORDER BY so_luong_ton_kho ASC
#     """)
#     for id_sp, ten_sp, sl in cursor.fetchall():
#         hien_thi = f"{id_sp} : {ten_sp} ({sl})"
#         ui.kho_nhap_hang_de_xuat_combobox.addItem(hien_thi, id_sp)
    
#     cursor.close()
#     conn.close()

# def on_combobox_de_xuat_changed(ui):
#     id_sp = ui.kho_nhap_hang_de_xuat_combobox.currentData()
#     if not id_sp:
#         return

#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT ten_san_pham, so_luong_ton_kho
#         FROM danh_sach_san_pham
#         WHERE id_san_pham = %s
#     """, (id_sp,))
#     row = cursor.fetchone()
#     if row:
#         ten_sp, sl_ton = row
#         ui.kho_nhap_hang_id_san_pham_line_edit.setText(str(id_sp))
#         ui.kho_nhap_hang_ten_san_pham_line_edit.setText(ten_sp)
#         ui.kho_nhap_hang_so_luong_ton_kho_line_edit.setText(str(sl_ton))
#         # Load ảnh
#         image_path = os.path.join("image", f"{id_sp}.jpg")
#         if os.path.exists(image_path):
#             ui.kho_nhap_hang_image_drop_label.setPixmap(QPixmap(image_path).scaledToWidth(200))
#     cursor.close()
#     conn.close()

def nhap_them_so_luong_hang(ui):
    try:
        id_sp = ui.kho_nhap_hang_id_san_pham_line_edit.text()
        so_luong_hien_tai = int(ui.kho_nhap_hang_so_luong_ton_kho_line_edit.text())
        so_luong_nhap_them = int(ui.kho_nhap_hang_so_luong_nhap_them_line_edit.text())
        gia_nhap_moi = float(ui.kho_nhap_hang_gia_nhap_san_pham_line_edit.text())

        if so_luong_nhap_them <= 0:
            QMessageBox.warning(ui.centralwidget, "Cảnh báo", "Số lượng nhập thêm phải lớn hơn 0.")
            return

        so_luong_moi = so_luong_hien_tai + so_luong_nhap_them

        conn = create_connection()
        cursor = conn.cursor()

        # 🔍 Lấy giá nhập hiện tại của sản phẩm
        cursor.execute("SELECT gia_nhap_san_pham FROM danh_sach_san_pham WHERE id_san_pham = %s", (id_sp,))
        result = cursor.fetchone()
        gia_nhap_hien_tai = result[0] if result and result[0] is not None else 0

        # 📊 Tính giá nhập trung bình mới
        tong_gia_tri_hien_tai = so_luong_hien_tai * gia_nhap_hien_tai
        tong_gia_tri_nhap_them = so_luong_nhap_them * gia_nhap_moi
        gia_nhap_trung_binh = (tong_gia_tri_hien_tai + tong_gia_tri_nhap_them) / so_luong_moi

        tong_gia_tri = tong_gia_tri_nhap_them

        # ✅ 1. Cập nhật lại số lượng và giá nhập trung bình
        cursor.execute("""
            UPDATE danh_sach_san_pham
            SET so_luong_ton_kho = %s,
                gia_nhap_san_pham = %s
            WHERE id_san_pham = %s
        """, (so_luong_moi, gia_nhap_trung_binh, id_sp))

        # ✅ 2. Tạo hóa đơn mới
        cursor.execute("SELECT MAX(id_hoa_don) FROM lich_su_hoa_don")
        result = cursor.fetchone()
        max_id = result[0] if result[0] is not None else 0
        id_hoa_don = max_id + 1

        ngay_giao_dich = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        loai_hoa_don = 'M'
        id_khach_hang = 0  # Nhập hàng = 0

        cursor.execute("""
            INSERT INTO lich_su_hoa_don (id_hoa_don, tong_gia_tri_hoa_don, id_khach_hang, loai_hoa_don, ngay_giao_dich)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_hoa_don, tong_gia_tri, id_khach_hang, loai_hoa_don, ngay_giao_dich))

        # ✅ 3. Chi tiết hóa đơn
        cursor.execute("""
            INSERT INTO chi_tiet_hoa_don (id_hoa_don, id_san_pham, so_luong)
            VALUES (%s, %s, %s)
        """, (id_hoa_don, id_sp, so_luong_nhap_them))

        conn.commit()
        cursor.close()
        conn.close()

        QMessageBox.information(ui.centralwidget, "Thành công", "Đã nhập hàng và lưu vào lịch sử hóa đơn.")

        # Cập nhật giao diện
        ui.kho_nhap_hang_so_luong_ton_kho_line_edit.setText(str(so_luong_moi))
        ui.kho_nhap_hang_so_luong_nhap_them_line_edit.clear()
        hien_thi_danh_sach_san_pham(ui)

    except Exception as e:
        QMessageBox.critical(ui.centralwidget, "Lỗi", str(e))

