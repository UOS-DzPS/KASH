from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import time
import pymysql

def connect_to_db():
    for i in range(10):
        try:
            print(f"[DB] connection attempt {i}/10")
            return pymysql.connect(
                    host=os.getenv("MYSQL_HOST"),
                    user=os.getenv("MYSQL_USER"),
                    password=os.getenv("MYSQL_PASSWORD"),
                    database=os.getenv("MYSQL_DATABASE")
                    )
        except pymysql.err.OperationalError:
            print("[DB] Not ready, retrying...")
            time.sleep(2)
    raise RuntimeError("[DB] Cannot connect to DB after 10 attempts")

load_dotenv()
app = Flask(__name__)
db = connect_to_db()
cursor = db.cursor()


@app.route("/")
def index():
    cursor.execute("""
        SELECT user_id, username
        FROM users
        ORDER BY created_at;
        """)
    msg = cursor.fetchall()

    return jsonify(msg)

@app.route("/<string:username>")
def test(username):
    cursor.execute(f"""INSERT INTO users (username)
            VALUES ("{username}");""")
    db.commit()

    return {"success": True}, 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
