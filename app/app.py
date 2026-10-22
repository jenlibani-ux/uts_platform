from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html><head><title>Buku Tamu Digital</title>
    <style>body{font-family:Arial;background:#f0f4ff;display:flex;
    justify-content:center;align-items:center;height:100vh;margin:0}
    .card{background:#fff;padding:40px 60px;border-radius:12px;
    box-shadow:0 4px 20px rgba(0,0,0,.1);text-align:center}
    h1{color:#2c3e50}</style></head>
    <body><div class="card">
    <h1>📖 Buku Tamu Digital</h1>
    <p>Flask berjalan di port 8000</p>
    <p>UTS Teknologi Platform — Jenli Melinda Banik (26110023)</p>
    </div></body></html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
