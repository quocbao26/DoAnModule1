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

def Ghi_Tivi(Tivi, don_gia_ban):
    Ten_tap_tin = Thu_muc_Tivi + Tivi['Ma_so']+'.json'
    Tivi['Don_gia_Ban'] = don_gia_ban
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
    Tivi['So_luong_ton'] += So_luong_nhap
    Tivi['Danh_sach_Phieu_Nhap'].append(Phieu_nhap)
    return Tien

def Tong_ket_1_Tivi_Theo_Ngay(Tivi, Ngay):
    Tong_So_luong = 0
    Tong_Tien = 0
    Don_gia = 0
    for Phieu_ban in Tivi['Danh_sach_Phieu_Ban']:
        if Phieu_ban['Ngay'] == Ngay:
            Tong_So_luong += int(Phieu_ban['So_luong'])
            Tong_Tien += int(Phieu_ban['Tien'])
            Don_gia = Phieu_ban['Don_gia']
    Thong_tin = {'Ten':Tivi['Ten'], 'So_luong':Tong_So_luong, 'Don_gia': Don_gia, 'Tien':Tong_Tien}
    return Thong_tin

def Tong_ket_1_Tivi_Theo_Ngay_Cua_Nhan_Vien(Tivi, Ngay, Ma_so):
    Tong_So_luong = 0
    Tong_Tien = 0
    Don_gia = 0
    Ma_so_nv = ""
    for Phieu_ban in Tivi['Danh_sach_Phieu_Ban']:
        if Phieu_ban['Nhan_vien']['Ma_so'] == Ma_so:
            if Phieu_ban['Ngay'] == Ngay:
                Tong_So_luong += int(Phieu_ban['So_luong'])
                Tong_Tien += int(Phieu_ban['Tien'])
                Don_gia = Phieu_ban['Don_gia']
                Ma_so_nv = Phieu_ban['Nhan_vien']['Ma_so']
    Thong_tin = {'Ma_so':Ma_so_nv,'Ten':Tivi['Ten'], 'So_luong':Tong_So_luong, 'Don_gia': Don_gia, 'Tien':Tong_Tien}
    print(Thong_tin)
    return Thong_tin

def Tong_ket_Doanh_thu_theo_Tivi(Danh_sach_Tivi, Ngay):
    Danh_sach = []
    for Tivi in Danh_sach_Tivi:
        thong_tin = Tong_ket_1_Tivi_Theo_Ngay(Tivi, Ngay)
        if thong_tin['So_luong'] != 0:
            Danh_sach.append(thong_tin)
    return Danh_sach

def Tong_ket_Doanh_thu_theo_nhan_vien(Danh_sach_Tivi, Ngay):
    Danh_sach = []
    dic = {}
    nv = Doc_Cong_ty()['Danh_sach_Nhan_vien_Ban_hang']
    for item in nv:
        dic[item['Ma_so']] = item['Ho_ten']

    for key, value in dic.items():
        for Tivi in Danh_sach_Tivi:
            thong_tin = Tong_ket_1_Tivi_Theo_Ngay_Cua_Nhan_Vien(Tivi, Ngay, key)
            # print(thong_tin)
            # print("-"*30)
            if thong_tin['So_luong'] != 0:
                Danh_sach.append(thong_tin)
        # print(dic)
        # print(Danh_sach)
    return Danh_sach,dic

def Lay_Thuong_Hieu():
    nhom_tivi = Doc_Cong_ty()
    tmp = nhom_tivi['Danh_sach_Nhom_Tivi']
    return tmp

def Tong_ket_So_luong_Ton(Danh_sach_Tivi):
    Danh_sach = {}
    lst_ma  = []
    lst_ten = []
    tong_all = 0
    so_luong_co_ma = 0
    thong_tin = Lay_Thuong_Hieu()
    for item in thong_tin:
        lst_ma.append(item['Ma_so'])
        lst_ten.append(item['Ten'])

    # set tất cả value bằng 0
    Danh_sach = Danh_sach.fromkeys(lst_ten,0)

    # tính tổng số lượng trong Danh sách
    for Tivi in Danh_sach_Tivi:
        tong_all += Tivi['So_luong_Ton']
    
    # tính tổng số lượng theo từng loại mã
    for i in range(len(lst_ma)):
        for Tivi in Danh_sach_Tivi:
            ten = Tivi['Ten']
            if lst_ma[i].lower() in ten.lower():
                Danh_sach[lst_ten[i]] += Tivi['So_luong_Ton']

    # tính tổng tất cả có mã
    for k, v in Danh_sach.items():
        so_luong_co_ma += v

    # tính tổng các sản phẩm không có mã
    Danh_sach['Khác'] = tong_all - so_luong_co_ma

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



# Xử lý nghiệp vụ
def Dang_nhap_Quan_ly(Danh_sach_Quan_ly, Ten_dang_nhap, Mat_khau):
    Danh_sach = list(filter(lambda Quan_ly: Quan_ly['Ten_dang_nhap'] == Ten_dang_nhap and Quan_ly['Mat_khau'] == Mat_khau, Danh_sach_Quan_ly))
    quan_ly = Danh_sach[0] if len(Danh_sach) == 1 else None
    return quan_ly
    

# Xử lý Thể hiện
def Tao_chuoi_HTML_Quan_ly(Quan_ly):
    Chuoi_HTML_Quan_ly = '<div class="row" >'
    Chuoi_Hinh = '<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = Quan_ly["Ma_so"]+'.png') + '" />'
    Chuoi_Thong_tin = '<div class="btn" style="text-align:left"> Xin chào Quản lý Bán hàng ' + \
                 Quan_ly["Ho_ten"] + "</div>"
    
    Chuoi_HTML_Quan_ly += Chuoi_Hinh + Chuoi_Thong_tin 
    
    return Markup(Chuoi_HTML_Quan_ly)  

def Tao_Chuoi_HTML_Tivi(Tivi, Thong_bao, Don_gia_ban_moi):
    Chuoi_Hinh='<img  style="width:300px" src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'
    Chuoi_Loai_Tivi = "Thuộc loại: " + Tivi["Nhom_Tivi"]["Ten"] + "<br/>"
    Chuoi_Ky_hieu = "Ký hiệu:" + Tivi["Ky_hieu"] + "<br/>"
    Chuoi_SL_Ton = "Số lượng tồn:" + str(Tivi["So_luong_Ton"]) + "<br/>"
    Chuoi_Don_gia_Ban="Đơn giá Bán hiện hành {:,}".format(Tivi["Don_gia_Ban"]).replace(",",".")
    Chuoi_Ngay = "Ngày: "  + datetime.now().strftime('%d-%m-%Y')
    Chuoi_HTML_Tivi = '''
        <div class="container">
          <div class="card" align="center">
            <h4 class="card-title">Cập nhật Đơn giá bán</h4>
            <h6 class="card-title">'''+ Chuoi_Ngay+'''</h6>
            ''' + Chuoi_Hinh + '''
            <div class="card-body">
              <h4 class="card-title">'''+ Tivi["Ten"]+'''</h4>
              <p class="card-text">'''+ Chuoi_Don_gia_Ban +'''<br/>'''+ Chuoi_SL_Ton +''' </p>
    
              <form method="POST">
                <div class="container-fluid">
                  <div class="alert" style="height:30px">
                    <input name="Th_Don_gia" type="number" required min="1" max="'''+ str(Tivi["Don_gia_Ban"])+'''" spellcheck="false" 
                    autocomplete="off" value="'''+ str(Don_gia_ban_moi) + '''"
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
        Chuoi_Don_gia_Ban="Đơn giá Bán {:,}".format(Tivi["Don_gia_Ban"]).replace(",",".")
        Chuoi_So_luong_ton = "SL Tồn " + str(Tivi["So_luong_Ton"])
        Chuoi_Hinh='<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'        
        Chuoi_Loai_Tivi = "Thuộc loại: " + Tivi["Nhom_Tivi"]["Ten"] + "<br/>"
        Chuoi_Ky_hieu = "Ký hiệu:" + Tivi["Ky_hieu"] + "<br/>"
        Chuoi_SL_Ton = "Số lượng tồn:" + str(Tivi["So_luong_Ton"]) + "<br/>"
        Chuoi_Thong_tin='<div class="btn" style="text-align:left">' + \
                 Tivi["Ten"] + "<br />" + Chuoi_Don_gia_Ban + "<br/>" + \
                 Chuoi_SL_Ton + \
                 '''<a href="/Quan_ly_Ban_hang/CapNhat/''' + Tivi["Ma_so"] +'''/">Cập nhật</a>'''+ '</div>'
        Chuoi_HTML ='<div class="col-md-4" >' +  \
                Chuoi_Hinh + Chuoi_Thong_tin + '</div>' 
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach += '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)

def Tao_Chuoi_HTML_Doanh_thu_nhan_vien(Danh_sach_Thong_ke, dic_ma_so):
    Ngay = "Ngày: " + datetime.now().strftime('%d-%m-%Y')
    Chuoi_HTML_Danh_sach = '<div class="container"><h3>Thống kê Doanh thu theo Nhân viên</h3><br/><h5>' + Ngay + '</h5></div>'
    for ma, ho_ten in dic_ma_so.items():

        Chuoi_Tong_tien = "...Tổng tiền: {:,}".format(sum(Tivi['Tien'] for Tivi in Danh_sach_Thong_ke if ma == Tivi['Ma_so'])).replace(",",".")

        Chuoi_HTML_Danh_sach += '<br><h4 class="ho_ten">Nhân viên ' + ho_ten + Chuoi_Tong_tien + "</h4>"
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
        Chuoi_HTML_Danh_sach += header
        for Tivi in Danh_sach_Thong_ke:
            if ma == Tivi['Ma_so']:
                Chuoi_HTML = '''
                    <div class="dong">
                    <div class="cot">''' + str(stt) + '''</div>
                    <div class="cot">''' + Tivi['Ten'] + '''</div>
                    <div class="cot">''' + str(Tivi['So_luong']) + '''</div>
                    <div class="cot">''' + "{:,}".format(Tivi["Don_gia"]).replace(",", ".") + '''</div>
                    <div class="cot">''' + "{:,}".format(Tivi["Tien"]).replace(",", ".") + '''</div>
                    </div>
                    '''
                stt += 1

                Chuoi_HTML_Danh_sach += Chuoi_HTML

        Chuoi_HTML_Danh_sach += '</div>'
    return Markup(Chuoi_HTML_Danh_sach)


def Tao_Chuoi_HTML_Thong_ke_SL_Ton_Tivi(Danh_sach_Thong_ke):
    Ngay = "Ngày: " + datetime.now().strftime('%d-%m-%Y') 
    #Chuoi_Tong_tien = "...Tổng tiền: {:,}".format(sum(Tivi['Tien'] for Tivi in Danh_sach_Thong_ke)).replace(",",".") 
    
    Chuoi_HTML_Danh_sach = '<div class="container"><h3>Thống kê Số lượng Tồn</h3><br/><h5>' + Ngay + '</h5></div>'
    Chuoi_HTML_Danh_sach += '<div class="row" >'
    
    stt = 1
    header = '''
        <div class="dong" >
        <div class="cot">STT</div>
        <div class="cot">Nhóm Tivi</div>
        <div class="cot">Số lượng tồn</div>
        </div>
        '''  
    Chuoi_HTML_Danh_sach +=header

    for key, value in Danh_sach_Thong_ke.items():
        Chuoi_HTML = '''
        <div class="dong">
        <div class="cot">'''+ str(stt) +'''</div>
        <div class="cot">'''+ key +'''</div>
        <div class="cot">'''+ str(value) +'''</div>
        
        </div>
        '''     
        stt += 1

        
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach += '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)


def Tao_Chuoi_HTML_Doanh_thu_Tivi(Danh_sach_Thong_ke):
    Ngay = "Ngày: " + datetime.now().strftime('%d-%m-%Y')
    Chuoi_Tong_tien = "...Tổng tiền: {:,}".format(sum(Tivi['Tien'] for Tivi in Danh_sach_Thong_ke)).replace(",",".")

    Chuoi_HTML_Danh_sach = '<div class="container"><h3>Thống kê Doanh thu theo Tivi</h3><br/><h5>' + Ngay + '... Tổng tiền:' + Chuoi_Tong_tien + '</h5></div>'
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
    Chuoi_HTML_Danh_sach += header

    for Tivi in Danh_sach_Thong_ke:
        Chuoi_HTML = '''
            <div class="dong">
            <div class="cot">''' + str(stt) + '''</div>
            <div class="cot">''' + Tivi['Ten'] + '''</div>
            <div class="cot">''' + str(Tivi['So_luong']) + '''</div>
            <div class="cot">''' + "{:,}".format(Tivi["Don_gia"]).replace(",", ".") + '''</div>
            <div class="cot">''' + "{:,}".format(Tivi["Tien"]).replace(",", ".") + '''</div>
            </div>
            '''
        stt += 1

        Chuoi_HTML_Danh_sach += Chuoi_HTML

    Chuoi_HTML_Danh_sach += '</div>'
    return Markup(Chuoi_HTML_Danh_sach)
