from core.db import predict_col
from core.model_service import recommend_installment


def run_prediction(user_id, customer, amount):
    # 🔥 copy tránh ghi đè dữ liệu gốc
    c = customer.copy()
    c["Purchase_Amount"] = amount

    # 🔥 gọi đúng hàm
    results = recommend_installment(c, amount)

    if not results:
        return []

    # 🔥 chuẩn hóa data trả về
    data = []
    for r in results:
        data.append({
            "months": r["months"],
            "monthly": r["monthly"],
            "risk": r["risk"]
        })

    # 🔥 chọn phương án tốt nhất
    best = min(data, key=lambda x: x["risk"])

    # 🔥 lưu DB
    predict_col.insert_one({
        "user_id": user_id,
        "customer": c,
        "amount": amount,
        "results": data,
        "best_option": best
    })

    return data