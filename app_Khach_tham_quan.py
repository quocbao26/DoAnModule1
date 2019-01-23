from flask import Flask, request, render_template, json
from Xu_ly.Khach_tham_quan.Xu_ly_3L import *
app = Flask(__name__, static_folder='Media', template_folder='Giao_dien')
app.secret_key = "2019"

@app.route('/', methods=['GET', 'POST'])
def index():
    Danh_Sach_Tivi = Doc_Danh_Sach_Tivi()
    
    Danh_Sach_tivi_Xem = Danh_Sach_Tivi # danh sách tất cả tivi
    Chuoi_Tra_Cuu = "" # chuỗi khi ng dùng nhập

    if request.form.get('Th_Chuoi_Tra_cuu') != None:
        Chuoi_Tra_Cuu = request.form.get('Th_Chuoi_Tra_cuu')
        Danh_Sach_tivi_Xem = Tra_Cuu_Tivi(Chuoi_Tra_Cuu, Danh_Sach_Tivi)

    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_Sach_tivi_Xem)
    return render_template('Khach_tham_quan/MH_Chinh.html', Chuoi_Tra_Cuu=Chuoi_Tra_Cuu, Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)

if __name__ == '__main__':
    app.debug=True
    app.run(port=5001)
