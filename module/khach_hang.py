from PySide6.QtWidgets import QTableWidgetItem, QDialog, QVBoxLayout, QLabel, QTableWidget, QMessageBox
from database.models import get_customers
from database.models import add_customer
from database.models import delete_customer
from database.models import update_customer
from database.connection import create_connection
import re
import unidecode
from fuzzywuzzy import fuzz

def display_customers(ui):
    """Hiển thị danh sách khách hàng trong QTableWidget"""
    customers = get_customers()
    ui.tableWidget.setRowCount(len(customers))  # Set number of rows

    # Hiển thị dữ liệu vào bảng
    for row, customer in enumerate(customers):
        ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(customer[0])))  # ID khách hàng
        ui.tableWidget.setItem(row, 1, QTableWidgetItem(customer[1]))  # Tên khách hàng
        ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(customer[2])))  # Tuổi
        ui.tableWidget.setItem(row, 3, QTableWidgetItem(customer[3]))  # giới tính
        ui.tableWidget.setItem(row, 4, QTableWidgetItem(customer[4]))  # địa chỉ
        ui.tableWidget.setItem(row, 5, QTableWidgetItem(customer[5]))  # số điện thoại

    ui.tableWidget.resizeColumnsToContents()  # Tự động điều chỉnh kích thước cột

def add_customer_to_db(ui):
    # Kiểm tra thiếu thông tin trước
    if not (ui.name_line_edit.text().strip() and ui.age_line_edit.text().strip() and ui.phone_line_edit.text().strip() and ui.address_line_edit.text().strip()):
        QMessageBox.warning(ui.add_button, "Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin khách hàng!")
        return

    reply = QMessageBox.question(
        ui.add_button, "Xác nhận", "Bạn có chắc chắn muốn thêm khách hàng này?",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply == QMessageBox.No:
        return

    customer_id = ui.id_line_edit.text()
    name = ui.name_line_edit.text()  # Lấy tên từ line edit
    age = ui.age_line_edit.text()
    gender = ui.gender_line_edit.currentText()
    phone = ui.phone_line_edit.text()  # Lấy số điện thoại
    address = ui.address_line_edit.text()  # Lấy địa chỉ

    add_customer(customer_id, name, age, gender, phone, address)
    display_customers(ui)  # Cập nhật lại bảng sau khi thêm
    clear_line_edit(ui)
    ui.add_button.setEnabled(False)

def update_customer_in_db(ui):
    reply = QMessageBox.question(
        ui.update_button, "Xác nhận", "Bạn có chắc chắn muốn sửa thông tin khách hàng này?",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply == QMessageBox.No:
        return
    customer_id = ui.id_line_edit.text()  # Lấy ID khách hàng cần cập nhật
    name = ui.name_line_edit.text()
    age = ui.age_line_edit.text()
    gender = ui.gender_line_edit.currentText()
    phone = ui.phone_line_edit.text()
    address = ui.address_line_edit.text()

    update_customer(customer_id, name, age, gender, phone, address)
    display_customers(ui)  # Cập nhật lại bảng sau khi sửa
    clear_line_edit(ui)
    ui.add_button.setEnabled(False)

def delete_customer_from_db(ui):
    reply = QMessageBox.question(
        ui.delete_button, "Xác nhận", "Bạn có chắc chắn muốn xóa khách hàng này?",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply == QMessageBox.No:
        return
    customer_id = ui.id_line_edit.text()  # Lấy ID khách hàng cần xóa
    try:
        affected_rows = delete_customer(customer_id)
        if affected_rows == 0:
            QMessageBox.warning(
                ui.delete_button,
                "Không thể xóa",
                "Không thể xóa khách hàng này. Có thể khách hàng không tồn tại hoặc đã phát sinh hóa đơn/dữ liệu liên quan!"
            )
            return
        display_customers(ui)  # Cập nhật lại bảng sau khi xóa
        clear_line_edit(ui)
        ui.add_button.setEnabled(False)
    except Exception as e:
        # Nếu là lỗi ràng buộc khóa ngoại (không xóa được do có hóa đơn liên quan)
        if "1451" in str(e) or "foreign key constraint fails" in str(e).lower():
            QMessageBox.warning(
                ui.delete_button,
                "Không thể xóa",
                "Không thể xóa khách hàng vì đã phát sinh hóa đơn hoặc dữ liệu liên quan!"
            )
        else:
            QMessageBox.critical(
                ui.delete_button,
                "Lỗi",
                f"Lỗi khi xóa khách hàng: {e}"
            )


def show_purchase_history(ui):
    id_text = ui.id_line_edit.text().strip()
    if not id_text.isdigit():
        QMessageBox.warning(ui.add_button, "Lỗi", "ID không hợp lệ.")
        return

    id_khach_hang = int(id_text)
    conn = create_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
            kh.id_khach_hang,
            kh.ten_khach_hang,
            hd.id_hoa_don,
            sp.id_san_pham,
            sp.ten_san_pham,
            ct.so_luong
        FROM danh_sach_khach_hang kh
        JOIN lich_su_hoa_don hd ON kh.id_khach_hang = hd.id_khach_hang
        JOIN chi_tiet_hoa_don ct ON hd.id_hoa_don = ct.id_hoa_don
        JOIN danh_sach_san_pham sp ON ct.id_san_pham = sp.id_san_pham
        WHERE kh.id_khach_hang = %s
    """
    cursor.execute(query, (id_khach_hang,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if not results:
        QMessageBox.information(ui.add_button, "Thông báo", "Khách hàng này chưa từng mua hàng.")
        return

    # Tạo cửa sổ popup
    dialog = QDialog()
    dialog.setWindowTitle("Lịch sử mua hàng")
    layout = QVBoxLayout(dialog)

    table = QTableWidget()
    table.setColumnCount(6)
    table.setHorizontalHeaderLabels([
        "ID KH", "Tên KH", "ID HĐ", "ID SP", "Tên SP", "Số lượng"
    ])
    table.setRowCount(len(results))

    for row_idx, row_data in enumerate(results):
        for col_idx, value in enumerate(row_data):
            table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    clear_line_edit(ui)
    layout.addWidget(table)
    dialog.setLayout(layout)
    dialog.resize(700, 400)
    dialog.exec()


def clear_line_edit(ui):
    ui.id_line_edit.clear()
    ui.name_line_edit.clear()
    ui.age_line_edit.clear()
    ui.gender_line_edit.setCurrentIndex(0)
    ui.phone_line_edit.clear()
    ui.address_line_edit.clear()

def normalize_text(text):
    text = text.lower()
    text = unidecode.unidecode(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text):
    return text.split()


def filter_customers(ui):
    raw_keyword = ui.search_khach_hang.text()
    keyword = normalize_text(raw_keyword)
    if not keyword:
        display_customers(ui)
        return

    keyword_tokens = set(tokenize(keyword))
    customers = get_customers()
    search_results = []
    is_digit = keyword.isdigit()

    for customer in customers:
        id_khach = str(customer[0])
        ten_khach = customer[1]
        so_dien_thoai = customer[5]

        normalized_id = normalize_text(id_khach)
        normalized_name = normalize_text(ten_khach)
        normalized_phone = normalize_text(so_dien_thoai)

        name_tokens = set(tokenize(normalized_name))
        token_overlap = keyword_tokens & name_tokens
        direct_match = keyword in normalized_name
        fuzzy_match = fuzz.partial_ratio(keyword, normalized_name) >= 70
        id_match = keyword in normalized_id
        phone_match = keyword in normalized_phone

        if direct_match or fuzzy_match or token_overlap or id_match or phone_match:
            score = 0
            if id_match:
                score += 200
            if phone_match:
                score += 180
            if direct_match:
                score += 100
            if token_overlap:
                score += 80
            score += fuzz.ratio(keyword, normalized_name) * 0.4
            # Nếu keyword là số và id_khach_hang trùng, tăng điểm thật cao
            if is_digit and id_khach == keyword:
                score += 1000
            search_results.append((score, int(id_khach), customer))

    # Sắp xếp: điểm số giảm dần, nếu bằng nhau thì id_khach_hang tăng dần
    search_results.sort(key=lambda x: (-x[0], x[1]))
    filtered_customers = [customer for score, id_khach, customer in search_results[:20]]

    # Hiển thị kết quả lên bảng
    ui.tableWidget.setRowCount(len(filtered_customers))
    for row, customer in enumerate(filtered_customers):
        ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(customer[0])))
        ui.tableWidget.setItem(row, 1, QTableWidgetItem(customer[1]))
        ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(customer[2])))
        ui.tableWidget.setItem(row, 3, QTableWidgetItem(customer[3]))
        ui.tableWidget.setItem(row, 4, QTableWidgetItem(customer[4]))
        ui.tableWidget.setItem(row, 5, QTableWidgetItem(customer[5]))
    ui.tableWidget.resizeColumnsToContents()

def generate_new_customer_id():
    customers = get_customers()
    if not customers:
        return 1
    max_id = max(int(c[0]) for c in customers)
    return max_id + 1


def handle_them_khach_moi(ui):
    new_id = generate_new_customer_id()
    ui.id_line_edit.setText(str(new_id))
    ui.name_line_edit.clear()
    ui.age_line_edit.clear()
    ui.gender_line_edit.setCurrentIndex(0)
    ui.phone_line_edit.clear()
    ui.address_line_edit.clear()
    ui.add_button.setEnabled(True)

def on_customer_row_selected(ui):
    selected_row = ui.tableWidget.currentRow()
    if selected_row < 0:
        return
    ui.id_line_edit.setText(ui.tableWidget.item(selected_row, 0).text())
    ui.name_line_edit.setText(ui.tableWidget.item(selected_row, 1).text())
    ui.age_line_edit.setText(ui.tableWidget.item(selected_row, 2).text())
    gender = ui.tableWidget.item(selected_row, 3).text()
    index = ui.gender_line_edit.findText(gender)
    if index >= 0:
        ui.gender_line_edit.setCurrentIndex(index)
    ui.address_line_edit.setText(ui.tableWidget.item(selected_row, 4).text())
    ui.phone_line_edit.setText(ui.tableWidget.item(selected_row, 5).text())
    ui.add_button.setEnabled(False)
