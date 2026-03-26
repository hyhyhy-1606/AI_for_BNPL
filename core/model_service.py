import joblib
import pandas as pd

model = joblib.load("model.pkl")

features = [
    'Customer_Age',
    'Annual_Income',
    'Credit_Score',
    'Purchase_Amount',
    'Gender',
    'Purchase_Category',
    'BNPL_Provider',
    'Device_Type',
    'Connection_Type',
    'Checkout_Time_Seconds',
    'Browser',
    'Installment_Months',
    'Monthly_Payment',
    'Payment_to_Income'
]


def predict_default(customer):
    df = pd.DataFrame([customer])

    # 🔥 đảm bảo đủ cột
    for col in features:
        if col not in df.columns:
            df[col] = 0

    df = df[features]
    df = df.fillna(0)

    return model.predict_proba(df)[0][1]


def recommend_installment(customer, amount):
    results = []

    for i in range(1, 13):
        monthly = amount / i

        c = customer.copy()
        c['Purchase_Amount'] = amount

        income = c['Annual_Income'] if c['Annual_Income'] > 0 else 1

        # 🔥 luôn add đủ feature
        c['Installment_Months'] = i
        c['Monthly_Payment'] = monthly
        c['Payment_to_Income'] = monthly / income

        risk = predict_default(c)

        results.append({
            "months": i,
            "monthly": round(monthly, 0),
            "risk": round(float(risk), 4)
        })

    return sorted(results, key=lambda x: x["risk"])