from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
import base64
from src.save import SaveFile
import sys
import secrets
import string

def main():
    global name 
    name = input("Whats your name: ")
    filename = SaveFile(name)
    if filename.load():
        master_password = input("Enter your master password: ")
        if not validate_password(filename, master_password):
            sys.exit("Invalid password")
        while True:
            choice = input(f"What do you want to do? \n1. Add an account\n2. Look at your accounts\n3. Remove an account\n")
            match choice:
                case "1":
                    website = input("What website: ").title()
                    username = input("What username: ")
                    password = input("What pass: ")
                    add_account(filename, master_password, website, username, password)
                case "2":
                    website = input("What website do you want your account from: ").title()
                    print(look_accounts(filename, master_password, website))
                case "3":
                    website = input("What website do you want to remove your account from: ").title()
                    remove_account(filename, website, master_password)
                case _:
                    break
    else:
        filename.new_user("C:\\Users\Andrei\\Desktop\\VScode")
        master_password = input("Enter a master password")
        match_password(filename, master_password)

        return
    
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  
        salt=salt,
        length=32 
    )

    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def add_account(file_handler, master_password, website, username, password):
    salt = byte_salt(file_handler)
    key = generate_key(master_password, salt)
    encryption = Fernet(key)

    username = bytes(username, 'utf-8')
    password = bytes(password, 'utf-8')

    encrypted_name, encrypted_password = encryption.encrypt(username), encryption.encrypt(password)

    str_username, str_password = base64.b64encode(encrypted_name).decode('utf-8'), base64.b64encode(encrypted_password).decode('utf-8')

    file_handler.save(website, {"Username": str_username, "Password": str_password})
    return f"Added!"

def look_accounts(filehandler, password, website):
    accounts = decrypt(filehandler, password)
    if not accounts:
        return "No account's found"
    account_list = ''
    previous = None
    for account in accounts:
        if website == "All" and account['Website'] != previous:
            account_list += f"Website: {account['Website']}\nUsername: {account['Username']}\nPassword: {account['Password']}\n\n"
            previous = account['Website']
        elif website == account['Website'] or website == "All" and account['Website'] == previous:
            account_list += f"Username: {account['Username']}\nPassword: {account['Password']}\n\n"
    return account_list

def decrypt(file_handler, password):
    salt = byte_salt(file_handler)
    key = generate_key(password, salt) 
    encryption = Fernet(key)  

    accounts = []
    check = []

    json = file_handler.load()
    for website in json[file_handler._username]:
        if website == "User_info":
            continue
        for account in json[file_handler._username][website]:
            binuser = base64.b64decode(account["Username"]).decode('utf-8')
            binpass = base64.b64decode(account["Password"]).decode('utf-8')
            decrypteduser = encryption.decrypt(binuser).decode('utf-8')
            decryptedpass = encryption.decrypt(binpass).decode('utf-8')
            accounts.append({'Website': website, 'Username': decrypteduser, 'Password': decryptedpass})
    if check == accounts:
        return False
    return accounts
def remove_account(filehandler, website, password):
    accounts = decrypt(filehandler, password)
    website_accounts = [account for account in accounts if account["Website"] == website]
    if not website_accounts:
        print("No accounts")
        return

    for i, account in enumerate(website_accounts):
        print(f"{i + 1}. Username: {account['Username']} \n   Password: {account['Password']}\n")

    try:
        remove = (int(input("What account do you want to remove?: "))) - 1
        confirm = input(f"Are you sure you want to delete account {website_accounts[remove]['Username']} from {website}? (Y/N)")
        match confirm:
            case "Y":
                filehandler.remove(website, remove)
            case "N":
                return
    except IndexError:
        print("That account doesnt exist!")
        return


def byte_salt(filename):
    data = filename.load()
    username = filename._username
    salt = data[username]['User_info'][0]['Salt']
    byte_salt = bytes(salt, 'utf-8')

    return byte_salt

def validate_password(filehandler, password):
    try:
        print(password)
        salt = byte_salt(filehandler)
        print(salt)
        key = generate_key(password, salt)
        print(key)
        encryption = Fernet(key)

        json = filehandler.load()
        word = json.get(filehandler._username, {}).get("User_info", [{}])[1].get("Random_word", "")
        byte_word = bytes(base64.b64decode(word).decode('utf-8'), 'utf-8')
        check = encryption.decrypt(byte_word)
    except InvalidToken:
        return False

    return True

def match_password(filehandler, password):
    print(password)
    random_word = bytes(generate_password(10), 'utf-8')
    salt = byte_salt(filehandler)
    print(salt)
    key = generate_key(password, salt)
    encryption = Fernet(key)
    word = encryption.encrypt(random_word)
    str_word = base64.b64encode(word).decode('utf-8')
    print("matchpass")
    print(key)
    filehandler.save("User_info", {"Random_word": str_word})

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_word = ''.join(secrets.choice(characters) for _ in range(length))
    return random_word

if __name__ == "__main__":
    main()

    