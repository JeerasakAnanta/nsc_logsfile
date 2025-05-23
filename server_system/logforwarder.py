#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System 1: Apache Access Log Tailer & Forwarder
"""

import time
import re
import json
import requests
import argparse
from pathlib import Path

# ---------------------------
# กำหนดพารามิเตอร์
# ---------------------------
parser = argparse.ArgumentParser(
    description="Forward Apache access.log entries to a monitoring service."
)
parser.add_argument(
    "--log-file",
    default="/var/log/apache2/access.log",
    help="Path to Apache access log file",
)
parser.add_argument(
    "--endpoint",
    default="http://localhost:5000/api/logs",
    help="Monitor service HTTP endpoint",
)
parser.add_argument(
    "--sleep", type=float, default=0.5, help="Seconds to wait when no new log line"
)
args = parser.parse_args()


# ---------------------------
# Regex สำหรับ Apache Common Log Format
# ---------------------------
LOG_PATTERN = re.compile(
    r"(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "
    r'"(?P<method>\S+)\s(?P<path>\S+)\s?(?P<proto>[^"]*)"\s'
    r"(?P<status>\d{3})\s(?P<size>\S+)"
)


def tail_file(path, sleep_sec):
    """Generator: คืนค่าแต่ละบรรทัดใหม่ในไฟล์แบบ tail -f"""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        # ไปอยู่ปลายไฟล์
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(sleep_sec)
                continue
            yield line.rstrip("\n")


def parse_apache_line(line):
    """Parse log line ด้วย regex, คืน dict หรือ None ถ้าไม่แมตช์"""
    m = LOG_PATTERN.match(line)
    if not m:
        return None
    d = m.groupdict()
    return {
        "ip": d["ip"],
        "timestamp": d["time"],
        "method": d["method"],
        "path": d["path"],
        "protocol": d["proto"],
        "status": int(d["status"]),
        "size": None if d["size"] == "-" else int(d["size"]),
    }


def forward_log(entry, endpoint):
    """ส่ง entry เป็น JSON ไปที่ endpoint"""
    try:
        resp = requests.post(endpoint, json=entry, timeout=5)
        resp.raise_for_status()
        print(f"[OK] Sent: {entry['ip']} {entry['path']} → {resp.status_code}")
    except Exception as e:
        print(f"[Error] Failed to send log: {e}")


def main():
    log_path = Path(args.log_file)
    if not log_path.exists():
        print(f"Log file not found: {log_path}")
        return

    print(f"▶︎ Tailing {log_path} → POST to {args.endpoint}")
    for line in tail_file(str(log_path), args.sleep):
        data = parse_apache_line(line)
        if data:
            forward_log(data, args.endpoint)


if __name__ == "__main__":
    main()
