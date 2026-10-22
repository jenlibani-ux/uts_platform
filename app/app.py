from flask import Flask, request, redirect
import os
import time
import pymysql

app = Flask(__name__)

# Kredensial DB dari environment variable (di-set di docker-compose)
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_USER = os.environ.get('DB_USER', 'tamu')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'rahasia123')
DB_NAME = os.environ.get('DB_NAME', 'bukutamu')


def get_db():
    return pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


def wait_for_db(max_retry=30):
    for i in range(max_retry):
        try:
            conn = get_db()
            conn.close()
            print(f"[INIT] DB siap setelah percobaan ke-{i + 1}", flush=True)
            return True
        except Exception as e:
            print(f"[INIT] Menunggu DB ({i + 1}/{max_retry}): {e}", flush=True)
            time.sleep(2)
    return False


def init_table():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tamu (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(100) NOT NULL,
                pesan TEXT NOT NULL,
                waktu DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()
    print("[INIT] Tabel 'tamu' siap", flush=True)


@app.route('/')
def index():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT id, nama, pesan, waktu FROM tamu ORDER BY id DESC")
        rows = cur.fetchall()
    conn.close()

    daftar = "".join(
        f"<li><strong>{r['nama']}</strong> "
        f"<span style='color:#888'>({r['waktu']})</span><br>{r['pesan']}</li>"
        for r in rows
    ) or "<li><em>Belum ada tamu.</em></li>"

    return f"""
    <!DOCTYPE html>
    <html><head><title>Buku Tamu Digital</title>
    <style>
      body{{font-family:Arial;background:#f0f4ff;margin:0;padding:20px}}
      .card{{background:#fff;max-width:600px;margin:20px auto;padding:30px;
             border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,.1)}}
      h1{{color:#2c3e50;text-align:center}}
      input,textarea{{width:100%;padding:10px;margin:5px 0 15px;
                     border:1px solid #ddd;border-radius:6px;box-sizing:border-box}}
      button{{background:#2c3e50;color:#fff;padding:10px 20px;border:none;
             border-radius:6px;cursor:pointer}}
      ul{{list-style:none;padding:0}}
      li{{background:#f8f9fa;padding:12px;margin:8px 0;border-radius:6px;
         border-left:4px solid #2c3e50}}
    </style></head>
    <body><div class="card">
      <h1>📖 Buku Tamu Digital</h1>
      <p style="text-align:center;color:#888">UTS Teknologi Platform — Jenli Melinda Banik (26110023)</p>
      <form method="POST" action="/tambah">
        <input type="text" name="nama" placeholder="Nama Anda" required maxlength="100">
        <textarea name="pesan" placeholder="Pesan Anda" required rows="3"></textarea>
        <button type="submit">Kirim</button>
      </form>
      <h3>Tamu yang sudah mengisi:</h3>
      <ul>{daftar}</ul>
    </div></body></html>
    """


@app.route('/tambah', methods=['POST'])
def tambah():
    nama = request.form.get('nama', '').strip()
    pesan = request.form.get('pesan', '').strip()
    if nama and pesan:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tamu (nama, pesan) VALUES (%s, %s)",
                        (nama, pesan))
        conn.commit()
        conn.close()
        print(f"[INSERT] {nama}: {pesan}", flush=True)
    return redirect('/')


if __name__ == '__main__':
    if wait_for_db():
        init_table()
    app.run(host='0.0.0.0', port=5000)
