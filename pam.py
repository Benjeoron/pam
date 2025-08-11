import sys
import getpass
import pam_core


def print_help():
    print("Usage: pam <option> <input>\noptions:\n",
          "init -- initializes a new instance of pam in the current working directory\n"
          "add <usage> <username> -- adds a new password")

if __name__ == "__main__":
    print (sys.argv)
    match sys.argv[1]:
        case "init":
            matched = False
            attempts = 0
            while not matched and attempts < 3:
                master_pwd = getpass.getpass("Enter a master password: ")
                if getpass.getpass("Re-enter the password to confirm: ") == master_pwd:
                    matched = True
                else:
                    print("Incorrect password.")
                    attempts += 1
            if not matched:
                print("Initialization failed, please try again.")
            else:
                pam_core.pam_init(master_pwd)
        case "add":
            db = pam_core.pam_start()
            service = sys.argv[2] if len(sys.argv) > 2 else input("Enter the use for this password: ")
            username = sys.argv[3] if len(sys.argv) > 3 else input("Enter your username: ")
            pwd = getpass.getpass("Enter your password: ")
        case _:
            print(f"Command not found: {sys.argv[1]}")
            print_help()




