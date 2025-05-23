# การตรวจจับเหตุการณ์ผิดปกติจากข้อมูลการจราจรทางคอมพิวเตอร์  (Anomaly Detection From Log Files)

- โครงการสำหรับ การตรวจจับเหตุการณ์ผิดปกติจากข้อมูลการจราจรทางคอมพิวเตอร์ โดยใช้เทคนิคการเรียนรู้ของเครื่อง (Machine Learning) และการวิเคราะห์ข้อมูล (Data Analysis) เพื่อช่วยในการตรวจสอบและวิเคราะห์เหตุการณ์ที่เกิดขึ้นในระบบคอมพิวเตอร์  
- 
##  flow logs app 
![app flow](docs/logs_app_flow.png)

# System Architecture 

-  Single Servers  Anomaly Detection From Log Files
-  ![Single Servers](./docs/image_Single_Servers.png)
-  Multi Servers Anomaly Detection From Log Files  
- ![Multi Servers](./docs/image_Multiple_servers.png)

## System 1 (LogForwarder)
- Sequence Diagram
```mermaid 
sequenceDiagram
    autonumber
    participant Tailer as LogForwarder
    participant Apache as Apache Access Log
    participant Monitor as Monitor System (HTTP)

    %% Initialization
    Tailer->>Apache: open("/var/log/apache2/access.log")
    Tailer->>Apache: seek to end of file

    loop continuously
        Apache-->>Tailer: new log line
        Tailer->>Tailer: parse_apache_line(line)
        alt parse success
            Tailer->>Monitor: HTTP POST /api/logs\n{ "ip":…, "path":…, … }
            alt 2xx response
                Monitor-->>Tailer: 204 No Content
                Tailer->>Tailer: print("[OK] Sent …")
            else error/timeout
                Monitor-->>Tailer: error/timeout
                Tailer->>Tailer: print("[Error] Failed to send …")
            end
        else parse fails
            Tailer->>Tailer: ignore line
        end
        Tailer->>Tailer: wait(sleep_sec) if no new line
    end
```

## System 2 (Monitor System) 

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Browser
    participant FlaskApp
    participant TemplateEngine

    %% 1) หน้าแรก + กรอง Alert
    User->>Browser: เปิดหน้า "/"
    Browser->>FlaskApp: GET /
    FlaskApp->>FlaskApp: get_alerts()
    FlaskApp->>TemplateEngine: render index.html (alerts, filters)
    TemplateEngine-->>FlaskApp: HTML
    FlaskApp-->>Browser: 200 OK + หน้า index

    %% 2) จัดการข้อมูลจากระบบที่ 1
    Browser->>FlaskApp: GET /manage_data
    FlaskApp->>TemplateEngine: render manage_data.html (alerts_store)
    TemplateEngine-->>FlaskApp: HTML
    FlaskApp-->>Browser: 200 OK + หน้า manage_data

    User->>Browser: กด “บันทึก” Dataset
    Browser->>FlaskApp: POST /assign_dataset {id, dataset}
    FlaskApp->>FlaskApp: update alerts_store
    FlaskApp-->>Browser: 302 Redirect ไป /manage_data
    Browser->>FlaskApp: GET /manage_data
    FlaskApp->>TemplateEngine: render manage_data.html (updated)
    TemplateEngine-->>FlaskApp: HTML
    FlaskApp-->>Browser: 200 OK + หน้า manage_data

    User->>Browser: กด “ลบ” Alert
    Browser->>FlaskApp: POST /delete_alert {id}
    FlaskApp->>FlaskApp: remove alert from alerts_store
    FlaskApp-->>Browser: 302 Redirect ไป /manage_data

    %% 3) ดูสถานะเซิร์ฟเวอร์
    Browser->>FlaskApp: GET /server_status
    FlaskApp->>TemplateEngine: render server_status.html (server_data)
    TemplateEngine-->>FlaskApp: HTML
    FlaskApp-->>Browser: 200 OK + หน้า server_status

    %% 4) เลือกโมเดลจำแนกประเภท
    Browser->>FlaskApp: GET /classification_model
    FlaskApp->>TemplateEngine: render classification_model.html (model_info_list)
    TemplateEngine-->>FlaskApp: HTML
    FlaskApp-->>Browser: 200 OK + หน้า classification_model

    User->>Browser: เลือก Radio + กด “ใช้งานโมเดลนี้”
    Browser->>FlaskApp: POST /use_model {selected_model}
    FlaskApp->>TemplateEngine: render model_selected.html (model_name)
    TemplateEngine-->>FlaskApp: HTML
    FlaskApp-->>Browser: 200 OK + หน้า model_selected

    %% 5) เลือกข้อมูลสำหรับฝึกอบรม
    Browser->>FlaskApp: GET /training_data
    FlaskApp->>TemplateEngine: render training_data.html (tags, description, datasets)
    TemplateEngine-->>FlaskApp: HTML
    FlaskApp-->>Browser: 200 OK + หน้า training_data

    User->>Browser: กรอก Form + กด “ฝึกอบรมโมเดล”
    Browser->>FlaskApp: POST /train_model {tag, description, dataset}
    FlaskApp->>FlaskApp: accuracy = random.randint(85,95)
    FlaskApp->>TemplateEngine: render model_selected.html (tag,description,dataset,accuracy)
    TemplateEngine-->>FlaskApp: HTML
    FlaskApp-->>Browser: 200 OK + หน้า model_selected
```