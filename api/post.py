import requests
import datetime


# API endpoints
api_DD = "http://127.0.0.1:8000/diemdanh"
api_checkDD = "http://127.0.0.1:8000/check_diemdanh"
api_checkSV = "http://127.0.0.1:8000/check_sinhvien"

# Function to get the current time
def get_current_time():
    current_time = datetime.datetime.now()
    return current_time.strftime("%d/%m/%Y %H:%M")  # Return as string in expected format

# Function to check the attendance status based on class start time and check-in time
def check_attendance_status(gio_hoc, gio_vao):
    """
    Returns:
    - 1 if the student is late (i.e., check-in time is more than 15 minutes after class start time)
    - 0 if the student is on time (check-in time is within 15 minutes of class start time)
    """
    gio_hoc_time = datetime.datetime.strptime(gio_hoc, "%d/%m/%Y %H:%M")
    gio_vao_time = datetime.datetime.strptime(gio_vao, "%d/%m/%Y %H:%M")
    time_diff = gio_vao_time - gio_hoc_time

    if time_diff > datetime.timedelta(minutes=15):
        return 2  # Student is late
    else:
        return 1  # Student is on time


def diem_danh(mssv, MaBH, MaGVDD, MaMon, GioHoc, GioKetThuc, GioVao):
    try:
        # Kiểm tra điểm danh - sử dụng parameters
        check_url = f"{api_checkDD}?mabh={MaBH}&mssv={mssv}"
        response = requests.get(check_url)

        if response.status_code != 200:
            print(f"Lỗi khi gọi API kiểm tra trạng thái điểm danh: {response.status_code}")
            return None

        check_data = response.json()
        if check_data.get("exists") == "1":
            print("Sinh viên đã điểm danh rồi.")
            return {"message": "Sinh viên đã điểm danh rồi."}

        # Kiểm tra sinh viên - sử dụng parameters
        check_url_sinhvien = f"{api_checkSV}?ma_bh={MaBH}&ma_sv={mssv}"
        response = requests.get(check_url_sinhvien)

        if response.status_code != 200:
            print(f"Lỗi khi gọi API kiểm tra sự có mặt của sinh viên: {response.status_code}")
            return None

        check_data_sinhvien = response.json()
        if "message" in check_data_sinhvien and check_data_sinhvien["message"] == "Sinh viên không có mặt trong buổi học.":
            print("Sinh viên không có mặt trong buổi học.")
            return {"message": "Sinh viên không có mặt trong buổi học."}

        # Nếu sinh viên có mặt, tiến hành điểm danh
        status = check_attendance_status(GioHoc, GioVao)
        if status is None:
            print("Lỗi: Không thể kiểm tra thời gian.")
            return None

        # Chuẩn bị payload để gửi tới API điểm danh
        diemdanh_payload = {
            "MaSVDD": str(mssv),
            "MaDD": str(mssv+MaBH),
            "MaGVDD": str(MaGVDD),
            "MaBH": str(MaBH),
            "MaMH": str(MaMon),
            "GioDD": str(GioHoc),
            "GioSinhVienDD": str(GioVao),
            "TrangThai": status
        }

        # Gửi POST request để điểm danh với body
        response = requests.post(api_DD, json=diemdanh_payload)

        if response.status_code == 201:
            data = response.json()
            print("Điểm danh thành công:", data)
            return data
        else:
            print(f"Error: Không thể điểm danh. Mã lỗi: {response.status_code}", flush= True)
            print("Thông báo từ API:", response.json(), flush= True)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        return None