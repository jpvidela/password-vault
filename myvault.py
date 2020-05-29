# Importar librerías
import sqlite3
from Crypto.Hash import SHA256
import my_secrets
import encrypter
import time

# MAIN MENU


def GetAction():
    while True:
        # Print menu
        print('\n\nWhat would you like to do next? \n')
        print(10 * '~')
        print('')
        print('s : Store new password')
        print('r : Retrieve stored password')
        print('d : Delete existing password')
        print('l : List stored services/sites')
        print('q : Quit program')
        print('')
        print(10 * '~')
        action = input('\nYour command: ')[0]
        if action == 'q':
            break
        if action == 's':
            # Get inputs
            service = input("Service/Site name: ")
            user = input("User: ")
            password = input("Password: ")
            if store(service, user, password, AES_key) == 0:
                print("Password succesfully stored!")
                input("Press Enter to continue")
        if action == 'r':
            service = input("Retrieve password for Service/Site name: ")
            user = input("User: ")
            ans = retrieve(service, user, AES_key)
            if ans != 1:
                print(f'Service: {service}')
                print(f'User: {user}')
                print(f'Password: {ans}')
            input("Press Enter to continue")
        if action == 'd':
            pass
        if action == 'l':
            pass
    return 0


# *** DATABASE AND ENCRIPTION FUNCTIONS ***

# Hash a word with SHA256 algorithm
def hash_word(word):
    h = SHA256.new()
    h.update(word.encode('utf-8'))
    return h.hexdigest()


# Store password in database
def store(svc, usr, pw, AES_key):
    try:
        # Generate AES encrypted password
        key = encrypter.encrypt(pw, AES_key)
        # Store in database
        db.execute(f"INSERT INTO cles (site, user, key) VALUES(?, ?, ?)", (svc, usr, key))
        # Save changes into database
        db.commit()
        print(f"Password stored for service '{svc}' and user '{usr}'")
        return 0
    except:
        return 1


# Retrieve and decrypt password from database
def retrieve(svc, usr, AES_key):
    # Retrieve encrypted password from database
    data = check_record(svc, usr)
    if data == 1:
        print("Try Again!")
        return 1
    else:
        key = data[0][2]
    # Decrypt pasword with AES algorithm
    pw_decrypt = encrypter.decrypt(key, AES_key)
    return pw_decrypt


# Check if record exists in database
def check_record(svc, usr):
    # Search for register.
    cursor = db.execute('SELECT * FROM cles WHERE site = ? and user = ?', (svc, usr))
    data = cursor.fetchall()
    if len(data) == 0:
        print("Couldn't found any matching record")
        return 1
    else:
        return data


# *** END OF FUNCTIONS ***

# Login
input_pw = ''
print("Type admin password. Type 'qq' to quit")
while input_pw != my_secrets.password:
    input_pw = input('Admin passwowrd: ')
    if input_pw == 'qq':
        exit()


# Generate key from SHA256 hash algorithm and store last 16 characters
AES_key = hash_word(my_secrets.password)[-16:]

# Crear base de datos
db = sqlite3.connect('vault.db')

# Crear tabla cles dentro de vault
command = "CREATE TABLE cles (user TEXT, site TEXT, key TEXT)"
try:
    db.execute(command)
    print("\nVault created!")
    GetAction()
except sqlite3.Error:
    print('Welcome back!')
    print('\nYou already have a vault!')
    time.sleep(2)
    GetAction()
