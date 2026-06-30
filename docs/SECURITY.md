# Security

- Never commit `.env`.
- Never commit Telegram tokens, passwords, SSH keys, or broker credentials.
- Keep `.env` only on the server or local development machine.
- Telegram scripts skip gracefully if credentials are missing.
- SSH key login is used for deployment; protect the private key on the Windows machine.
- UFW allows SSH, HTTP, and Streamlit only.
- Do not add account numbers to CSV data files.
