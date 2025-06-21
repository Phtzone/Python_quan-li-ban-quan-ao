from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QComboBox, QLabel, QPushButton, QVBoxLayout, QTableWidget, QDialog, QGridLayout, QLineEdit, QFrame
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os
from database.connection import create_connection
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def get_hoa_don_by_month_year(thang, nam):
    """Lấy dữ liệu hóa đơn theo tháng và năm"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = """
            SELECT id_hoa_don, tong_gia_tri_hoa_don, id_khach_hang, loai_hoa_don, ngay_giao_dich 
            FROM lich_su_hoa_don
            WHERE MONTH(ngay_giao_dich) = %s AND YEAR(ngay_giao_dich) = %s
        """
        cursor.execute(query, (thang, nam))
        data = cursor.fetchall()
        
        # Chuyển kết quả thành DataFrame
        df = pd.DataFrame(data, columns=['id_hoa_don', 'tong_gia_tri', 'id_khach_hang', 'loai_hoa_don', 'ngay_giao_dich'])
        
        cursor.close()
        return df
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu hóa đơn: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def tinh_tong_doanh_thu(thang, nam):
    """Tính tổng doanh thu theo tháng và năm"""
    df = get_hoa_don_by_month_year(thang, nam)
    
    if df.empty:
        return 0
    
    # Chỉ tính doanh thu từ hóa đơn bán (loại B)
    df_ban = df[df['loai_hoa_don'] == 'B']
    
    return df_ban['tong_gia_tri'].sum() if not df_ban.empty else 0

def tinh_doanh_thu_thang_hien_tai(thang, nam):
    """Tính doanh thu tháng hiện tại"""
    return tinh_tong_doanh_thu(thang, nam)

def tinh_tong_san_pham_ban_ra(thang, nam):
    """Tính tổng số sản phẩm đã bán trong tháng và năm"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = """
            SELECT SUM(so_luong) AS tong_so_luong
            FROM chi_tiet_hoa_don
            JOIN lich_su_hoa_don ON chi_tiet_hoa_don.id_hoa_don = lich_su_hoa_don.id_hoa_don
            WHERE MONTH(ngay_giao_dich) = %s AND YEAR(ngay_giao_dich) = %s AND loai_hoa_don = 'B'
        """
        cursor.execute(query, (thang, nam))
        result = cursor.fetchone()
        cursor.close()
        
        return result[0] if result[0] else 0
    except Exception as e:
        print(f"Lỗi khi tính tổng sản phẩm bán ra: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def tinh_loi_nhuan_thang(thang, nam):
    """Tính lợi nhuận trong tháng dựa trên giá bán - giá nhập từng sản phẩm"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = """
            SELECT SUM(
                cthd.so_luong * (sp.gia_san_pham - IFNULL(sp.gia_nhap_san_pham, 0))
            )
            FROM chi_tiet_hoa_don cthd
            JOIN lich_su_hoa_don lshd ON cthd.id_hoa_don = lshd.id_hoa_don
            JOIN danh_sach_san_pham sp ON cthd.id_san_pham = sp.id_san_pham
            WHERE lshd.loai_hoa_don = 'B'
              AND MONTH(lshd.ngay_giao_dich) = %s
              AND YEAR(lshd.ngay_giao_dich) = %s
        """
        cursor.execute(query, (thang, nam))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result[0] else 0
    except Exception as e:
        print(f"Lỗi khi tính lợi nhuận: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def tinh_tong_doanh_thu_nam(nam):
    """Tính tổng doanh thu của cả năm"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = """
            SELECT SUM(tong_gia_tri_hoa_don)
            FROM lich_su_hoa_don
            WHERE YEAR(ngay_giao_dich) = %s AND loai_hoa_don = 'B'
        """
        cursor.execute(query, (nam,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result[0] else 0
    except Exception as e:
        print(f"Lỗi khi tính tổng doanh thu năm: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def tinh_tang_truong_doanh_thu(thang, nam):
    """Tính phần trăm tăng trưởng doanh thu so với tháng trước"""
    if thang == 1:
        thang_truoc = 12
        nam_truoc = nam - 1
    else:
        thang_truoc = thang - 1
        nam_truoc = nam

    doanh_thu_hien_tai = tinh_doanh_thu_thang_hien_tai(thang, nam)
    doanh_thu_thang_truoc = tinh_doanh_thu_thang_hien_tai(thang_truoc, nam_truoc)

    if doanh_thu_thang_truoc == 0:
        return None  # Không có dữ liệu tháng trước

    ty_le = (doanh_thu_hien_tai - doanh_thu_thang_truoc) / doanh_thu_thang_truoc * 100
    return ty_le

def tinh_tong_chi_thang(thang, nam):
    """Tính tổng chi phí (mua hàng) trong tháng và năm"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = """
            SELECT SUM(tong_gia_tri_hoa_don)
            FROM lich_su_hoa_don
            WHERE MONTH(ngay_giao_dich) = %s AND YEAR(ngay_giao_dich) = %s AND loai_hoa_don = 'M'
        """
        cursor.execute(query, (thang, nam))
        tong_chi = cursor.fetchone()[0] or 0
        cursor.close()
        return tong_chi
    except Exception as e:
        print(f"Lỗi khi tính tổng chi tháng: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def cap_nhat_thong_ke_bao_cao(ui, thang, nam):
    """Cập nhật các thông tin thống kê lên giao diện báo cáo"""
    # Tính toán các giá trị thống kê
    tong_doanh_thu = tinh_tong_doanh_thu_nam(nam)  # Tổng doanh thu cả năm
    doanh_thu_thang = tinh_doanh_thu_thang_hien_tai(thang, nam)
    tong_san_pham = tinh_tong_san_pham_ban_ra(thang, nam)
    tong_loi_nhuan = tinh_loi_nhuan_thang(thang, nam)
    tong_chi_thang = tinh_tong_chi_thang(thang, nam)  # Tổng chi tháng hiện tại
    
    # Hiển thị lên giao diện
    ui.tong_doanh_thu_label.setText(f"{tong_doanh_thu:,} đ")
    ui.doanh_thu_thang_label.setText(f"{doanh_thu_thang:,} đ")
    ui.tong_san_pham_label.setText(str(tong_san_pham))
    ui.tong_loi_nhuan_label.setText(f"{tong_loi_nhuan:,} đ")
    ui.tong_chi_thang_label.setText(f"{tong_chi_thang:,} đ")

    # Hiển thị tăng trưởng doanh thu so với tháng trước
    ty_le = tinh_tang_truong_doanh_thu(thang, nam)
    if hasattr(ui, 'so_voi_thang_truoc_label'):
        if ty_le is None:
            ui.so_voi_thang_truoc_label.setText("Không có dữ liệu")
        elif ty_le >= 0:
            ui.so_voi_thang_truoc_label.setText(f"<span style='color:green;font-weight:bold'>Tăng +{ty_le:.1f}%</span>")
        else:
            ui.so_voi_thang_truoc_label.setText(f"<span style='color:red;font-weight:bold'>Giảm {ty_le:.1f}%</span>")

def ve_bieu_do_doanh_thu(ui, thang, nam, for_export=False):
    conn = create_connection()
    if for_export:
        fig = Figure(figsize=(7, 4), dpi=100)  # Rộng hơn khi xuất PDF
    else:
        fig = Figure(figsize=(4, 4), dpi=100)  # Kích thước mặc định cho giao diện
    try:
        cursor = conn.cursor()
        query = """
            SELECT DAY(ngay_giao_dich) as ngay, SUM(tong_gia_tri_hoa_don) as doanh_thu
            FROM lich_su_hoa_don
            WHERE MONTH(ngay_giao_dich) = %s AND YEAR(ngay_giao_dich) = %s AND loai_hoa_don = 'B'
            GROUP BY DAY(ngay_giao_dich)
            ORDER BY ngay
        """
        cursor.execute(query, (thang, nam))
        data = cursor.fetchall()
        cursor.close()
        if not for_export:
            for i in reversed(range(ui.bieu_do_layout.count())): 
                ui.bieu_do_layout.itemAt(i).widget().setParent(None)
        if not data:
            canvas = FigureCanvas(fig)
            if not for_export:
                ui.bieu_do_layout.addWidget(canvas)
            ax = fig.add_subplot(111)
            ax.set_title(f'Không có dữ liệu doanh thu - Tháng {thang}/{nam}')
            ax.set_xlabel('Ngày')
            ax.set_ylabel('Doanh thu (VNĐ)')
            ax.grid(True, linestyle='--', alpha=0.7)
            canvas.draw()
            return fig
        df = pd.DataFrame(data, columns=['ngay', 'doanh_thu'])
        import calendar
        so_ngay = calendar.monthrange(nam, thang)[1]
        ngay_chuan = list(range(1, so_ngay+1, 5))
        if so_ngay not in ngay_chuan:
            ngay_chuan.append(so_ngay)

        canvas = FigureCanvas(fig)
        if not for_export:
            ui.bieu_do_layout.addWidget(canvas)
        ax = fig.add_subplot(111)
        ax.bar(df['ngay'], df['doanh_thu'], color='skyblue')
        ax.set_title(f'Doanh thu theo ngày - Tháng {thang}/{nam}')
        ax.set_xlabel('Ngày')
        ax.set_ylabel('Doanh thu (VNĐ)')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
        )
        ax.set_xticks(ngay_chuan)
        fig.subplots_adjust(left=0.18)
        canvas.draw()
        return fig
    except Exception as e:
        print(f"Lỗi khi vẽ biểu đồ doanh thu: {e}")
        return fig
    finally:
        if conn:
            conn.close()

def xuat_bao_cao_excel(thang, nam):
    """Xuất báo cáo ra file Excel"""
    try:
        # Lấy dữ liệu hóa đơn
        df_hoa_don = get_hoa_don_by_month_year(thang, nam)
        
        if df_hoa_don.empty:
            return False, "Không có dữ liệu hóa đơn trong tháng này"
        
        # Chuyển cột ngày về datetime (nếu có)
        if 'ngay_giao_dich' in df_hoa_don.columns:
            df_hoa_don['ngay_giao_dich'] = pd.to_datetime(df_hoa_don['ngay_giao_dich'])
        
        # Tạo thư mục báo cáo nếu chưa tồn tại
        if not os.path.exists("bao_cao"):
            os.makedirs("bao_cao")
        
        # Tạo tên file báo cáo
        file_name = f"bao_cao/bao_cao_thang_{thang}_{nam}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Tạo writer để ghi file Excel
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            # Ghi dữ liệu hóa đơn
            df_hoa_don.to_excel(writer, sheet_name='Hoa_Don', index=False)
            # Tự động điều chỉnh độ rộng cột
            worksheet = writer.sheets['Hoa_Don']
            for column_cells in worksheet.columns:
                max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = max_length + 2
            
            # Tạo trang tổng kết
            tong_doanh_thu = tinh_tong_doanh_thu(thang, nam)
            tong_sp_ban = tinh_tong_san_pham_ban_ra(thang, nam)
            tong_loi_nhuan = tinh_loi_nhuan_thang(thang, nam)
            
            df_tong_ket = pd.DataFrame({
                'Chỉ số': ['Tổng doanh thu', 'Tổng sản phẩm bán ra', 'Tổng lợi nhuận'],
                'Giá trị': [tong_doanh_thu, tong_sp_ban, tong_loi_nhuan]
            })
            
            df_tong_ket.to_excel(writer, sheet_name='Tong_Ket', index=False)
            
            worksheet2 = writer.sheets['Tong_Ket']
            for column_cells in worksheet2.columns:
                max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
                worksheet2.column_dimensions[column_cells[0].column_letter].width = max_length + 2
            
        return True, file_name
    except Exception as e:
        print(f"Lỗi khi xuất báo cáo Excel: {e}")
        return False, str(e)


def load_san_pham_theo_thang(ui, thang, nam):
    # Đã bỏ bảng, không làm gì cả
    return True

def tao_thong_ke_theo_loai_hoa_don(ui, thang, nam, for_export=False):
    conn = create_connection()
    fig = Figure(figsize=(4.5, 3.5), dpi=90)
    try:
        cursor = conn.cursor()
        query = """
            SELECT 
                CASE loai_hoa_don 
                    WHEN 'B' THEN 'Bán Ra' 
                    WHEN 'M' THEN 'Nhập Vào' 
                    ELSE 'Khác' 
                END as loai,
                COUNT(*) as so_luong,
                SUM(tong_gia_tri_hoa_don) as tong_gia_tri
            FROM lich_su_hoa_don
            WHERE MONTH(ngay_giao_dich) = %s AND YEAR(ngay_giao_dich) = %s
            GROUP BY loai_hoa_don
        """
        cursor.execute(query, (thang, nam))
        data = cursor.fetchall()
        cursor.close()
        if not for_export:
            for i in reversed(range(ui.bieu_do_phan_tich_layout.count())): 
                ui.bieu_do_phan_tich_layout.itemAt(i).widget().setParent(None)
        if not data:
            canvas = FigureCanvas(fig)
            if not for_export:
                ui.bieu_do_phan_tich_layout.addWidget(canvas)
            ax = fig.add_subplot(111)
            ax.set_title(f'Không có dữ liệu phân tích - Tháng {thang}/{nam}')
            ax.axis('off')
            canvas.draw()
            return fig
        df = pd.DataFrame(data, columns=['loai', 'so_luong', 'tong_gia_tri'])
        canvas = FigureCanvas(fig)
        if not for_export:
            ui.bieu_do_phan_tich_layout.addWidget(canvas)
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie(
            df['so_luong'],
            labels=[loai if loai in ['Bán Ra', 'Nhập Vào'] else '' for loai in df['loai']],
            autopct='%1.1f%%',
            startangle=90,
            shadow=True,
            textprops={'fontsize': 9, 'fontweight': 'bold'},
            colors=['#3498db', '#e74c3c', '#2ecc71'],
            wedgeprops={'edgecolor': 'w', 'linewidth': 1}
        )
        ax.set_title('Số lượng hóa đơn theo loại', fontsize=11, pad=10)
        ax.axis('equal')
        legend_labels = [f"{label}" for label in df['loai']]
        ax.legend(
            wedges, 
            legend_labels,
            title="Loại hóa đơn",
            loc="center right",
            bbox_to_anchor=(1.4, 0.5),
            fontsize=8
        )
        for autotext in autotexts:
            autotext.set_color('white')
        fig.tight_layout()
        fig.subplots_adjust(left=0.2, right=0.95)
        canvas.draw()
        return fig
    except Exception as e:
        print(f"Lỗi khi tạo biểu đồ phân tích hóa đơn: {e}")
        return fig
    finally:
        if conn:
            conn.close()

def ve_bieu_do_doanh_thu_loi_nhuan_theo_danh_muc(ui, thang, nam, for_export=False):
    conn = create_connection()
    fig = Figure(figsize=(8, 4), dpi=100)
    try:
        cursor = conn.cursor()
        query = """
            SELECT dm.ten_danh_muc,
                   SUM(cthd.so_luong * sp.gia_san_pham) AS doanh_thu,
                   SUM(cthd.so_luong * (sp.gia_san_pham - IFNULL(sp.gia_nhap_san_pham,0))) AS loi_nhuan
            FROM chi_tiet_hoa_don cthd
            JOIN lich_su_hoa_don lshd ON cthd.id_hoa_don = lshd.id_hoa_don
            JOIN danh_sach_san_pham sp ON cthd.id_san_pham = sp.id_san_pham
            JOIN danh_muc_san_pham dm ON sp.id_danh_muc = dm.id_danh_muc
            WHERE MONTH(lshd.ngay_giao_dich) = %s AND YEAR(lshd.ngay_giao_dich) = %s AND lshd.loai_hoa_don = 'B'
            GROUP BY dm.ten_danh_muc
            ORDER BY doanh_thu DESC
        """
        cursor.execute(query, (thang, nam))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        if not for_export:
            for i in reversed(range(ui.bieu_do_doanh_muc_layout.count())):
                ui.bieu_do_doanh_muc_layout.itemAt(i).widget().setParent(None)
        if not data:
            canvas = FigureCanvas(fig)
            if not for_export:
                ui.bieu_do_doanh_muc_layout.addWidget(canvas)
            ax = fig.add_subplot(111)
            ax.set_title('Không có dữ liệu doanh thu/lợi nhuận theo danh mục')
            ax.axis('off')
            canvas.draw()
            return fig
        df = pd.DataFrame(data, columns=['Danh mục', 'Doanh thu', 'Lợi nhuận'])
        y = np.arange(len(df))
        width = 0.35
        canvas = FigureCanvas(fig)
        if not for_export:
            ui.bieu_do_doanh_muc_layout.addWidget(canvas)
        ax = fig.add_subplot(111)
        ax.barh(y - width/2, df['Doanh thu'], height=width, label='Doanh thu', color='#3498db')
        ax.barh(y + width/2, df['Lợi nhuận'], height=width, label='Lợi nhuận', color='#2ecc71')
        ax.set_yticks(y)
        ax.set_yticklabels(df['Danh mục'])
        ax.set_xlabel('')
        fig.suptitle(f'Doanh thu & Lợi nhuận theo danh mục - Tháng {thang}/{nam}', fontsize=12)
        ax.legend()
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        canvas.draw()
        return fig
    except Exception as e:
        print(f'Lỗi khi vẽ biểu đồ doanh thu/lợi nhuận theo danh mục: {e}')
        return fig

def xu_ly_su_kien_bao_cao(ui):
    """Kết nối các sự kiện từ giao diện với các hàm xử lý"""
    # Lấy tháng và năm từ giao diện
    thang_text = ui.thang_combobox.currentText()
    nam_text = ui.nam_combobox.currentText()
    
    # Chuyển đổi sang kiểu số
    try:
        # Trích xuất số tháng từ "Tháng X"
        thang = int(thang_text.split()[1])
        
        # Trích xuất số năm từ "Năm XXXX"
        nam = int(nam_text.split()[1])
    except (ValueError, IndexError):
        QMessageBox.warning(None, "Lỗi", "Tháng hoặc năm không hợp lệ!")
        return
    
    # Cập nhật thông tin thống kê
    cap_nhat_thong_ke_bao_cao(ui, thang, nam)
    
    # Vẽ biểu đồ doanh thu
    ve_bieu_do_doanh_thu(ui, thang, nam)
    
    # Load danh sách hóa đơn
    
    # Load danh sách sản phẩm bán ra trong tháng
    load_san_pham_theo_thang(ui, thang, nam)
    
    # Tạo biểu đồ phân tích theo loại hóa đơn
    tao_thong_ke_theo_loai_hoa_don(ui, thang, nam)
    
    # Vẽ biểu đồ doanh thu/lợi nhuận theo danh mục
    ve_bieu_do_doanh_thu_loi_nhuan_theo_danh_muc(ui, thang, nam)

    # Hiển thị bảng top 5 sản phẩm bán chạy
    hien_thi_bang_top_5_san_pham(ui, thang, nam)

def xu_ly_xuat_bao_cao_pdf(ui):
    try:
        thang_text = ui.thang_combobox.currentText()
        nam_text = ui.nam_combobox.currentText()
        thang = int(thang_text.split()[-1])  # Lấy số sau chữ "Tháng"
        nam = int(nam_text.split()[-1])      # Lấy số sau chữ "Năm"
    except Exception:
        QMessageBox.warning(None, "Lỗi", "Tháng hoặc năm không hợp lệ!")
        return
    pdf_path = xuat_bao_cao_phan_tich_pdf(ui, thang, nam)
    QMessageBox.information(None, "Thành công", f"Đã xuất báo cáo PDF!\nFile: {pdf_path}")

def xu_ly_xuat_bao_cao_excel(ui):
    try:
        thang_text = ui.thang_combobox.currentText()
        nam_text = ui.nam_combobox.currentText()
        thang = int(thang_text.split()[-1])  # Lấy số sau chữ "Tháng"
        nam = int(nam_text.split()[-1])      # Lấy số sau chữ "Năm"
    except Exception:
        QMessageBox.warning(None, "Lỗi", "Tháng hoặc năm không hợp lệ!")
        return
    success, message = xuat_bao_cao_excel(thang, nam)
    if success:
        try:
            import os, subprocess
            abs_path = os.path.abspath(message)
            if os.path.exists(abs_path):
                if os.name == 'nt':
                    os.startfile(abs_path)
                else:
                    subprocess.Popen(['xdg-open', abs_path])
            else:
                print(f"File không tồn tại: {abs_path}")
        except Exception as e:
            print(f"Không thể mở file Excel: {e}")
        QMessageBox.information(None, "Thành công", f"Đã xuất dữ liệu Excel!\nFile: {message}")
    else:
        QMessageBox.warning(None, "Lỗi", f"Lỗi khi xuất dữ liệu: {message}")

def khoi_tao_bao_cao(ui):
    """Khởi tạo giao diện báo cáo và kết nối các sự kiện"""
    # Khởi tạo ComboBox tháng và năm
    ui.thang_combobox = ui.thang
    ui.nam_combobox = ui.nam
    
    # Điền dữ liệu cho ComboBox tháng với định dạng "Tháng X"
    if ui.thang_combobox.count() == 0:
        for thang in range(1, 13):
            ui.thang_combobox.addItem(f"Tháng {thang}")
    
    # Điền dữ liệu cho ComboBox năm với định dạng "Năm XXXX"
    nam_hien_tai = datetime.now().year
    if ui.nam_combobox.count() == 0:
        for nam in range(nam_hien_tai - 5, nam_hien_tai + 1):
            ui.nam_combobox.addItem(f"Năm {nam}")
    # Luôn set năm hiện tại, không phụ thuộc vào count
    ui.nam_combobox.setCurrentText(f"Năm {nam_hien_tai}")
    
    # Chọn tháng hiện tại
    thang_hien_tai = datetime.now().month
    ui.thang_combobox.setCurrentText(f"Tháng {thang_hien_tai}")
    
    # Kết nối sự kiện thay đổi tháng/năm
    ui.thang_combobox.currentIndexChanged.connect(lambda: xu_ly_su_kien_bao_cao(ui))
    ui.nam_combobox.currentIndexChanged.connect(lambda: xu_ly_su_kien_bao_cao(ui))
    
    # Kết nối sự kiện nút xuất báo cáo
    ui.xuat_bao_cao_button.clicked.connect(lambda: xu_ly_xuat_bao_cao_pdf(ui))
    ui.xuat_du_lieu_button.clicked.connect(lambda: xu_ly_xuat_bao_cao_excel(ui))
    
    # Tạo tham chiếu đến các label hiển thị thông tin
    ui.tong_doanh_thu_label = ui.label_7  # Label tổng doanh thu
    ui.doanh_thu_thang_label = ui.label_8  # Label doanh thu tháng hiện tại
    ui.tong_san_pham_label = ui.label_10  # Label tổng sản phẩm bán ra
    ui.tong_loi_nhuan_label = ui.label_12  # Label tổng lợi nhuận tháng này
    ui.so_voi_thang_truoc_label = ui.label_13  # hoặc label nào bạn dùng cho phần này
    ui.tong_chi_thang_label = ui.label_16  # Thêm dòng này: ánh xạ label tổng chi tháng hiện tại
    
    # Tạo layout cho biểu đồ
    ui.bieu_do_layout = QVBoxLayout()
    ui.frame_bieu_do = QFrame(ui.bao_cao_screen)
    ui.frame_bieu_do.setGeometry(QRect(40, 350, 571, 271))
    ui.frame_bieu_do.setLayout(ui.bieu_do_layout)
    
    # Tạo layout cho biểu đồ phân tích và mở rộng kích thước
    ui.bieu_do_phan_tich_layout = QVBoxLayout()
    ui.frame_bieu_do_phan_tich = QFrame(ui.bao_cao_screen)
    ui.frame_bieu_do_phan_tich.setGeometry(QRect(630, 350, 371, 271))
    ui.frame_bieu_do_phan_tich.setLayout(ui.bieu_do_phan_tich_layout)
    
    # Tạo layout cho biểu đồ doanh thu/lợi nhuận theo danh mục
    ui.bieu_do_doanh_muc_layout = QVBoxLayout()
    ui.frame_bieu_do_doanh_muc = QFrame(ui.bao_cao_screen)
    ui.frame_bieu_do_doanh_muc.setGeometry(QRect(360, 20, 471, 311))
    ui.frame_bieu_do_doanh_muc.setLayout(ui.bieu_do_doanh_muc_layout)
    
    # Tạo layout cho bảng top 5 sản phẩm bán chạy
    ui.top5_layout = QVBoxLayout()
    ui.frame_top5 = QFrame(ui.bao_cao_screen)
    ui.frame_top5.setGeometry(QRect(860, 90, 321, 231))  # <-- CHỈNH Ở ĐÂY
    ui.frame_top5.setLayout(ui.top5_layout)
    
    # Khởi tạo dữ liệu ban đầu
    xu_ly_su_kien_bao_cao(ui)
    # Cập nhật bảng top 5 sản phẩm bán chạy ban đầu

def lay_top_5_san_pham_ban_chay(thang, nam):
    """Lấy top 5 sản phẩm bán chạy nhất trong tháng/năm"""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = """
            SELECT sp.ten_san_pham, 
                   SUM(cthd.so_luong) AS so_luong_ban, 
                   SUM(cthd.so_luong * sp.gia_san_pham) AS doanh_thu
            FROM chi_tiet_hoa_don cthd
            JOIN lich_su_hoa_don lshd ON cthd.id_hoa_don = lshd.id_hoa_don
            JOIN danh_sach_san_pham sp ON cthd.id_san_pham = sp.id_san_pham
            WHERE lshd.loai_hoa_don = 'B'
              AND MONTH(lshd.ngay_giao_dich) = %s
              AND YEAR(lshd.ngay_giao_dich) = %s
            GROUP BY sp.ten_san_pham
            ORDER BY so_luong_ban DESC
            LIMIT 5
        """
        cursor.execute(query, (thang, nam))
        data = cursor.fetchall()
        cursor.close()
        return data
    except Exception as e:
        print(f"Lỗi khi lấy top 5 sản phẩm bán chạy: {e}")
        return []
    finally:
        if conn:
            conn.close()

def hien_thi_bang_top_5_san_pham(ui, thang, nam):
    """Hiển thị bảng top 5 sản phẩm bán chạy lên giao diện"""
    data = lay_top_5_san_pham_ban_chay(thang, nam)
    # Xóa bảng cũ nếu có
    for i in reversed(range(ui.top5_layout.count())):
        widget = ui.top5_layout.itemAt(i).widget()
        if widget:
            widget.setParent(None)
    # Tiêu đề
    title = QLabel(f"<b>Top 5 sản phẩm bán chạy tháng {thang}/{nam}</b>")
    ui.top5_layout.addWidget(title)
    # Tạo bảng
    table = QTableWidget(len(data), 3)
    table.setHorizontalHeaderLabels(["Sản phẩm", "Số lượng", "Doanh thu"])
    for row, (ten, sl, dt) in enumerate(data):
        for col, val in enumerate([ten, sl, f"{dt:,.0f} đ"]):
            item = QTableWidgetItem(str(val))
            if row == 0:
                item.setBackground(QColor("#FFFACD"))  # Vàng nhạt cho top 1
            table.setItem(row, col, item)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.resizeColumnsToContents()
    ui.top5_layout.addWidget(table)

def xuat_bao_cao_phan_tich_pdf(ui, thang, nam):
    temp_dir = "bao_cao/temp_bao_cao"
    os.makedirs(temp_dir, exist_ok=True)
    # Lưu các Figure ra file
    fig1 = ve_bieu_do_doanh_thu(ui, thang, nam, for_export=True)
    fig2 = ve_bieu_do_doanh_thu_loi_nhuan_theo_danh_muc(ui, thang, nam, for_export=True)
    fig3 = tao_thong_ke_theo_loai_hoa_don(ui, thang, nam, for_export=True)
    fig1.savefig(f"{temp_dir}/bieu_do_doanh_thu_ngay.png")
    fig2.savefig(f"{temp_dir}/bieu_do_danh_muc.png")
    fig3.savefig(f"{temp_dir}/bieu_do_phan_tich_loai.png")
    # Đăng ký font Roboto
    font_path = os.path.join("Font", "Roboto.ttf")
    font_bold_path = os.path.join("Font", "Roboto-Bold.ttf")
    pdfmetrics.registerFont(TTFont("Roboto", font_path))
    pdfmetrics.registerFont(TTFont("Roboto-Bold", font_bold_path))
    # Đặt tên file PDF
    now = datetime.now()
    pdf_name = f"bao_cao_thang_{thang}_{nam}_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = os.path.join("bao_cao", pdf_name)
    custom_size = (600, 900)  # width, height
    c = canvas.Canvas(pdf_path, pagesize=custom_size)
    width, height = custom_size
    y = height - 40
    c.setFont("Roboto-Bold", 14)
    c.drawString(40, y, f"BÁO CÁO PHÂN TÍCH THÁNG {thang}/{nam}")
    y -= 30
    c.setFont("Roboto", 11)
    c.drawString(40, y, f"Tổng doanh thu năm: {ui.tong_doanh_thu_label.text()}")
    y -= 20
    c.drawString(40, y, f"Doanh thu tháng hiện tại: {ui.doanh_thu_thang_label.text()}")
    y -= 20
    c.drawString(40, y, f"Tổng chi tháng hiện tại: {ui.tong_chi_thang_label.text()}")
    y -= 20
    c.drawString(40, y, f"Tổng sản phẩm bán ra: {ui.tong_san_pham_label.text()}")
    y -= 20
    c.drawString(40, y, f"Tổng lợi nhuận tháng này: {ui.tong_loi_nhuan_label.text()}")
    y -= 30
    c.setFont("Roboto-Bold", 12)
    c.drawString(40, y, "Top 5 sản phẩm bán chạy:")
    y -= 20
    c.setFont("Roboto", 10)
    table = ui.top5_layout.itemAt(1).widget()  # QTableWidget
    for row in range(table.rowCount()):
        row_data = [table.item(row, col).text() for col in range(table.columnCount())]
        c.drawString(50, y, " | ".join(row_data))
        y -= 15
    y -= 20
    img_paths = [
        (f"{temp_dir}/bieu_do_doanh_thu_ngay.png", "Biểu đồ doanh thu theo ngày"),
        (f"{temp_dir}/bieu_do_danh_muc.png", "Biểu đồ doanh thu & lợi nhuận theo danh mục"),
        (f"{temp_dir}/bieu_do_phan_tich_loai.png", "Biểu đồ phân tích hóa đơn theo loại"),
    ]
    for img_path, title in img_paths:
        if os.path.exists(img_path):
            c.setFont("Roboto-Bold", 11)
            c.drawString(40, y, title)
            y -= 10
            c.drawImage(ImageReader(img_path), 40, y-180, width=500, height=180, preserveAspectRatio=True)
            y -= 200
            if y < 100:
                c.showPage()
                y = height - 40
    c.save()
    for img_path, _ in img_paths:
        if os.path.exists(img_path):
            os.remove(img_path)
    try:
        if os.name == 'nt':
            os.startfile(pdf_path)
        else:
            subprocess.Popen(['xdg-open', pdf_path])
    except Exception as e:
        print(f"Không thể mở file PDF: {e}")
    return pdf_path