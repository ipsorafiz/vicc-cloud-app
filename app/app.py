from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <title>VICC Cloud Application</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                text-align: center;
                padding-top: 100px;
            }
            .card {
                background: white;
                display: inline-block;
                padding: 40px 70px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.10);
            }
            .online {
                color: green;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>VICC Cloud Application</h1>
            <p>Status: <span class="online">Online</span></p>
            <p>Environment: Microsoft Azure</p>
            <p>Version: 1.0</p>
        </div>
    </body>
    </html>
    """

@app.route("/api/status")
def status():
    return jsonify(
        status="online",
        environment="Microsoft Azure",
        version="1.0"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
