# 🔐 Wallet Manager

A simple command-line tool for securely managing wallet keys (or any other sensitive strings such as API keys, passwords, etc.). All data is stored locally and encrypted, protected by a master password.

## ✨ Features

- **Strong encryption**: Uses `Fernet` (AES-128 in CBC mode with HMAC) from the `cryptography` library
- **Secure key derivation**: The master password is converted into an encryption key via `PBKDF2HMAC` with 600,000 iterations (SHA-256)
- **Random salt**: Generated once and stored locally (`salt.bin`)
- **Simple CLI**: View, add, and remove keys
- **No cloud, no server**: All data stays entirely on your local machine

## 📦 Requirements

- Python 3.8+
- The [`cryptography`](https://pypi.org/project/cryptography/) package

Install the dependency:

```bash
pip install cryptography
```

## 🚀 Usage

Run the script:

```bash
python wallet_manager.py
```

On first run, you'll be asked to set a master password. **Remember it well** — without this password, your stored keys cannot be recovered!

Available options:

```
1. View All Keys     – Shows all stored keys with their names
2. Add Key            – Adds a new key with a name
3. Remove Key          – Removes a stored key
4. Exit                – Exits the program
```

## 🗂 Generated Files

| File           | Description                                              |
|----------------|-------------------------------------------------------------|
| `salt.bin`     | Random salt used for key derivation (created once)          |
| `wallets.enc`  | Encrypted file containing all stored keys                   |

⚠️ **Important**: Both files should be kept safe and **never** uploaded to a public repository (e.g. via `.gitignore`).

Recommended `.gitignore`:

```
salt.bin
wallets.enc
```

## 🔒 Security Notes

- If the master password is wrong, decryption will fail and the program exits automatically.
- Security depends heavily on the **strength of your master password**. Use a long, random password.
- This tool is primarily intended for educational/personal use. For production or commercial use, a professionally audited solution (e.g. an established password manager) is recommended.

## 📁 Project Structure

```
.
├── wallet_manager.py   # Main script
├── salt.bin             # (auto-generated)
├── wallets.enc           # (auto-generated)
└── README.md
```

## 🛠 Planned Improvements (Ideas)

- [ ] Export/import encrypted backups
- [ ] Password strength check during setup
- [ ] Support for multiple profiles
- [ ] Copy-to-clipboard instead of plaintext display



## ⚠️ Disclaimer

This tool is provided "as is", without any warranty. Use it at your own risk, especially when handling wallet keys or other critical credentials.
