# No Docker Setup — Tamil + English

## 1. PostgreSQL Windows
Download PostgreSQL Windows installer from https://www.postgresql.org/download/windows/ and install PostgreSQL with pgAdmin. Remember the `postgres` password and port 5432. In pgAdmin, create a database `customer_chatbot` (right-click Databases > Create > Database). For beginner local testing, use the postgres account and set `.env` DATABASE_URL to `postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/customer_chatbot`. URL-encode special password characters if necessary. Prefer a dedicated restricted database user for deployment.

**தமிழ்:** PostgreSQL-ஐ Windows-ல் install செய்து pgAdmin மூலம் `customer_chatbot` database create பண்ணுங்கள். Docker தேவையில்லை.

## 2. Qdrant Cloud
Visit https://cloud.qdrant.io/ and create a cluster using the currently available free-tier option (if offered). Copy the HTTPS cluster URL and API key into `.env` as `QDRANT_URL` and `QDRANT_API_KEY`. Keep them secret.

**தமிழ்:** Qdrant Cloud-ல் cluster உருவாக்கி URL மற்றும் API key-ஐ `.env`-ல் paste செய்யுங்கள். API key-ஐ screenshots-ல் காட்ட வேண்டாம்.

## 3. Python + Ollama
In PowerShell inside the project folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull mistral
ollama pull nomic-embed-text
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(48)); print(secrets.token_urlsafe(48))"
```

Replace `.env` database password, Qdrant URL/key, and both random secrets. Keep `ENVIRONMENT=development` only for local testing. Never publish `.env`.

## 4. Run
```powershell
alembic upgrade head
python seed.py
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs

## 5. Verify
Use Swagger to request and verify OTP, login as Arun (9876543210), create a conversation, send messages, and test invoices. The development OTP goes to `.dev_otp_inbox`, not API responses. Check README for detailed steps.

**தமிழ்:** மேலுள்ள commands run செய்து Swagger UI-ல் OTP login, chat memory, invoice search, invoice confirmation test செய்யுங்கள்.

## Note
This is an adapted **starter**, not a fully verified production or assignment submission. A real PostgreSQL server, Qdrant Cloud connection, and working Ollama models are required for live testing. Real SMS delivery is not implemented; the development-only OTP adapter is used.
