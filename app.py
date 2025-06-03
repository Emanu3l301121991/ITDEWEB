
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "database.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inventar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unternehmen TEXT,
            stadt TEXT,
            instrument TEXT,
            seriennummer TEXT,
            empfangsdatum TEXT,
            status TEXT
        )
    ''')
    con.commit()
    con.close()

@app.route('/api/list', methods=['GET'])
def get_list():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM inventar')
    data = [dict(row) for row in cur.fetchall()]
    con.close()
    return jsonify(data)

@app.route('/api/add', methods=['POST'])
def add_entry():
    data = request.get_json()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute('''
        INSERT INTO inventar (unternehmen, stadt, instrument, seriennummer, empfangsdatum, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data.get('unternehmen'),
        data.get('stadt'),
        data.get('instrument'),
        data.get('seriennummer'),
        data.get('empfangsdatum'),
        data.get('status') or ""
    ))
    con.commit()
    con.close()
    return jsonify({"success": True})

@app.route('/api/delete/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute('DELETE FROM inventar WHERE id = ?', (entry_id,))
    con.commit()
    con.close()
    return jsonify({"success": True})

@app.route('/api/status/<int:entry_id>', methods=['PUT'])
def update_status(entry_id):
    data = request.get_json()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute('UPDATE inventar SET status = ? WHERE id = ?', (data.get('status'), entry_id))
    con.commit()
    con.close()
    return jsonify({"success": True})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
