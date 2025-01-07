 
from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from bson import ObjectId
class phonghoctest:
    map: str
    tenp: str
    thoigianSD: str
    thoigianHSD: str
    
class diemdanhtest:
    mabh:str
    mamh: str
    mssv: str
    thoigianH: str
    trangthai: str
    
class buoihoctest:
    mabh: str
    mamh:str
    map: str
    gioBD: str
    gioKT: str
    


def str_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

# Pydantic models for validation

class SinhVien(BaseModel):
    name: str
    email: str
    password: str
    mssv: str
    diemchuyencan: Optional[List]  # Array type field (List)
    HocKy: str

    class Config:
        orm_mode = True

    def to_dict(self):
        return {**self.dict(), "_id": str(self.id)}

class BuoiHoc(BaseModel):
    MaBH: str
    MaMH: str  # Reference to MonHoc
    MaGVDD: str  # Reference to GiangVien
    MaSVHOC: List[str]  # List of references to SinhVien
    GioHoc: str
    GioKetThuc: str
    MaP: str

    class Config:
        orm_mode = True

    def to_dict(self):
        return {**self.dict(), "_id": str(self.id)}

class MonHoc(BaseModel):
    MaMon: str
    TenMon: str
    SoTC: int
    GioHoc: str
    GioKetThuc: str
    GVPhuTrach: str  # Reference to GiangVien
    HocKy: str
    SinhVienHoc: List[str]  # List of references to SinhVien

    class Config:
        orm_mode = True

    def to_dict(self):
        return {**self.dict(), "_id": str(self.id)}

class GiangVien(BaseModel):
    TenGv: str
    Email: str
    Password: str
    HocVi: Optional[str]
    MaGV: str
    ChuNhiem: Optional[str]

    class Config:
        orm_mode = True

    def to_dict(self):
        return {**self.dict(), "_id": str(self.id)}

class PhongHoc(BaseModel):
    MaP: str
    TenPhong: str
    TgianSuDung: Optional[str]
    TgianHetSuDung: Optional[str]

    class Config:
        orm_mode = True

    def to_dict(self):
        return {**self.dict(), "_id": str(self.id)}

class DiemDanh(BaseModel):
    MaDD: str
    MaSVDD: str  # Reference to SinhVien
    MaGVDD: str  # Reference to GiangVien
    MaBH: str  # Reference to BuoiHoc
    MaMH: str  # Reference to MonHoc
    GioDD: str
    GioSinhVienDD: str
    TrangThai: int  # Enum values [0, 1, 2]

    class Config:
        orm_mode = True

    def to_dict(self):
        return {**self.dict(), "_id": str(self.id)}