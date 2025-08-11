import argon2
import os
import sqlite3
import Crypto

def check_cwd() -> bool:
    return (os.path.exists("./.pam"), os.path.exists("./.pam/pam.db"))

def pam_init(pwd : str):
    check = check_cwd()
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
    curs.execute("CREATE TABLE keys (service TEXT, username TEXT, hash TEXT, salt1 TEXT, salt2 TEXT, is_master INTEGER)")
    curs.execute("INSERT INTO keys VALUES (?, ?, ?, ?, ? ,?)", ("pam", "MASTER", master_hash, salt.hex(), os.urandom(32).hex(), 1))
    db.commit()
    db.close()


