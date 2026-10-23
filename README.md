# Secure Customer AI Chatbot — Beginner guide (Tamil + English)

This is an **independent reference implementation**, not a tested final submission. The assignment's original `step1_memory.py`, `step2_login.py`, `step3_rag.py`, `step4_functions.py` and `customer_data.py` were not uploaded. Run and verify every required check locally. Screenshots must be from your own running application.

## 1. Install software

Install Python 3.11 or 3.12, VS Code, PostgreSQL for Windows, and Ollama. Create a Qdrant Cloud cluster. Docker is NOT required. In Windows PowerShell, from this folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.

## 2. Set up PostgreSQL locally, Qdrant Cloud and models

```powershell
ollama pull mistral
ollama pull nomic-embed-text
ollama list
```

Mistral tool-call compatibility varies by Ollama model version. If tool calling fails, configure a tool-capable model in `CHAT_MODEL` and verify its output. The embedding model should remain consistent after indexing.

Set `DATABASE_URL` in `.env` to your local PostgreSQL connection string. Create a database named `customer_chatbot` using pgAdmin or psql. Set `QDRANT_URL` and `QDRANT_API_KEY` from your Qdrant Cloud cluster. Do not commit these credentials.

## 3. Configure secrets

```powershell
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(48)); print(secrets.token_urlsafe(48))"
```

Replace both `REPLACE_...` values in `.env` with the two distinct generated secrets. **Never commit `.env` or `.dev_otp_inbox`.** The development OTP adapter writes the one-time code to `.dev_otp_inbox` only, never to the API response. It must be disabled outside development. This is not real SMS delivery.

## 4. Migrate, seed and start API

```powershell
alembic upgrade head
python seed.py
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs . No frontend is needed; Swagger is enough to demonstrate the backend.

## 5. OTP login (தமிழ்)

1. `/auth/request-otp` → `Try it out` → `{"mobile":"9876543210"}` → Execute.
2. VS Code terminal-ல் `Get-Content .dev_otp_inbox -Tail 1` run செய்து **development-only** OTP பாருங்கள். OTP-ஐ screenshot-ல் hide செய்யுங்கள்.
3. `/auth/verify-otp` → `{"mobile":"9876543210","otp":"<the six digit code>"}` → Execute.
4. Response-ல் access token வரும். Swagger `Authorize` மூலம் bearer token set செய்யுங்கள்; token screenshot-ல் மறைக்கவும்.
5. `/me` endpoint customer name Arun காட்ட வேண்டும்.

**English:** Only verified OTP produces an expiring JWT; mobile-number entry alone never logs in. OTP expires after five minutes, has five attempts, and cannot be reused. Request cooldown is 60 seconds.

## 6. Create a conversation and chat

- `POST /conversations` with authorized token; note returned `id`, e.g. 1.
- `POST /conversations/1/chat` with `{"text":"My name is Arun"}`.
- Again with `{"text":"What is my name?"}`.
- Restart Uvicorn; `GET /conversations/1/messages` and chat again to demonstrate persistent history.
- History passed to the LLM is limited to **12 stored messages**; all messages remain in PostgreSQL.

## 7. RAG and invoices

- `POST /admin/reindex` while authenticated as Arun to index Arun's five seeded invoices. Repeat for Deepa after logging in as Deepa.
- `GET /search?q=unpaid invoices` returns only invoice IDs belonging to the authenticated customer.
- Chat `What unpaid invoices do I have?` and compare cited invoice IDs with `GET /invoices`.
- Chat `Create invoice INV-300 dated 2026-10-22 for INR 1250, unpaid`. The model must call `add_invoice` to create a pending proposal; inspect `pending_invoices` in the response.
- Confirm **only after reviewing details** using `POST /invoices/confirm/{pending_id}`. The invoice is saved to PostgreSQL before vector indexing. The response `searchable=false` indicates indexing failed; `POST /admin/reindex` retries.
- Repeating a confirmed invoice number returns a duplicate error; a PostgreSQL unique constraint enforces this too.

## 8. Mandatory screenshot checklist

1. OTP requested, valid login, expired/reused/incorrect OTP, cooldown, five-attempt lockout.
2. Unauthorized `/me` returns 401.
3. Arun memory persists after backend restart.
4. Deepa cannot access Arun's conversation or invoice data.
5. Unpaid invoice response and matching invoice IDs from PostgreSQL.
6. `hello` response with `tool_requests: 0`.
7. Invoice proposal, explicit confirmation, new invoice in `GET /invoices`.
8. `GET /search?q=INV-300` contains new invoice ID.
9. Repeated INV-300 creation prevented.
10. Simulate Qdrant failure during confirmation, show `saved=true, searchable=false`; restore Qdrant and run `/admin/reindex`.

Use `docker compose stop qdrant` to simulate indexing failure, then `docker compose start qdrant` and `/admin/reindex` to recover. Do not stop PostgreSQL for this test.

## 9. Architecture

`FastAPI` → verifies JWT → `PostgreSQL` stores customer ownership, invoices and chat → `Ollama` handles LLM + real embeddings → `Qdrant` persists filtered vectors. The `search_records` tool never accepts a customer ID from the model. Vector IDs are deterministic to prevent duplicate indexing.

## Important limitations and improvements

- This is a **starter implementation** that needs live end-to-end testing, not a claim of passing the assignment.
- The LLM may not request tools reliably depending on installed model. Confirm real tool calling and embeddings before submission.
- For production use, add real SMS provider integration, HTTPS, rate limiting by IP/mobile, transaction-safe OTP concurrency, service monitoring, and more complete integration tests.
- `POST /admin/reindex` is named for convenience but is scoped to the authenticated customer's own invoices; it is not a global administrative API.
- The deadline in the assignment is **23 October 2026 at 1:00 PM IST**. Screenshots, not a ZIP or report, are the stated submission format.
