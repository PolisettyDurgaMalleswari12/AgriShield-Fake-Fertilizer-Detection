import sqlite3, os
DB="database/agrishield.db"
def conn():
    os.makedirs("database",exist_ok=True)
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
    c=conn()
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT UNIQUE,password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS verifications(id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT,product_name TEXT,brand TEXT,batch_number TEXT,mrp REAL,risk REAL,result TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    c.execute("CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT,product_name TEXT,brand TEXT,batch_number TEXT,seller TEXT,reason TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    c.commit(); c.close()
def add_user(name,email,password):
    try:
        c=conn(); c.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",(name,email,password)); c.commit(); c.close(); return True
    except sqlite3.IntegrityError: return False
def find_user(email,password):
    c=conn(); x=c.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password)).fetchone(); c.close(); return x
def save_verification(email,product,brand,batch,mrp,risk,result):
    c=conn(); c.execute("INSERT INTO verifications(email,product_name,brand,batch_number,mrp,risk,result) VALUES(?,?,?,?,?,?,?)",(email,product,brand,batch,mrp,risk,result)); c.commit(); c.close()
def save_report(email,product,brand,batch,seller,reason):
    c=conn(); c.execute("INSERT INTO reports(email,product_name,brand,batch_number,seller,reason) VALUES(?,?,?,?,?,?)",(email,product,brand,batch,seller,reason)); c.commit(); c.close()
def get_user_verifications(email):
    c=conn(); x=c.execute("SELECT * FROM verifications WHERE email=? ORDER BY id DESC",(email,)).fetchall(); c.close(); return x
def get_verifications():
    c=conn(); x=c.execute("SELECT * FROM verifications ORDER BY id DESC").fetchall(); c.close(); return x
def get_reports():
    c=conn(); x=c.execute("SELECT * FROM reports ORDER BY id DESC").fetchall(); c.close(); return x
