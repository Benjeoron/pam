import argon2
import os
import sqlite3
import Crypto.Cipher.AES as AES
import secrets
import base64

def pam_verify(pwd : str) -> tuple[bool, str]:
    db = sqlite3.connect("./.pam/pam.db")
    cs = db.cursor()
    vals : list[tuple[str, str]]= cs.execute("SELECT hash, salt from keys WHERE is_master = 1").fetchall()
    try:
        ph = argon2.PasswordHasher()
        ph.verify(hash=vals[0][0], password=pwd)
        return (True, ph.hash(password=pwd, salt=vals[0][1].encode()))
    except:
        return (False, "")

def check_cwd() -> tuple[bool, bool]:
    return (os.path.exists("./.pam"), os.path.exists("./.pam/pam.db"))

def pam_init(pwd : str, check : tuple[bool, bool]) -> None:
    if check[1]:
        os.remove("./.pam/pam.db")
    db = sqlite3.connect("./.pam/pam.db")
    curs = db.cursor()
    salt = secrets.token_bytes(32)
    master_hash = argon2.PasswordHasher().hash(password=pwd, salt=salt)

    curs.execute("CREATE TABLE keys (service TEXT, username TEXT, hash TEXT, salt TEXT, is_master INTEGER)")
    curs.execute("INSERT INTO keys VALUES (?, ?, ?, ?, ?)", ("pam", "MASTER", master_hash, secrets.token_bytes(32).hex(), 1))
    curs.execute("CREATE TABLE passwords (service TEXT, username TEXT, ciphertext TEXT)")
    db.commit()
    db.close()

def pam_add(service : str, username : str, pwd : str, key : str) -> None:
    if not all(check for check in check_cwd()):
        print("Please initialize pam in this directory first by running \"py pam init\"")
        return

    db = sqlite3.connect("./.pam/pam.db")
    cs = db.cursor()
    salt = secrets.token_bytes(32)
    full_dek = argon2.PasswordHasher(hash_len=16).hash(password=key, salt=salt)
    # cs.execute("INSERT INTO keys VALUES (?, ?, ?, ?, ?)", (service, username, dek, salt, 0))
    dek = base64.b64decode(full_dek.split("$")[5]+"==").hex()
    nonce = secrets.token_bytes(16)
    aes = AES.new(key=dek.encode(), mode=AES.MODE_GCM, nonce=nonce)
    enc = aes.encrypt(plaintext=pwd.encode())
    print(enc)
    # cs.execute("INSERT INTO passwords VALUES (?, ?, ?)", (service, username, enc))
    # db.commit()


