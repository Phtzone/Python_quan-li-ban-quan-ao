from PySide6.QtWidgets import QTableWidgetItem, QDialog, QVBoxLayout, QTableWidget
from PySide6.QtCore import QDate

from database.connection import create_connection



def load_all_hoa_don(ui):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_hoa_don, tong_gia_tri_hoa_don, id_khach_hang, loai_hoa_don, ngay_giao_dich FROM lich_su_hoa_don")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    table = ui.table_hoa_don
    table.setRowCount(len(data))
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["ID", "Tổng tiền", "Khách hàng", "Loại", "Ngày tạo"])

    for row, (id_hd, tong, id_kh, loai, ngay) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem(str(id_hd)))
        table.setItem(row, 1, QTableWidgetItem(f"{tong:,} đ"))
        table.setItem(row, 2, QTableWidgetItem(str(id_kh)))
        table.setItem(row, 3, QTableWidgetItem("Mua" if loai == "M" else "Bán"))
        table.setItem(row, 4, QTableWidgetItem(ngay.strftime("%Y-%m-%d %H:%M:%S")))


def show_hoa_don_in_range(ui):
    from_date = ui.from_date_edit.date().toPython()
    to_date = ui.to_date_edit.date().toPython()

    dialog = QDialog()
    from_str = from_date.strftime("%d/%m/%Y")
    to_str = to_date.strftime("%d/%m/%Y")

    dialog.setWindowTitle(f"Hóa đơn từ {from_str} đến {to_str}")
    layout = QVBoxLayout(dialog)

    table = QTableWidget()
    layout.addWidget(table)

    conn = create_connection()
    cursor = conn.cursor()
    query = """
        SELECT id_hoa_don, tong_gia_tri_hoa_don, id_khach_hang, loai_hoa_don, ngay_giao_dich
        FROM lich_su_hoa_don
        WHERE DATE(ngay_giao_dich) BETWEEN %s AND %s
    """
    cursor.execute(query, (from_date, to_date))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    table.setRowCount(len(data))
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["ID", "Tổng tiền", "Khách hàng", "Loại", "Ngày giao dịch"])

    for row, (id_hd, tong, id_kh, loai, ngay) in enumerate(data):
        table.setItem(row, 0, QTableWidgetItem(str(id_hd)))
        table.setItem(row, 1, QTableWidgetItem(f"{tong:,} đ"))
        table.setItem(row, 2, QTableWidgetItem(str(id_kh)))
        table.setItem(row, 3, QTableWidgetItem("Mua" if loai == "M" else "Bán"))
        table.setItem(row, 4, QTableWidgetItem(ngay.strftime("%Y-%m-%d %H:%M:%S")))

    dialog.resize(700, 400)
    dialog.exec()


def sort_hoa_don(ui, tang_dan=True):
    table = ui.table_hoa_don
    rows = []

    for row in range(table.rowCount()):
        tong_text = table.item(row, 1).text().replace(" đ", "").replace(",", "")
        tong = int(tong_text)
        row_data = [table.item(row, col).text() for col in range(5)]
        rows.append((tong, row_data))

    rows.sort(reverse=not tang_dan)

    table.setRowCount(0)
    table.setRowCount(len(rows))
    for row, (_, row_data) in enumerate(rows):
        for col, val in enumerate(row_data):
            table.setItem(row, col, QTableWidgetItem(val))


def show_hoa_don_detail(ui):
    selected_row = ui.table_hoa_don.currentRow()
    if selected_row < 0:
        return
    id_hoa_don = ui.table_hoa_don.item(selected_row, 0).text()

    conn = create_connection()
    cursor = conn.cursor()
    # Lấy thông tin hóa đơn
    cursor.execute(
        "SELECT id_hoa_don, tong_gia_tri_hoa_don, id_khach_hang, loai_hoa_don, ngay_giao_dich FROM lich_su_hoa_don WHERE id_hoa_don = %s",
        (id_hoa_don,)
    )
    hoa_don = cursor.fetchone()
    # Lấy chi tiết sản phẩm trong hóa đơn (nếu có bảng chi tiết)
    cursor.execute(
        """SELECT sp.ten_san_pham, ct.so_luong
        FROM chi_tiet_hoa_don ct
        JOIN danh_sach_san_pham sp ON ct.id_san_pham = sp.id_san_pham
        WHERE ct.id_hoa_don = %s""", (id_hoa_don,)
    )
    chi_tiet = cursor.fetchall()
    cursor.close()
    conn.close()

    # Hiển thị popup chi tiết
    dialog = QDialog()
    dialog.setWindowTitle(f"Chi tiết hóa đơn #{id_hoa_don}")
    layout = QVBoxLayout(dialog)

    # Thông tin hóa đơn
    info = f"""<b>ID:</b> {hoa_don[0]}<br>
    <b>Tổng tiền:</b> {hoa_don[1]:,} đ<br>
    <b>Khách hàng:</b> {hoa_don[2]}<br>
    <b>Loại:</b> {'Mua' if hoa_don[3]=='M' else 'Bán'}<br>
    <b>Ngày tạo:</b> {hoa_don[4].strftime('%Y-%m-%d %H:%M:%S')}<br>"""
    from PySide6.QtWidgets import QLabel
    layout.addWidget(QLabel(info))

    # Bảng chi tiết sản phẩm
    if chi_tiet:
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Sản phẩm', 'Số lượng'])
        table.setRowCount(len(chi_tiet))
        for row, (ten_sp, so_luong) in enumerate(chi_tiet):
            table.setItem(row, 0, QTableWidgetItem(str(ten_sp)))
            table.setItem(row, 1, QTableWidgetItem(str(so_luong)))
        layout.addWidget(table)

    dialog.setLayout(layout)
    dialog.resize(500, 400)
    dialog.exec()
