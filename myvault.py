# Importar librerías
import sqlite3
from Crypto.Hash import SHA256
import my_secrets
import encrypter


def GetAction():
    while True:
        # Print menu
        print('\nWhat do you want to do? \n')
        print(10 * '#')
        print('')
        print('s : Store new password')
        print('r : Retrieve stored password')
        print('d : Delete existing password')
        print('l : List stored services/sites')
        print('q : Quit program')
        print('')
        print(10 * '#')
        action = input('\nYour command: ')[0]
        if action == 'q':
            break
        if action == 's':
            service = input("Service/Site name: ")
            user = input("User: ")
            password = input("Password: ")
            print(store(service, user, password, AES_key))
        if action == 'r':
            service = input("Retrieve password for Service/Site name: ")
            user = input("User: ")
            retrieve(service, user, AES_key)
        if action == 'd':
            pass
        if action == 'l':
            pass
    return 0


# Hash a word with SHA256 algorithm
def hash_word(word):
    h = SHA256.new()
    h.update(word.encode('utf-8'))
    return h.hexdigest()


def store(svc, usr, pw, AES_key):
    # Generate AES encrypted password
    key = encrypter.encrypt(pw, AES_key)
    # Store in database
    db.execute(f"INSERT INTO cles (site, user, key) VALUES(?, ?, ?)", (svc, usr, key))
    # Save changes into database
    db.commit()
    print(f"Password stored for service '{svc}' and user '{usr}'")
    return 0


def retrieve(svc, usr, AES_key):
    # Retrieve encrypted password from database
    cursor = db.execute('SELECT key FROM cles WHERE site = ? and user = ?', (svc, usr))
    key = cursor.fetchall()[0][0]
    print(f'Stored key value in database: {key}')
    # Decrypt pasword with AES algorithm
    pw_decrypt = encrypter.decrypt(key, AES_key)
    print(f'Service: {svc}')
    print(f'User: {usr}')
    print(f'Password: {pw_decrypt}')
    return 0


# Login
input_pw = ''
print("Type admin password. Type 'qq' to quit")
while input_pw != my_secrets.password:
    input_pw = input('Admin passwowrd: ')
    if input_pw == 'qq':
        exit()


# Generate key from SHA256 hash algorithm and store last 16 characters
AES_key = hash_word(my_secrets.password)[-16:]
# FOR DEBUGGING

key_file = open("AES_key.txt", "w")
key_file.write(AES_key)
key_file.close()

# END FOR DEBUGGING
# Crear base de datos
db = sqlite3.connect('vault.db')
# Crear tabla cles dentro de vault
command = "CREATE TABLE cles (user TEXT, site TEXT, key TEXT)"
try:
    db.execute(command)
    print("\nVault created!")
    GetAction()
except:
    print('\nYou already have a vault!')
    GetAction()
