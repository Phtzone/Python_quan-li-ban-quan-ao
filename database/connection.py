import mysql.connector
from mysql.connector import Error

def create_connection():
    """Tạo kết nối với MySQL"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",      # Địa chỉ máy chủ MySQL
            user="root",           # Tên người dùng MySQL
            password="111111",     # Mật khẩu MySQL
            database="quan_li_ban_quan_ao"  # Tên database
        )
        print("success")
    except Error as e:
        print(f"Lỗi kết nối đến MySQL: {e}")
    return connection
