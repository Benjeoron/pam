import argon2
import sqlite3

db = sqlite3.connect("./.pam/pam.db")
ph = argon2.PasswordHasher()
cs = db.cursor()

master_hash = cs.execute("SELECT hash from keys WHERE is_master = 1").fetchall()
db.commit()

print(ph.verify(vals[0][0], "bungus"))
