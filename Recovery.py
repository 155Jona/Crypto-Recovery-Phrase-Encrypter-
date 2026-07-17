from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64
import os
import json
import getpass


SALT_DATEI = "salt.bin"
DATEN_DATEI = "wallets.enc"



def get_or_create_salt() -> bytes:
    if os.path.exists(SALT_DATEI):
        with open(SALT_DATEI, "rb") as f:
            return f.read()
    else:
        neue_salt = os.urandom(16)
        with open(SALT_DATEI, "wb") as f:
            f.write(neue_salt)
        return neue_salt



def passwort_zu_schluessel(passwort: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(passwort.encode()))



def speichere_daten(fernet: Fernet, keys_name: list, keys: list):
    daten = {"keys_name": keys_name, "keys": keys}
    daten_json = json.dumps(daten)
    verschluesselt = fernet.encrypt(daten_json.encode())
    with open(DATEN_DATEI, "wb") as f:
        f.write(verschluesselt)



def lade_daten(fernet: Fernet) -> dict:
    if not os.path.exists(DATEN_DATEI):
        return {"keys_name": [], "keys": []}
    with open(DATEN_DATEI, "rb") as f:
        verschluesselt = f.read()
    try:
        daten_json = fernet.decrypt(verschluesselt)
    except Exception:
        print("Wrong password or corrupted data. Exiting...")
        exit(1)
    return json.loads(daten_json.decode())


def main():
    salt = get_or_create_salt()
    passwort = input("Master-Passwort: ")
    schluessel = passwort_zu_schluessel(passwort, salt)
    fernet = Fernet(schluessel)

    daten = lade_daten(fernet)
    keys_name = daten["keys_name"]
    keys = daten["keys"]

    while True:
        print("\n1. View All Keys")
        print("2. Add Key")
        print("3. Remove Key")
        print("4. Exit")

        option = input("Select an option: ")

        if option == "1":
            os.system('cls')
            for i, name in enumerate(keys_name):
                print(f"{i + 1}. {name}")
            option_keys = input("Select a key to view: ")
            index = int(option_keys) - 1
            if 0 <= index < len(keys):
                print(f"Key: {keys[index]}")

        elif option == "2":
            key_name = input("Enter key name: ")
            key_value = input("Enter key value: ")
            keys_name.append(key_name)
            keys.append(key_value)
            speichere_daten(fernet, keys_name, keys)
            print("Gespeichert!")

        elif option == "3":
            for i, name in enumerate(keys_name):
                print(f"{i + 1}. {name}")
            option_keys = input("Select a key to remove: ")
            index = int(option_keys) - 1
            if 0 <= index < len(keys_name):
                removed = keys_name.pop(index)
                keys.pop(index)
                speichere_daten(fernet, keys_name, keys)
                print(f"'{removed}' wurde entfernt.")

        elif option == "4":
            print("Exiting...")
            return

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")