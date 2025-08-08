import sys
import os
import getpass
import Crypto

def check_cwd():
    return (os.path.exists("./.pam"), os.path.exists("./.pam/pam.db"))
    


def print_help():
    print("Usage: pam <option> <input>\noptions:\n",
          "init -- initializes a new instance of pam in the current working directory\n"
          "add <account> <username> -- adds a new password")

if __name__ == "__main__":
    match sys.argv[1]:
        case "init":
            os.mkdir("./.pam")
        case "add":
            getpass()
        case _:
            print(f"Command not found: {sys.argv[1]}")
            print_help()

        


