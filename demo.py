import random
import pandas as pd

# Đọc dữ liệu từ file Excel
def doc_du_lieu_tu_excel(duong_dan):
    df = pd.read_excel(duong_dan)
    khach_moi = list(set(df['Nguoi1'].tolist() + df['Nguoi2'].tolist()))
    quan_he = {(row['Nguoi1'], row['Nguoi2']): row['MoiQuanHe'] for _, row in df.iterrows()}
    return khach_moi, quan_he

# Đọc dữ liệu với đường dẫn
khach_moi, quan_he = doc_du_lieu_tu_excel(r'D:\ai\data.xlsx')

# Cấu hình cơ bản
KICH_THUOC_QUAN_THE = 100
SO_THE_HE = 1000
TY_LE_DOT_BIEN = 0.1

điểm_quan_he = {
    'vo_chong': 2000,
    'anh_chi_em_ruot': 900,
    'cha_me_con': 700,
    'anh_chi_em_ho': 500,
    'ho_hang': 300,
    'ban_be': 100,
    'khong_quen': 0
}

# Giới hạn số người mỗi bàn
gioi_han_so_nguoi = 5
    
# Hàm tính điểm thân thiết cho một bàn
def tinh_diem_ban(ban):
    diem = 0
    for i in range(len(ban)):
        for j in range(i + 1, len(ban)):
            cap = (ban[i], ban[j]) if (ban[i], ban[j]) in quan_he else (ban[j], ban[i])
            diem += điểm_quan_he.get(quan_he.get(cap, 'khong_quen'), 0)
    return diem

# Hàm đánh giá toàn bộ sơ đồ
def danh_gia(so_do):
    return sum(tinh_diem_ban(ban) for ban in so_do)

# Tạo cá thể ngẫu nhiên
def tao_ca_the():
    khach_ngau_nhien = khach_moi[:]
    random.shuffle(khach_ngau_nhien)
    return [khach_ngau_nhien[i:i + gioi_han_so_nguoi] for i in range(0, len(khach_ngau_nhien), gioi_han_so_nguoi)]

# Chọn lọc cá thể tốt
def chon_loc(quan_the):
    quan_the.sort(key=danh_gia, reverse=True)
    return quan_the[:len(quan_the) // 2]

# Lai ghép hai cá thể
def lai_ghep(cha, me):
    con = []
    for i in range(len(cha)):
        con.append(random.choice([cha[i], me[i]]))
    return con

# Đột biến
def dot_bien(ca_the):
    if random.random() < TY_LE_DOT_BIEN:
        a, b = random.sample(range(len(khach_moi)), 2)
        ds_phang = sum(ca_the, [])
        ds_phang[a], ds_phang[b] = ds_phang[b], ds_phang[a]
        return [ds_phang[i:i + gioi_han_so_nguoi] for i in range(0, len(ds_phang), gioi_han_so_nguoi)]
    return ca_the

# Giải thuật di truyền
def thuat_toan_di_truyen():
    quan_the = [tao_ca_the() for _ in range(KICH_THUOC_QUAN_THE)]
    for _ in range(SO_THE_HE):
        quan_the = chon_loc(quan_the)
        con_cai = [dot_bien(lai_ghep(random.choice(quan_the), random.choice(quan_the))) for _ in range(KICH_THUOC_QUAN_THE)]
        quan_the.extend(con_cai)
    giai_phap_tot_nhat = max(quan_the, key=danh_gia)
    return giai_phap_tot_nhat, danh_gia(giai_phap_tot_nhat)

# Chạy thuật toán
giai_phap, diem_tot_nhat = thuat_toan_di_truyen()

# Hiển thị sơ đồ chỗ ngồi tối ưu và tìm các bàn có điểm cao nhất
print("Sơ đồ chỗ ngồi tối ưu:")
ban_tot_nhat = []
diem_ban_tot_nhat = -1

for i, ban in enumerate(giai_phap):
    diem_ban = tinh_diem_ban(ban)
    print(f"Bàn {i + 1}: {', '.join(ban)} - Điểm: {diem_ban}")
    if diem_ban > diem_ban_tot_nhat:
        diem_ban_tot_nhat = diem_ban
        ban_tot_nhat = [(i + 1, ban)]
    elif diem_ban == diem_ban_tot_nhat:
        ban_tot_nhat.append((i + 1, ban))

# Hiển thị các bàn có điểm cao nhất
print(f"\nCác bàn có điểm số cao nhất (Điểm: {diem_ban_tot_nhat}):")
for ban in ban_tot_nhat:
    print(f"Bàn {ban[0]} - Thành viên: {', '.join(ban[1])}")
