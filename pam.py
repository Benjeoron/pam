import sys
import os
import getpass
import Crypto
import sqlite3

def check_cwd():
    return (os.path.exists("./.pam"), os.path.exists("./.pam/pam.db"))



def print_help():
    print("Usage: pam <option> <input>\noptions:\n",
          "init -- initializes a new instance of pam in the current working directory\n"
          "add <usage> <username> -- adds a new password")

if __name__ == "__main__":
    print (sys.argv)
    match sys.argv[1]:
        case "init":
            os.mkdir("./.pam")
            sqlite3.connect("./.pam/pam.db")
        case "add":
            db = sqlite3.connect("./.pam/pam.db")
            service = sys.argv[2] if len(sys.argv) > 2 else input("Enter the use for this password: ")
            username = sys.argv[3] if len(sys.argv) > 3 else input("Enter your username: ")
            pwd = getpass.getpass("Enter your password: ")
        case _:
            print(f"Command not found: {sys.argv[1]}")
            print_help()




