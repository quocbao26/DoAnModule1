from flask import Flask, request, render_template, json, redirect, session
from Xu_ly.Khach_tham_quan.Xu_ly_3L import *
from Xu_ly.Nhan_vien_Ban_hang.Xu_ly_3L import *

app = Flask(__name__, static_folder='Media', template_folder='Giao_dien')
app.secret_key = "2019"

@app.route('/', methods=['GET', 'POST'])
def Dang_Nhap():
    if session.get('Nhan_vien_Ban_hang'):
        return redirect(url_for('index'))
    Cong_ty = Doc_Cong_ty()
    Ten_dang_nhap = ""
    Mat_khau = ""
    Chuoi_Thong_bao = ""
    if request.method == 'POST':
        Ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        Mat_khau = request.form.get('Th_Mat_khau')
        
        nhan_vien = Dang_nhap_Nhan_vien(Cong_ty['Danh_sach_Nhan_vien_Ban_hang'] ,Ten_dang_nhap, Mat_khau)
        if nhan_vien != None:
            session['Nhan_vien_Ban_hang'] = nhan_vien
            return redirect(url_for('index'))
        else:
            Chuoi_Thong_bao = "Đăng nhập thất bại"

    return render_template('Nhan_vien_Ban_hang/MH_Dang_nhap.html', Chuoi_Thong_bao=Chuoi_Thong_bao)


@app.route('/Nhan_vien_Ban_hang', methods=['GET', 'POST'])
def index():
    Nhan_vien_Dang_nhap = session['Nhan_vien_Ban_hang']
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

    url_MH = "/Nhan_vien_Ban_hang/Xem_Danh_sach_Tivi"
    if request.method == 'POST':
        Ma_so = request.form.get('Th_Ma_so')
        if Ma_so == 'DANH_SACH':
            url_MH = "/Nhan_vien_Ban_hang/Xem_Danh_sach_Tivi"
        if Ma_so == 'TRA_CUU':
            Chuoi_Tra_Cuu = request.form.get('Th_Chuoi_Tra_cuu')
            url_MH = "/Nhan_vien_Ban_hang/Tra_cuu/" + Chuoi_Tra_Cuu + "/"
        # PHIEU_NHAP
        if Ma_so == 'DOANH_THU':
            url_MH = "/Nhan_vien_Ban_hang/Thong_ke/"

    return render_template('Nhan_vien_Ban_hang/MH_Chinh.html', Dia_chi_MH=url_MH, Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien)

def Thong_tin():
    Nhan_vien_Dang_nhap = session['Nhan_vien_Ban_hang']
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)
    Danh_sach_Tivi = Doc_Danh_Sach_Tivi()
    return Chuoi_HTML_Nhan_vien, Danh_sach_Tivi

@app.route('/Nhan_vien_Ban_hang/Xem_Danh_sach_Tivi', methods=['GET', 'POST'])
def Xem_Danh_sach_Tivi():
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    # Khai báo biến
    Danh_sach_Tivi_Xem = Danh_sach_Tivi
    # Kết xuất
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)

    return render_template('Nhan_vien_Ban_hang/MH_Xem_Danh_sach_Tivi.html', Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi, Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien)

@app.route('/Nhan_vien_Ban_hang/Tra_cuu/<string:Chuoi_Tra_cuu>/', methods=['GET', 'POST'])
def Tra_cuu_Tivi_theo_Chuoi_Tra_cuu(Chuoi_Tra_cuu):
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    # Khai báo biến
    Danh_sach_Tivi_Xem = Danh_sach_Tivi
    # Biến kết quả
    Danh_sach_Tivi_Xem = Tra_Cuu_Tivi(Chuoi_Tra_cuu, Danh_sach_Tivi)
    # Kết xuất
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)
    return render_template('Nhan_vien_Ban_hang/MH_Xem_Danh_sach_Tivi.html', Chuoi_Tra_cuu=Chuoi_Tra_cuu, Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien, Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)

@app.route('/Nhan_vien_Ban_hang/Ban/<string:Ma_so>/', methods=['GET', 'POST'])
def Nhan_vien_Ban_Tivi(Ma_so):
    Nhan_vien_Dang_nhap = session['Nhan_vien_Ban_hang']
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    Tivi_Chon = Lay_Chi_tiet_Tivi(Danh_sach_Tivi, Ma_so)

    if Tivi_Chon != None:
        So_luong = 1
        Thong_Bao = ""
        if request.method == 'POST':
            So_luong = int(request.form.get('Th_So_luong'))
            Tien = Ban_Tivi(Nhan_vien_Dang_nhap, Tivi_Chon, So_luong)
            Thong_Bao = "Vừa bán " + str(So_luong) + " Tivi " + Tivi_Chon['Ten'] + " - Tiền phải trả là: {:,}".format(Tien).replace(',','.')
            Ghi_Tivi(Tivi_Chon)
        Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_Chon, Thong_Bao, So_luong)
        return render_template('Nhan_vien_Ban_hang/MH_Ban_Tivi.html', Chuoi_HTML_Tivi=Chuoi_HTML_Tivi)

@app.route('/Nhan_vien_Ban_hang/Thong_ke/', methods=['GET', 'POST'])
def Liet_ke_Phieu_nhap():
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    Ngay = datetime.now().strftime('%d-%m-%Y')
    Danh_sach_Tivi_ban = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay)

    Danh_sach_Thong_ke = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi, Ngay)

    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_Thong_ke_Tivi(Danh_sach_Thong_ke)
    return render_template('Nhan_vien_Ban_hang/MH_Xem_Doanh_thu.html', Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)

@app.route('/Nhan_vien_Ban_hang/Dang_xuat/', methods=['GET', 'POST'])
def Dang_Xuat():
    session.pop('Nhan_vien_Ban_hang', None)
    return redirect(url_for('Dang_Nhap'))


if __name__ == '__main__':
    app.debug=True
    app.run(port=5002)
