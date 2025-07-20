import requests
import time

# === بيانات الحساب الحقيقي ===
USERNAME = input("اسم مستخدم انستغرام: ")
PASSWORD = input("كلمة السر: ")

# === بيانات الحساب المستهدف ===
TARGET_USER_ID = input("user_id الحساب المستهدف (مثلاً 123456789): ")
REASON_ID = input("رقم نوع البلاغ (مثلاً 1=تحرش، 2=انتحال...): ")
REPORT_COUNT = int(input("كم عدد البلاغات اللي تريد ترسلها؟ "))

# === إعدادات الاتصال ===
session = requests.Session()
login_url = "https://www.instagram.com/accounts/login/ajax/"

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/accounts/login/",
}

# 1. جلب csrf token
r = session.get("https://www.instagram.com/accounts/login/", headers=headers)
csrf = r.cookies.get("csrftoken")
headers["X-CSRFToken"] = csrf

# 2. تسجيل الدخول
login_data = {
    "username": USERNAME,
    "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:0:{PASSWORD}",
    "queryParams": {},
    "optIntoOneTap": "false"
}
resp = session.post(login_url, data=login_data, headers=headers, allow_redirects=True)
print("نتيجة تسجيل الدخول:", resp.text)
if not resp.json().get("authenticated"):
    print("❌ فشل تسجيل الدخول! راجع البيانات أو حاول من متصفح آخر.")
    exit()

print("✅ تم تسجيل الدخول بنجاح، البدء في إرسال البلاغات...")

# 3. إرسال البلاغات
report_url = f"https://www.instagram.com/users/{TARGET_USER_ID}/report/"
report_data = {
    "reason_id": REASON_ID,
    "source_name": "profile",
    "surface": "profile",
}

headers["X-CSRFToken"] = session.cookies.get("csrftoken")

for i in range(REPORT_COUNT):
    r = session.post(report_url, data=report_data, headers=headers)
    print(f"بلاغ رقم {i+1}: الحالة {r.status_code}, الرد: {r.text}")
    # انتظر ثانيتين بين كل بلاغ حتى لا يتحظر الحساب بسرعة
    time.sleep(2)