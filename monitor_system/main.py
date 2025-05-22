# app.py
from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)


# -----------------------------------------------------------------------------
# 1) Simulate incoming alerts from System #1 and keep them in memory
# -----------------------------------------------------------------------------
def get_alerts():
    types = (
        ["Normal Traffic"] * 70
        + ["SQL Injection"] * 10
        + ["Path Traversal"] * 3
        + ["Denial of Service"] * 17
    )
    random.shuffle(types)
    servers = ["Server A", "Server B", "Server C"]
    alerts = []
    base_time = 35
    for i in range(1, 21):
        t = types[i - 1]
        minute = (base_time + (i // 60)) % 60
        second = (22 + i % 60) % 60
        hour = 14 + (base_time + i // 60) // 60
        if hour >= 24:
            hour %= 24
        alerts.append(
            {
                "id": i,
                "type": t,
                "timestamp": f"{hour:02d}:{minute:02d}:{second:02d}",
                "status": (
                    "สูง"
                    if t == "Denial of Service"
                    else ("กลาง" if t == "SQL Injection" else "ต่ำ")
                ),
                "ip": f"192.168.1.{i}",
                "server": random.choice(servers),
                "dataset": "",
            }
        )
    return alerts


# Global store
alerts_store = get_alerts()
dataset_options = ["Dataset 1", "Dataset 2", "Dataset 3", "Dataset 4"]


# -----------------------------------------------------------------------------
# 2) Home & Alert Filtering
# -----------------------------------------------------------------------------
@app.route("/")
def index():
    alerts = list(alerts_store)  # copy
    sel_types = request.args.getlist("attack_types")
    sel_servers = request.args.getlist("server_types")

    if sel_types:
        alerts = [a for a in alerts if a["type"] in sel_types]
    if sel_servers:
        alerts = [a for a in alerts if a["server"] in sel_servers]

    return render_template(
        "index.html",
        alerts=alerts,
        selected_types=sel_types,
        selected_servers=sel_servers,
    )


# -----------------------------------------------------------------------------
# 3) Server Status Page
# -----------------------------------------------------------------------------
@app.route("/server_status")
def server_status():
    server_data = {
        "Server A": "Online",
        "Server B": "Online",
        "Server C": "Maintenance",
        "Server D": "Offline",
    }
    return render_template("server_status.html", server_data=server_data)


# -----------------------------------------------------------------------------
# 4) Classification Model Selection
# -----------------------------------------------------------------------------
@app.route("/classification_model", methods=["GET"])
def classification_model():
    models = [
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
    return render_template("classification_model.html", model_info_list=models)


@app.route("/use_model", methods=["POST"])
def use_model():
    chosen = request.form.get("selected_model")
    return render_template("model_selected.html", model_name=chosen)


# -----------------------------------------------------------------------------
# 5) Training-Data Page & Trainer
# -----------------------------------------------------------------------------
@app.route("/training_data")
def training_data():
    return render_template("training_data.html", training_data_options=dataset_options)


@app.route("/train_model", methods=["POST"])
def train_model():
    tag = request.form.get("tag")
    desc = request.form.get("description")
    ds = request.form.get("dataset")
    accuracy = random.randint(85, 95)
    return render_template(
        "model_selected.html", tag=tag, description=desc, dataset=ds, accuracy=accuracy
    )


# -----------------------------------------------------------------------------
# 6) Manage Alerts → assign to dataset or delete
# -----------------------------------------------------------------------------
@app.route("/manage_data")
def manage_data():
    return render_template(
        "manage_data.html", alerts=alerts_store, dataset_options=dataset_options
    )


@app.route("/assign_dataset", methods=["POST"])
def assign_dataset():
    rec_id = int(request.form["id"])
    ds = request.form["dataset"]
    for a in alerts_store:
        if a["id"] == rec_id:
            a["dataset"] = ds
            break
    return redirect(url_for("manage_data"))


@app.route("/delete_alert", methods=["POST"])
def delete_alert():
    rec_id = int(request.form["id"])
    global alerts_store
    alerts_store = [a for a in alerts_store if a["id"] != rec_id]
    return redirect(url_for("manage_data"))


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
