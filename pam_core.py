import argon2
import os
import sqlite3
import Crypto.Cipher.AES as AES

def pam_verify(pwd : str) -> tuple[bool, str]:
    db = sqlite3.connect("./.pam/pam.db")
    cs = db.cursor()
    vals = cs.execute("SELECT hash, salt from keys WHERE is_master = 1").fetchall()
    try:
        ph = argon2.PasswordHasher
        ph.verify(vals[0][0], pwd)
        return (True, ph.hash( password=pwd,salt=vals[0][1] ))
    except:
        print("Incorrect master password.")
        return (False, "")

def _check_cwd() -> tuple[bool, bool]:
    return (os.path.exists("./.pam"), os.path.exists("./.pam/pam.db"))

def pam_init(pwd : str) -> None:
    check = _check_cwd()
    if not check[0]:
        os.mkdir("./.pam")
    if check[1]:
        while True:
            answer = input("Warning, there is already an instance of pam set up here. Do you wish to " \
            "overwrite the instance, deleting all of the stored passwords? [y/n] ")
            if answer.lower() == "y" or answer.lower() == "yes":
                os.remove("./.pam/pam.db")
                break
            elif answer.lower() == "n" or answer.lower() == "no":
                return
    db = sqlite3.connect("./.pam/pam.db")
    curs = db.cursor()
    salt = os.urandom(32)
    master_hash = argon2.PasswordHasher().hash(password=pwd, salt=salt)
    curs.execute("CREATE TABLE keys (service TEXT, username TEXT, hash TEXT, salt TEXT, is_master INTEGER)")
    curs.execute("INSERT INTO keys VALUES (?, ?, ?, ?, ?)", ("pam", "MASTER", master_hash, os.urandom(32).hex(), 1))
    curs.execute("CREATE TABLE passwords (service TEXT, username TEXT, ciphertext TEXT)")
    db.commit()
    db.close()

def pam_add(service : str, username : str, pwd : str) -> None:
    if not all(check for check in _check_cwd()):
        print("Please initialize pam in this directory first by running \"py pam init\"")
        return
    db = sqlite3.connect("./.pam/pam.db")
    cs = db.cursor()
    salt = os.urandom(32)
    hash = argon2.PasswordHasher()
    cs.execute("INSERT")

    AES.new(mode=AES.MODE_GCM)


