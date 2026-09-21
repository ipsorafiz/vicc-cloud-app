from flask import Flask, jsonify
from pathlib import Path
from datetime import datetime, timezone
import json
import html
import time
import requests

app = Flask(__name__)

APP_VERSION = "1.2"
ENVIRONMENT = "Microsoft Azure"
DATA_FILE = Path(__file__).with_name("services.json")


def load_services():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def check_service(service):
    name = service["name"]
    url = service["url"]
    timeout = service.get("timeout", 5)

    started = time.perf_counter()

    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "VICC-Service-Monitor/1.2"}
        )

        response_time_ms = round((time.perf_counter() - started) * 1000)

        if 200 <= response.status_code < 400:
            if response_time_ms > 2000:
                status = "degraded"
            else:
                status = "online"
        elif 400 <= response.status_code < 500:
            status = "degraded"
        else:
            status = "offline"

        return {
            "name": name,
            "url": url,
            "status": status,
            "http_status": response.status_code,
            "response_time_ms": response_time_ms
        }

    except requests.RequestException:
        response_time_ms = round((time.perf_counter() - started) * 1000)

        return {
            "name": name,
            "url": url,
            "status": "offline",
            "http_status": None,
            "response_time_ms": response_time_ms
        }


def check_all_services():
    return [check_service(service) for service in load_services()]


def calculate_overall_status(services):
    statuses = [service["status"] for service in services]

    if "offline" in statuses:
        return "outage"

    if "degraded" in statuses:
        return "degraded"

    return "operational"


def current_timestamp():
    return datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M:%S UTC")


@app.route("/")
def home():
    services = check_all_services()
    overall = calculate_overall_status(services)
    timestamp = current_timestamp()

    status_text = {
        "operational": "Alle überwachten Services sind betriebsbereit",
        "degraded": "Einzelne Services sind eingeschränkt",
        "outage": "Mindestens ein Service ist nicht erreichbar"
    }

    overall_class = {
        "operational": "green",
        "degraded": "yellow",
        "outage": "red"
    }

    service_text = {
        "online": "Online",
        "degraded": "Eingeschränkt",
        "offline": "Offline"
    }

    rows = ""

    for service in services:
        name = html.escape(service["name"])
        url = html.escape(service["url"])
        status = service["status"]
        label = service_text.get(status, status)

        http_status = (
            str(service["http_status"])
            if service["http_status"] is not None
            else "-"
        )

        rows += f"""
        <div class="service">
            <div>
                <div class="service-name">{name}</div>
                <div class="service-url">{url}</div>
            </div>

            <div class="service-result">
                <div class="status">
                    <span class="dot {status}"></span>
                    {label}
                </div>

                <div class="details">
                    HTTP {http_status} · {service["response_time_ms"]} ms
                </div>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>IT Service Monitor</title>

        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                color: #1f2937;
            }}

            .container {{
                width: 90%;
                max-width: 950px;
                margin: 55px auto;
            }}

            h1 {{
                margin-bottom: 8px;
                font-size: 32px;
            }}

            .subtitle {{
                margin-top: 0;
                color: #6b7280;
            }}

            .overall {{
                background: white;
                border-radius: 12px;
                padding: 24px;
                margin: 25px 0 20px 0;
                box-shadow: 0 3px 12px rgba(0,0,0,0.08);
                display: flex;
                align-items: center;
                gap: 14px;
                font-size: 20px;
                font-weight: bold;
            }}

            .overall-indicator {{
                width: 16px;
                height: 16px;
                border-radius: 50%;
            }}

            .green {{
                background: #16a34a;
            }}

            .yellow {{
                background: #eab308;
            }}

            .red {{
                background: #dc2626;
            }}

            .services {{
                background: white;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 3px 12px rgba(0,0,0,0.08);
            }}

            .service {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 30px;
                padding: 20px 25px;
                border-bottom: 1px solid #e5e7eb;
            }}

            .service:last-child {{
                border-bottom: none;
            }}

            .service-name {{
                font-weight: bold;
                margin-bottom: 5px;
            }}

            .service-url {{
                color: #6b7280;
                font-size: 13px;
            }}

            .service-result {{
                min-width: 170px;
                text-align: right;
            }}

            .status {{
                display: flex;
                justify-content: flex-end;
                align-items: center;
                gap: 8px;
                font-weight: bold;
            }}

            .dot {{
                width: 11px;
                height: 11px;
                border-radius: 50%;
                display: inline-block;
            }}

            .online {{
                background: #16a34a;
            }}

            .degraded {{
                background: #eab308;
            }}

            .offline {{
                background: #dc2626;
            }}

            .details {{
                margin-top: 5px;
                font-size: 13px;
                color: #6b7280;
            }}

            .footer {{
                margin-top: 22px;
                color: #6b7280;
                font-size: 14px;
                line-height: 1.6;
            }}

            .api-link {{
                display: inline-block;
                margin-top: 12px;
                color: #2563eb;
                text-decoration: none;
            }}

            .api-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>

    <body>
        <div class="container">

            <h1>IT Service Monitor</h1>
            <p class="subtitle">
                Cloudbasierter und konfigurierbarer Statusmonitor für IT-Services
            </p>

            <div class="overall">
                <span class="overall-indicator {overall_class[overall]}"></span>
                {status_text[overall]}
            </div>

            <div class="services">
                {rows}
            </div>

            <div class="footer">
                Letzte Prüfung: {timestamp}<br>
                Environment: {ENVIRONMENT}<br>
                Version: {APP_VERSION}<br>

                <a class="api-link" href="/api/status">
                    REST-API anzeigen
                </a>
            </div>

        </div>
    </body>
    </html>
    """


@app.route("/api/status")
def api_status():
    services = check_all_services()
    overall = calculate_overall_status(services)

    return jsonify(
        application="IT Service Monitor",
        overall_status=overall,
        environment=ENVIRONMENT,
        version=APP_VERSION,
        timestamp=current_timestamp(),
        services=services
    )


@app.route("/health")
def health():
    return jsonify(
        status="healthy",
        application="IT Service Monitor",
        version=APP_VERSION
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)