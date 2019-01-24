from flask import Flask, request, render_template, json, redirect, session
from Xu_ly.Khach_tham_quan.Xu_ly_3L import *
from Xu_ly.Quan_ly_Ban_hang.Xu_ly import *

app = Flask(__name__, static_folder='Media', template_folder='Giao_dien')
app.secret_key = "2019"


@app.route('/', methods=['GET', 'POST'])
def Dang_Nhap():
    if session.get('Quan_ly_Ban_hang'):
        return redirect(url_for('index'))
    Cong_ty = Doc_Cong_ty()
    Ten_dang_nhap = ""
    Mat_khau = ""
    Chuoi_Thong_bao = ""
    if request.method == 'POST':
        Ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        Mat_khau = request.form.get('Th_Mat_khau')

        quan_ly = Dang_nhap_Quan_ly(Cong_ty['Danh_sach_Quan_ly_Ban_hang'], Ten_dang_nhap, Mat_khau)
        if quan_ly != None:
            session['Quan_ly_Ban_hang'] = quan_ly
            return redirect(url_for('index'))
        else:
            Chuoi_Thong_bao = "Đăng nhập thất bại"

    return render_template('Quan_ly_Ban_hang/MH_Dang_nhap.html', Chuoi_Thong_bao=Chuoi_Thong_bao)


@app.route('/Quan_ly_Ban_hang', methods=['GET', 'POST'])
def index():
    Quan_ly_Dang_nhap = session['Quan_ly_Ban_hang']
    Chuoi_HTML_Quan_ly = Tao_chuoi_HTML_Quan_ly(Quan_ly_Dang_nhap)

    url_MH = "/Quan_ly_Ban_hang/Xem_Danh_sach_Tivi"
    if request.method == 'POST':
        Ma_so = request.form.get('Th_Ma_so')
        if Ma_so == 'DANH_SACH':
            url_MH = "/Quan_ly_Ban_hang/Xem_Danh_sach_Tivi"
        if Ma_so == 'TRA_CUU':
            Chuoi_Tra_Cuu = request.form.get('Th_Chuoi_Tra_cuu')
            url_MH = "/Quan_ly_Ban_hang/Tra_cuu/" + Chuoi_Tra_Cuu + "/"
        # PHIEU_NHAP
        if Ma_so == 'SO_LUONG_TON':
            url_MH = "/Quan_ly_Ban_hang/Thong_ke_so_luong_ton/"
        if Ma_so == 'DOANH_THU_TIVI':
            url_MH = "/Quan_ly_Ban_hang/Thong_ke_doanh_thu_theo_tivi/"
        if Ma_so == 'DOANH_THU_NHAN_VIEN':
            url_MH = "/Quan_ly_Ban_hang/Thong_ke_doanh_thu_theo_nhan_vien/"

    return render_template('Quan_ly_Ban_hang/MH_Chinh.html', Dia_chi_MH=url_MH, Chuoi_HTML_Quan_ly=Chuoi_HTML_Quan_ly)


def Thong_tin():
    Quan_ly_Dang_nhap = session['Quan_ly_Ban_hang']
    Chuoi_HTML_Quan_ly = Tao_chuoi_HTML_Quan_ly(Quan_ly_Dang_nhap)
    Danh_sach_Tivi = Doc_Danh_Sach_Tivi()
    return Chuoi_HTML_Quan_ly, Danh_sach_Tivi


@app.route('/Quan_ly_Ban_hang/Xem_Danh_sach_Tivi', methods=['GET', 'POST'])
def Xem_Danh_sach_Tivi():
    Chuoi_HTML_Quan_ly, Danh_sach_Tivi = Thong_tin()
    # Khai báo biến
    Danh_sach_Tivi_Xem = Danh_sach_Tivi
    # Kết xuất
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)

    return render_template('Quan_ly_Ban_hang/MH_Xem_Danh_sach_Tivi.html',
                           Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)


@app.route('/Quan_ly_Ban_hang/Tra_cuu/<string:Chuoi_Tra_cuu>/', methods=['GET', 'POST'])
def Tra_cuu_Tivi_theo_Chuoi_Tra_cuu(Chuoi_Tra_cuu):
    Chuoi_HTML_Quan_ly, Danh_sach_Tivi = Thong_tin()
    # Khai báo biến
    Danh_sach_Tivi_Xem = Danh_sach_Tivi
    # Biến kết quả
    Danh_sach_Tivi_Xem = Tra_Cuu_Tivi(Chuoi_Tra_cuu, Danh_sach_Tivi)

    # Kết xuất
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)
    return render_template('Quan_ly_Ban_hang/MH_Xem_Danh_sach_Tivi.html',
                           Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi, Chuoi_Tra_cuu=Chuoi_Tra_cuu)


@app.route('/Quan_ly_Ban_hang/CapNhat/<string:Ma_so>/', methods=['GET', 'POST'])
def Quan_ly_CapNhap_Tivi(Ma_so):
    Quan_ly_Dang_nhap = session['Quan_ly_Ban_hang']
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    Tivi_Chon = Lay_Chi_tiet_Tivi(Danh_sach_Tivi, Ma_so)

    if Tivi_Chon != None:
        don_gia_ban = 1
        Thong_Bao = ""
        if request.method == 'POST':
            don_gia_ban = int(request.form.get('Th_Don_gia'))
            # Tien = Nhap_Tivi(Quan_ly_Dang_nhap, Tivi_Chon, don_gia_nhap)
            Thong_Bao = "Cập nhật thành công với đơn giá mới {:,}".format(don_gia_ban).replace(',', '.')
            Ghi_Tivi(Tivi_Chon, don_gia_ban)
        Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_Chon, Thong_Bao, don_gia_ban)
        return render_template('Quan_ly_Ban_hang/MH_Cap_Nhap_Tivi.html', Chuoi_HTML_Tivi=Chuoi_HTML_Tivi)


@app.route('/Quan_ly_Ban_hang/Thong_ke_so_luong_ton/', methods=['GET', 'POST'])
def Liet_ke_So_luong_Ton():
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()

    # Danh_sach_Tivi_nhap = Danh_sach_Tivi_Nhap_Theo_ngay(Danh_sach_Tivi, Ngay)

    Danh_sach_Thong_ke = Tong_ket_So_luong_Ton(Danh_sach_Tivi)

    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_Thong_ke_SL_Ton_Tivi(Danh_sach_Thong_ke)
    return render_template('Quan_ly_Ban_hang/MH_Xem_SL_Ton.html',
                           Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)

@app.route('/Quan_ly_Ban_hang/Thong_ke_doanh_thu_theo_tivi/', methods=['GET', 'POST'])
def Liet_ke_doanh_thu_theo_Tivi():
    Chuoi_HTML_Nhan_vien, Danh_sach_Tivi = Thong_tin()
    Ngay = datetime.now().strftime('%d-%m-%Y')
    #Danh_sach_Tivi_ban = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay)

    Danh_sach_Thong_ke = Tong_ket_Doanh_thu_theo_Tivi(Danh_sach_Tivi, Ngay)

    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_Doanh_thu_Tivi(Danh_sach_Thong_ke)

    return render_template('Quan_ly_Ban_hang/MH_Xem_Doanh_thu_Tivi.html', Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)

@app.route('/Quan_ly_Ban_hang/Thong_ke_doanh_thu_theo_nhan_vien/', methods=['GET', 'POST'])
def Liet_ke_doanh_thu_theo_nhan_vien():
    Chuoi_HTML_Quan_ly, Danh_sach_Tivi = Thong_tin()
    Ngay = datetime.now().strftime('%d-%m-%Y')
    #Danh_sach_Tivi_ban = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay)

    Danh_sach_Thong_ke, dic_ma_so = Tong_ket_Doanh_thu_theo_nhan_vien(Danh_sach_Tivi, Ngay)

    Chuoi_HTML_Thong_ke_Nhan_vien = Tao_Chuoi_HTML_Doanh_thu_nhan_vien(Danh_sach_Thong_ke, dic_ma_so)

    return render_template('Quan_ly_Ban_hang/MH_Xem_Doanh_thu_Nhan_vien.html', Chuoi_HTML_Thong_ke_Nhan_vien=Chuoi_HTML_Thong_ke_Nhan_vien)

@app.route('/Quan_ly_Ban_hang/Dang_xuat/', methods=['GET', 'POST'])
def Dang_Xuat():
    session.pop('Quan_ly_Ban_hang', None)
    return redirect(url_for('Dang_Nhap'))


if __name__ == '__main__':
    app.debug = True
    app.run(port=5005)
