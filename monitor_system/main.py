from flask import Flask, render_template, request
import random

app = Flask(__name__)


@app.route("/")
def index():
    alerts = get_alerts()
    selected_types = request.args.getlist("attack_types")
    selected_servers = request.args.getlist("server_types")

    # กรองการโจมตีตามประเภทและเซิร์ฟเวอร์ที่เลือก
    if selected_types:
        alerts = [alert for alert in alerts if alert["type"] in selected_types]
    if selected_servers:
        alerts = [alert for alert in alerts if alert["server"] in selected_servers]

    return render_template(
        "index.html",
        alerts=alerts,
        selected_types=selected_types,
        selected_servers=selected_servers,
    )


@app.route("/server_status")
def server_status():
    # จำลองข้อมูลสถานะเซิร์ฟเวอร์
    server_data = {
        "Server A": "Online",
        "Server B": "Online",
        "Server C": "Maintenance",
        "Server D": "Offline",
    }
    return render_template("server_status.html", server_data=server_data)


@app.route("/classification_model", methods=["GET"])
def classification_model():
    model_info_list = [
        {
            "name": "Random Forest",
            "accuracy": "95%",
            "description": "Detect anomalies",
            "data_source": "Dataset 1",
        },
        {
            "name": "CNN",
            "accuracy": "90%",
            "description": "Pattern detection",
            "data_source": "Dataset 2",
        },
        {
            "name": "SVM",
            "accuracy": "88%",
            "description": "Classify traffic",
            "data_source": "Dataset 3",
        },
        {
            "name": "KNN",
            "accuracy": "85%",
            "description": "Simple classifier",
            "data_source": "Dataset 4",
        },
        {
            "name": "GradientBoost",
            "accuracy": "82%",
            "description": "Boosted trees",
            "data_source": "Dataset 5",
        },
    ]
    return render_template("classification_model.html", model_info_list=model_info_list)


@app.route("/use_model", methods=["POST"])
def use_model():
    selected = request.form.get("selected_model")
    # (ถ้าต้องการ หน่วงฝั่งเซิร์ฟเวอร์อีกชั้น)
    # time.sleep(random.randint(3,6))
    return render_template("model_selected.html", model_name=selected)


@app.route("/training_data")
def training_data():
    # จำลองข้อมูลที่สามารถใช้ฝึกโมเดล
    training_data_options = ["Dataset 1", "Dataset 2", "Dataset 3", "Dataset 4"]
    return render_template(
        "training_data.html", training_data_options=training_data_options
    )


# เส้นทางสำหรับการฝึกอบรมโมเดล
@app.route("/train_model", methods=["POST"])
def train_model():
    selected_data = request.form.getlist("training_data")
    # ในที่นี้คุณสามารถดำเนินการฝึกโมเดลของคุณด้วยข้อมูลที่เลือกได้
    return f"Training model with: {', '.join(selected_data)}"


def get_alerts():
    # สร้างข้อมูลการโจมตีแบบสุ่มตามสัดส่วนที่กำหนด
    attack_types = (
        ["Normal Traffic"] * 70
        + ["SQL Injection"] * 10
        + ["Path Traversal"] * 3
        + ["Denial of Service"] * 17
    )
    random.shuffle(attack_types)

    servers = ["Server A", "Server B", "Server C"]
    alerts = []
    base_time = 35  # เวลาที่เริ่มต้น เช่น 14:35:00

    for i in range(20):
        alert_type = attack_types[i]
        ip_address = f"192.168.1.{i + 1}"
        server = random.choice(servers)  # เลือกเซิร์ฟเวอร์แบบสุ่ม
        minute = (base_time + (i // 60)) % 60
        second = (22 + (i % 60)) % 60
        hour = 14 + (base_time + i // 60) // 60

        if hour >= 24:
            hour = hour % 24

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
                "server": server,
            }
        )

    return alerts


if __name__ == "__main__":
    app.run(debug=True)
