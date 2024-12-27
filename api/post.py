import requests
import datetime

def get_current_time():
    # Get the current time
    current_time = datetime.datetime.now()

    # Return the current time as a string (you can format it as you like)
    return current_time

api_fetch = "http://127.0.0.1:3001/auth"
api_post = "http://127.0.0.1:3001/auth/put"

# Payload for updating the record
payload = {
    "_id": "676e15742cca62d12b63077b",  # The _id of the record you want to update
    "TrangThai": 1 
}

# "send" holds the fields to send to the API
send = {
    "MADD": "",
    "TenGVDD": "",
    "TenSVDuocDD": "",
    "TenPhongHoc": "",
    "GioDiemDanh": "",
    "GioVaoHocCuaSV": "",
    "TrangThai": ""
}


def fetch_data():
    take = {
        "TenGVDD": "",
        "TenPhongHoc": "",
        "GioVaoHocCuaSV": ""
    }
    try:
        response = requests.get(api_fetch)

        # Checking if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract the required fields and update the take dictionary
            take["TenGVDD"] = data.get("TenGVDD", "")
            take["TenPhongHoc"] = data.get("TenPhongHoc", "")
            take["GioVaoHocCuaSV"] = data.get("GioVaoHocCuaSV", "")

            # Return the updated dictionary
            return take  # Return the updated take dictionary
        else:
            print(f"Error: Failed to retrieve data. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        # Catch network-related errors or invalid API URL
        print(f"Error occurred while fetching data: {e}")
        return None


def put(time, tenSVDD, take):
    print(f"take: {take}")  # Debugging line to check the structure of 'take'
    
    if not isinstance(take, dict):
        print("Error: 'take' is not a dictionary.")
        return
    
    # Set the values to the "send" dictionary
    send = {}
    send["TenGVDD"] = take.get("TenGVDD", "Default Name")  # Use .get() to avoid KeyError if key is missing
    send["TenPhongHoc"] = take.get("TenPhongHoc", "Default Room")
    send["GioVaoHocCuaSV"] = take.get("GioVaoHocCuaSV", "Default Time")
    send["TenSVDuocDD"] = tenSVDD
    send["GioVaoHocCuaSv"] = time

    # Check if the time is earlier than the student's scheduled entry time
    if time < take.get("GioVaoHocCuaSV", time):  # Default to 'time' if GioVaoHocCuaSV is not provided
        send["TrangThai"] = 1
    else:
        send["TrangThai"] = 0  # Set status to 1 if the student arrives on time or later
    
    # Sending a PUT request to the API with the payload
    try:
        response = requests.put(api_post, json=send)
        
        # Checking if the request was successful (status code 200)
        if response.status_code == 200:
            print(f"Updated record successfully")
        else:
            print(f"Failed to update record. Status code: {response.status_code}")
    except Exception as e:
        # Catch any exceptions during the API request
        print(f"Error occurred while making the API request: {e}")
