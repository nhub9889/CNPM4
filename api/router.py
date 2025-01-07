from fastapi import APIRouter, HTTPException, Form, Depends
from mongodb import get_db
import threading
import subprocess
from flask import Flask, jsonify, request
import time
import asyncio
from schema import phonghoctest, buoihoctest, diemdanhtest
from pymongo import MongoClient
from model import phonghoc, buoihoc, diemdanh, BuoiHoc, PhongHoc, DiemDanh
from typing import List
import os
from pydantic import BaseModel, HttpUrl
from datetime import datetime


router = APIRouter()


@router.get("/phonghoc", response_model=List[PhongHoc])
async def get_all_rooms(db: MongoClient = Depends(get_db)):
    """
    API endpoint to fetch all rooms from the 'PHONGHOC' collection using the PhongHoc model.
    """
    try:
        # Access the 'PHONGHOC' collection from the database
        phonghoc_collection = db['PHONGHOC']

        # Fetch all the documents in the 'PHONGHOC' collection, projecting the necessary fields
        phonghoc_list = phonghoc_collection.find({}, {"_id": 0, "MaP": 1, "TenPhong": 1, "TgianSuDung": 1, "TgianHetSuDung": 1})

        # Convert the result to a list of dictionaries
        phonghoc_data = list(phonghoc_list)

        # If no rooms found, raise 404
        if not phonghoc_data:
            raise HTTPException(status_code=404, detail="No rooms found")

        # Ensure the key names match the frontend expectations (map, tenp)
        for room in phonghoc_data:
            room['MaP'] = room.pop('MaP')
            room['TenPhong'] = room.pop('TenPhong')

        return phonghoc_data

    except Exception as e:
        # If any exception occurs, return a 500 error with the exception message
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/buoihoc", response_model=List[BuoiHoc])
async def get_buoi_hoc_by_map(MaP: str, db: MongoClient = Depends(get_db)):
    """
    API endpoint to fetch all 'buổi học' with the given 'map' from MongoDB.
    """
    try:
        # Access the 'buoihoctest' collection
        buoihoc_collection = db['BUOIHOC']

        # Get current time (now) for comparison and convert to datetime object
        now = datetime.now()

        # Fetch all sessions for the given room (MaP)
        buoi_hoc_list = buoihoc_collection.find({"MaP": MaP})

        # Filter out sessions based on current time
        filtered_sessions = []
        for session in buoi_hoc_list:
            # Parse GioHoc and GioKetThuc into datetime objects
            gio_hoc = datetime.strptime(session["GioHoc"], "%d/%m/%Y %H:%M")
            gio_ket_thuc = datetime.strptime(session["GioKetThuc"], "%d/%m/%Y %H:%M")

            # Check if the current time is between GioHoc and GioKetThuc
            if gio_hoc <= now <= gio_ket_thuc:
                filtered_sessions.append(BuoiHoc(**session))

        # If no sessions found for the given room and time range
        if not filtered_sessions:
            raise HTTPException(status_code=404, detail="No sessions found for this room at the current time")

        return filtered_sessions

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    

    
@router.post("/diemdanh", response_model=DiemDanh)
async def create_diemdanh(diemdanh_data: DiemDanh, db: MongoClient = Depends(get_db)):
    """
    API endpoint to create a new diemdanh (attendance record).
    """
    try:
        # Access the 'diemdanh' collection in MongoDB
        diemdanh_collection = db['DIEMDANH']

        # Convert the Pydantic model to a dictionary (excluding the _id)
        diemdanh_dict = diemdanh_data.dict(exclude_unset=True)
        # Insert the new diemdanh document into the MongoDB collection
        result = diemdanh_collection.insert_one(diemdanh_dict)

        # Check if the insert was successful
        if result.inserted_id:
            # Add the inserted _id to the diemdanh_data and return it
            diemdanh_data_with_id = DiemDanh(**diemdanh_dict, MaDD=str(result.inserted_id))
            return diemdanh_data_with_id
        else:
            raise HTTPException(status_code=500, detail="Failed to create diemdanh")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")




@router.get("/check_diemdanh")
async def check_diemdanh(mabh: str, mssv: str, db: MongoClient = Depends(get_db)):
    """
    API endpoint to check if a diemdanh (attendance record) exists based on mabh (course ID) and mssv (student ID).
    """
    try:
        # Access the 'diemdanh' collection in MongoDB
        diemdanh_collection = db['DIEMDANH']

        # Query MongoDB for a record with matching mabh and mssv
        diemdanh_record = diemdanh_collection.find_one({"MaBH": mabh, "MaSVDD": mssv})

        # If no record is found, return a 404 with message "0"
        if not diemdanh_record:
            return {"exists": "0"}  # or you can return {"exists": False} as well

        # If record exists, return a response with message "1"
        return {"exists": "1"}  # or you can return {"exists": True} for better clarity

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/check_sinhvien")
async def check_sinhvien_in_buoi_hoc(ma_bh: str, ma_sv: str, db: MongoClient = Depends(get_db)):
    """
    API endpoint to check if a student (MaSV) is in the list of students (MaSVHOC) for a given session (MaBH).
    """
    try:
        # Truy vấn dữ liệu BuoiHoc từ MongoDB
        buoi_hoc_collection = db['BUOIHOC']  # Tên collection trong MongoDB
        buoi_hoc = buoi_hoc_collection.find_one({"MaBH": ma_bh})

        # Kiểm tra nếu không có buổi học nào với MaBH tương ứng
        if not buoi_hoc:
            raise HTTPException(status_code=404, detail="Buổi học không tồn tại")

        # Kiểm tra nếu MaSV có trong danh sách MaSVHOC
        if ma_sv in buoi_hoc.get("MaSVHOC", []):
            return {"message": "Sinh viên có mặt trong buổi học."}
        else:
            return {"message": "Sinh viên không có mặt trong buổi học."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
   
class RequestData(BaseModel):
    MaBH: str
    MaGVDD: str
    MaMH: str
    GioHoc: str
    GioKetThuc: str

@router.post("/run")
async def run_recognize(data: RequestData):
    try:
        # Path to Python executable và script
        venv_python = r'C:\Users\Lenovo\miniconda3\envs\face-dev\python.exe'
        script_path = os.path.join(os.path.dirname(os.getcwd()), 'recognize.py')

        # Tạo command
        command = [
            venv_python,
            script_path,
            str(data.MaBH),
            str(data.MaGVDD),
            str(data.MaMH),
            str(data.GioHoc),
            str(data.GioKetThuc)
        ]

        # Mở terminal mới và chạy script
       
        process = subprocess.Popen(
            ['start', 'cmd', '/k'] + command,
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
       

        return {"message": "recognize.py has been started in a new terminal"}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))