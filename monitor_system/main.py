from flask import Flask, render_template, request
import random

app = Flask(__name__)


@app.route("/")
def index():
    alerts = get_alerts()
    search_query = request.args.get("search", "")

    if search_query:
        alerts = [
            alert for alert in alerts if search_query.lower() in alert["ip"].lower()
        ]

    return render_template("index.html", alerts=alerts, search_query=search_query)


def get_alerts():
    # สร้างข้อมูลการโจมตีแบบสุ่มตามสัดส่วนที่กำหนด
    attack_types = (
        ["Normal Traffic"] * 70
        + ["SQL Injection"] * 10
        + ["Path Traversal"] * 3
        + ["Denial of Service"] * 17
    )
    random.shuffle(attack_types)

    alerts = []
    base_time = 35  # เวลาที่เริ่มต้น เช่น 14:35:00

    for i in range(20):
        alert_type = attack_types[i]
        ip_address = f"192.168.1.{i + 1}"
        # สร้าง timestamp โดยไม่ใช้งานการหารหรือโมดูโลที่อาจนำไปสู่ข้อผิดพลาด
        minute = (base_time + (i // 60)) % 60
        second = (22 + (i % 60)) % 60
        hour = 14 + (base_time + i // 60) // 60  # คำนวณในกรณีที่ i เพิ่มขึ้นไปมาก

        # ควบคุมเวลาหากข้ามไปยังวันถัดไป
        if hour >= 24:
            hour = hour % 24

        # สร้าง time string สำหรับ timestamp
        timestamp = f"{hour:02}:{minute:02}:{second:02}"

        status = (
            "สูง"
            if alert_type == "Denial of Service"
            else ("กลาง" if alert_type == "SQL Injection" else "ต่ำ")
        )

        alerts.append(
            {
                "id": i + 1,
                "type": alert_type,
                "timestamp": timestamp,
                "status": status,
                "ip": ip_address,
            }
        )

    return alerts


if __name__ == "__main__":
    app.run(debug=True)
