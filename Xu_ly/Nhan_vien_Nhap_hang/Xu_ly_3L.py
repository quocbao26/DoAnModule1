from flask import   Markup, url_for
import json
import os
from datetime import datetime
Thu_muc_Du_lieu ="Du_lieu"
Thu_muc_Tivi = "Du_lieu/Tivi/"
Thu_muc_Cong_ty= "Du_lieu/Cong_ty/"

# Xử lý lưu trữ
def Doc_Danh_Sach_Tivi():
    Danh_Sach = []
    for Ten_Tap_Tin in os.listdir(Thu_muc_Tivi):
        Duong_Dan = Thu_muc_Tivi + Ten_Tap_Tin
        file = open(Duong_Dan, encoding='utf-8')
        Tivi = json.load(file)
        file.close()
        Danh_Sach.append(Tivi)
    return Danh_Sach

def Doc_Cong_ty():
    Duong_dan = Thu_muc_Cong_ty + "Cong_ty.json"
    file = open(Duong_dan, encoding='utf-8')
    cong_ty = json.load(file)
    file.close()
    return cong_ty

def Ghi_Tivi(Tivi):
    Ten_tap_tin = Thu_muc_Tivi + Tivi['Ma_so']+'.json'
    file = open(Ten_tap_tin, 'w', encoding='utf-8')
    json.dump(Tivi, file, indent=4, ensure_ascii=False)
    file.close()
    print('Đã ghi Tivi!')
    return 1
##
def Tra_Cuu_Tivi(Chuoi_tra_cuu, Danh_Sach_Tivi):
    Danh_Sach = list(filter(lambda Tivi: Chuoi_tra_cuu.upper() in Tivi['Ten'].upper() ,Danh_Sach_Tivi))
    return Danh_Sach

def Lay_Chi_tiet_Tivi(Danh_sach_Tivi, Ma_so):
    Danh_Sach = list(filter(lambda Tivi: Tivi['Ma_so'] == Ma_so ,Danh_sach_Tivi))
    Tivi = Danh_Sach[0] if len(Danh_Sach) == 1 else None
    return Tivi

def Nhap_Tivi(Nhan_vien, Tivi, So_luong_nhap):
    Tien = int(Tivi['Don_gia_Nhap']) * int(So_luong_nhap)
    Ngay = datetime.now().strftime('%d-%m-%Y')
    Phieu_nhap = {'Ngay':Ngay, 'So_luong':So_luong_nhap, 'Don_gia':Tivi['Don_gia_Nhap'], 'Tien':Tien, 'Nhan_vien': {'Ho_ten': Nhan_vien['Ho_ten'], 'Ma_so': Nhan_vien['Ma_so']}}
    Tivi['So_luong_Ton'] += So_luong_nhap
    Tivi['Danh_sach_Phieu_Nhap'].append(Phieu_nhap)
    return Tien

def Tong_ket_1_Tivi_Theo_Ngay(Tivi, Ngay):
    Tong_So_luong = 0
    Tong_Tien = 0
    Don_gia = 0
    for Phieu_ban in Tivi['Danh_sach_Phieu_Nhap']:
        if Phieu_ban['Ngay'] == Ngay:
            Tong_So_luong += int(Phieu_ban['So_luong'])
            Tong_Tien += int(Phieu_ban['Tien'])
            Don_gia = Phieu_ban['Don_gia']
    Thong_tin = {'Ten':Tivi['Ten'], 'So_luong':Tong_So_luong, 'Don_gia': Don_gia, 'Tien':Tong_Tien}
    return Thong_tin

def Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi, Ngay):
    Danh_sach = []
    for Tivi in Danh_sach_Tivi:
        thong_tin = Tong_ket_1_Tivi_Theo_Ngay(Tivi, Ngay)
        if thong_tin['So_luong'] != 0:
            Danh_sach.append(thong_tin)
    return Danh_sach

def Danh_sach_Tivi_Nhap_Theo_ngay(Danh_sach_Tivi, Ngay):
    Danh_sach = []
    for Tivi in Danh_sach_Tivi:
        for Phieu_ban in Tivi['Danh_sach_Phieu_Nhap']:
            if Phieu_ban['Ngay'] == Ngay:
                Danh_sach.append(Tivi)
                break
        Danh_sach
    return Danh_sach
#


# Xử lý nghiệp vụ
def Dang_nhap_Nhan_vien(Danh_sach_Nhan_vien, Ten_dang_nhap, Mat_khau):
    Danh_sach = list(filter(lambda Nhan_vien: Nhan_vien['Ten_dang_nhap'] == Ten_dang_nhap and Nhan_vien['Mat_khau'] == Mat_khau, Danh_sach_Nhan_vien))
    nhan_vien = Danh_sach[0] if len(Danh_sach) == 1 else None
    return nhan_vien
    

# Xử lý Thể hiện
def Tao_chuoi_HTML_Nhan_vien(Nhan_vien):
    Chuoi_HTML_Nhan_vien = '<div class="row" >'
    Chuoi_Hinh = '<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = Nhan_vien["Ma_so"]+'.png') + '" />'
    Chuoi_Thong_tin = '<div class="btn" style="text-align:left"> Xin chào nhân viên Nhập hàng ' + \
                 Nhan_vien["Ho_ten"] + "</div>"
    
    Chuoi_HTML_Nhan_vien += Chuoi_Hinh + Chuoi_Thong_tin 
    
    return Markup(Chuoi_HTML_Nhan_vien)  

def Tao_Chuoi_HTML_Tivi(Tivi, Thong_bao, So_luong):
    Chuoi_Hinh='<img  style="width:300px" src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'
    Chuoi_Loai_Tivi = "Thuộc loại: " + Tivi["Nhom_Tivi"]["Ten"] + "<br/>"
    Chuoi_Ky_hieu = "Ký hiệu:" + Tivi["Ky_hieu"] + "<br/>"
    Chuoi_SL_Ton = "Số lượng tồn:" + str(Tivi["So_luong_Ton"]) + "<br/>"
    Chuoi_Don_gia_Nhap="Đơn giá Nhập {:,}".format(Tivi["Don_gia_Nhap"]).replace(",",".") 
    Chuoi_Ngay = "Ngày: "  + datetime.now().strftime('%d-%m-%Y')
    Chuoi_HTML_Tivi = '''
        <div class="container">
          <div class="card" align="center">
            <h4 class="card-title">Phiếu nhập</h4>
            <h6 class="card-title">'''+ Chuoi_Ngay+'''</h6>
            ''' + Chuoi_Hinh + '''
            <div class="card-body">
              <h4 class="card-title">'''+ Tivi["Ten"]+'''</h4>
              <p class="card-text">'''+ Chuoi_Don_gia_Nhap +'''<br/>'''+ Chuoi_SL_Ton +''' </p>
    
              <form method="POST">
                <div class="container-fluid">
                  <div class="alert" style="height:30px">
                    <input name="Th_So_luong" type="number" required min="1" max="'''+ str(Tivi["So_luong_Ton"])+'''" spellcheck="false" 
                    autocomplete="off" value="'''+ str(So_luong) + '''"
                    />
                  </div>
                  <div class="alert" style="height:40px">
                    <button class="btn btn-danger" type="submit">Đồng ý</button>
                  </div>
                </div>
                <div>'''+ Thong_bao +'''</div>
              </form>
            </div>
          </div>
        </div>
        '''
    return Markup(Chuoi_HTML_Tivi)    

def Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi):   
    Chuoi_HTML_Danh_sach = '<div class="row" >'
    for Tivi in Danh_sach_Tivi:        
        Chuoi_Don_gia_Nhap="Đơn giá Nhập {:,}".format(Tivi["Don_gia_Nhap"]).replace(",",".")    
        Chuoi_So_luong_ton = "SL Tồn " + str(Tivi["So_luong_Ton"])
        Chuoi_Hinh='<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'        
        Chuoi_Loai_Tivi = "Thuộc loại: " + Tivi["Nhom_Tivi"]["Ten"] + "<br/>"
        Chuoi_Ky_hieu = "Ký hiệu:" + Tivi["Ky_hieu"] + "<br/>"
        Chuoi_SL_Ton = "Số lượng tồn:" + str(Tivi["So_luong_Ton"]) + "<br/>"
        Chuoi_Thong_tin='<div class="btn" style="text-align:left">' + \
                 Tivi["Ten"] + "<br />" + Chuoi_Don_gia_Nhap + "<br/>" + \
                 Chuoi_SL_Ton + \
                 '''<a href="/Nhan_vien_Nhap_hang/Nhap/''' + Tivi["Ma_so"] +'''/">Nhập</a>'''+ '</div>'
        Chuoi_HTML ='<div class="col-md-4" >' +  \
                Chuoi_Hinh + Chuoi_Thong_tin + '</div>' 
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach += '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)  
 
def Tao_Chuoi_HTML_Thong_ke_Tivi(Danh_sach_Thong_ke):
    Ngay = "Ngày: " + datetime.now().strftime('%d-%m-%Y') 
    Chuoi_Tong_tien = "...Tổng tiền: {:,}".format(sum(Tivi['Tien'] for Tivi in Danh_sach_Thong_ke)).replace(",",".") 
    
    Chuoi_HTML_Danh_sach = '<div class="container"><h3>Thống kê Phiếu nhập</h3><br/><h5>' + Ngay + Chuoi_Tong_tien + '</h5></div>'
    Chuoi_HTML_Danh_sach += '<div class="row" >'
    
    stt = 1
    header = '''
        <div class="dong" >
        <div class="cot">STT</div>
        <div class="cot">Tivi</div>
        <div class="cot">Số lượng</div>
        <div class="cot">Đơn giá</div>
        <div class="cot">Tiền</div>
        </div>
        '''  
    Chuoi_HTML_Danh_sach +=header

    for Tivi in Danh_sach_Thong_ke:
        Chuoi_HTML = '''
        <div class="dong">
        <div class="cot">'''+ str(stt) +'''</div>
        <div class="cot">'''+ Tivi['Ten']+'''</div>
        <div class="cot">'''+ str(Tivi['So_luong']) +'''</div>
        <div class="cot">'''+ "{:,}".format(Tivi["Don_gia"]).replace(",",".") +'''</div>
        <div class="cot">'''+ "{:,}".format(Tivi["Tien"]).replace(",",".") +'''</div>
        </div>
        '''     
        stt += 1

        
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach += '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)  
