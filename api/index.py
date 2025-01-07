from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router  # Giả sử bạn có file router.py chứa các routes của API

app = FastAPI()

# Cấu hình CORS cho phép frontend trên localhost:5500 truy cập
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP (GET, POST, PUT, DELETE, v.v.)
    allow_headers=["*"],  # Cho phép tất cả các headers
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],  # Chỉ cho phép yêu cầu từ địa chỉ này
)

# Thêm các route từ file router.py
app.include_router(router)
