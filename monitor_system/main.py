from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)


# สร้างข้อมูล alert เก็บในตัวแปร global เพื่อจำลองการรับจากระบบที่ 1
def get_alerts():
    attack_types = (
        ["Normal Traffic"] * 70
        + ["SQL Injection"] * 10
        + ["Path Traversal"] * 3
        + ["Denial of Service"] * 17
    )
    random.shuffle(attack_types)
    servers = ["Server A", "Server B", "Server C"]
    alerts = []
    base_time = 35
    for i in range(1, 21):
        typ = attack_types[i - 1]
        minute = (base_time + (i // 60)) % 60
        second = (22 + (i % 60)) % 60
        hour = 14 + (base_time + i // 60) // 60
        if hour >= 24:
            hour %= 24
        alerts.append(
            {
                "id": i,
                "type": typ,
                "timestamp": f"{hour:02}:{minute:02}:{second:02}",
                "status": (
                    "สูง"
                    if typ == "Denial of Service"
                    else ("กลาง" if typ == "SQL Injection" else "ต่ำ")
                ),
                "ip": f"192.168.1.{i}",
                "server": random.choice(servers),
                "dataset": "",  # ช่องเก็บชื่อ Dataset ที่เลือก
            }
        )
    return alerts


# สร้าง global store ครั้งเดียว
alerts_store = get_alerts()
dataset_options = ["Dataset 1", "Dataset 2", "Dataset 3", "Dataset 4"]


# หน้า Manage Data
@app.route("/manage_data")
def manage_data():
    return render_template(
        "manage_data.html", alerts=alerts_store, dataset_options=dataset_options
    )


# Assign dataset ให้รายการหนึ่งๆ
@app.route("/assign_dataset", methods=["POST"])
def assign_dataset():
    rec_id = int(request.form["id"])
    ds = request.form["dataset"]
    for a in alerts_store:
        if a["id"] == rec_id:
            a["dataset"] = ds
            break
    return redirect(url_for("manage_data"))


# ลบรายการแจ้งเตือน
@app.route("/delete_alert", methods=["POST"])
def delete_alert():
    rec_id = int(request.form["id"])
    global alerts_store
    alerts_store = [a for a in alerts_store if a["id"] != rec_id]
    return redirect(url_for("manage_data"))


# หน้าแรก
@app.route("/")
def index():
    alerts = alerts_store
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
            "tags": "Default Model",
            "accuracy": "95%",
            "description": "Detect anomalies",
            "data_source": "Dataset 1",
        },
        {
            "name": "CNN",
            "tags": "Default Model",
            "accuracy": "90%",
            "description": "Pattern detection",
            "data_source": "Dataset 2",
        },
        {
            "name": "SVM",
            "tags": "Default Model",
            "accuracy": "88%",
            "description": "Classify traffic",
            "data_source": "Dataset 3",
        },
        {
            "name": "KNN",
            "tags": "Default Model",
            "accuracy": "85%",
            "description": "Simple classifier",
            "data_source": "Dataset 4",
        },
        {
            "name": "GradientBoost",
            "tags": "Default Model",
            "accuracy": "82%",
            "description": "Boosted trees",
            "data_source": "Dataset 5",
        },
    ]
    return render_template("classification_model.html", model_info_list=model_info_list)


@app.route("/use_model", methods=["POST"])
def use_model():
    selected = request.form.get("selected_model")
    return render_template("model_selected.html", model_name=selected)


@app.route("/training_data")
def training_data():
    return render_template("training_data.html", training_data_options=dataset_options)


# เส้นทางสำหรับการฝึกอบรมโมเดล
@app.route("/train_model", methods=["POST"])
def train_model():
    selected_data = request.form.getlist("training_data")
    return f"Training model with: {', '.join(selected_data)}"


if __name__ == "__main__":
    app.run(debug=True)
