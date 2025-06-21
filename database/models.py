from .connection import create_connection

def get_customers():
    """Lấy danh sách khách hàng từ MySQL"""
    connection = create_connection()
    customers = []
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM danh_sach_khach_hang")  # Thay đổi tên bảng nếu cần
        customers = cursor.fetchall()  # Lấy tất cả khách hàng
        cursor.close()
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu khách hàng: {e}")
    finally:
        if connection:
            connection.close()
    return customers

def add_customer(customer_id, name, age, gender, phone, address):
    """Thêm khách hàng vào MySQL"""
    connection = create_connection()
    try:
        cursor = connection.cursor()
        query = "INSERT INTO danh_sach_khach_hang (id_khach_hang, ten_khach_hang, tuoi_khach_hang, gioi_tinh_khach_hang, so_dien_thoai, dia_chi_khach_hang) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (customer_id, name, age, gender, phone, address))
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Lỗi khi thêm khách hàng: {e}")
    finally:
        if connection:
            connection.close()

def delete_customer(customer_id):
    """Xóa khách hàng theo ID"""
    connection = create_connection()
    cursor = connection.cursor()
    query = "DELETE FROM danh_sach_khach_hang WHERE id_khach_hang = %s"
    cursor.execute(query, (customer_id,))
    affected_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()
    return affected_rows

def update_customer(customer_id, name, age, gender, phone, address):
    """Cập nhật thông tin khách hàng"""
    connection = create_connection()
    try:
        cursor = connection.cursor()
        query = """UPDATE danh_sach_khach_hang
                   SET ten_khach_hang = %s, tuoi_khach_hang = %s, gioi_tinh_khach_hang = %s, so_dien_thoai = %s, dia_chi_khach_hang = %s
                   WHERE id_khach_hang = %s"""
        cursor.execute(query, (name, age, gender, phone, address, customer_id))
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Lỗi khi cập nhật khách hàng: {e}")
    finally:
        if connection:
            connection.close()
