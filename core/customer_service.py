from core.db import info_col
from datetime import datetime


def save_customer(user_id, customer_data):
    # 🔥 Schema chuẩn theo dataset
    schema = {
        'Customer_Age': 0,
        'Annual_Income': 0.0,
        'Credit_Score': 0,
        'Purchase_Amount': 0.0,
        'Gender': 0,
        'Purchase_Category': 0,
        'BNPL_Provider': 0,
        'Device_Type': 0,
        'Connection_Type': 0,
        'Checkout_Time_Seconds': 0,
        'Browser': 0
    }

    # 🔥 Merge dữ liệu user nhập với schema
    full_customer = {**schema, **customer_data}

    # 🔥 Ép kiểu dữ liệu (rất quan trọng cho model)
    full_customer['Customer_Age'] = int(full_customer['Customer_Age'])
    full_customer['Annual_Income'] = float(full_customer['Annual_Income'])
    full_customer['Credit_Score'] = int(full_customer['Credit_Score'])
    full_customer['Purchase_Amount'] = float(full_customer['Purchase_Amount'])
    full_customer['Checkout_Time_Seconds'] = int(full_customer['Checkout_Time_Seconds'])

    # 🔥 Lưu DB
    info_col.insert_one({
        "user_id": user_id,
        "customer_data": full_customer,
        "created_at": datetime.utcnow()
    })