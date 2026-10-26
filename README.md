# MailCheck

A small Flask web app that estimates email deliverability by validating address syntax and looking up DNS mail-routing records. It never sends messages and does not store the submitted list.

## What the statuses mean

- **Likely delivered**: the address has a plausible format and the domain publishes an MX record. This is a *domain-level signal only*; it does not confirm the recipient mailbox exists or that a message will reach the inbox.
- **Likely bounce**: the address format is invalid, the domain does not exist, or no usable mail-routing/address records could be found.
- **Unknown**: DNS timed out, DNS responses were inconclusive, or fallback routing may apply.

## Limitations of the deployed version

MailCheck intentionally does **not** connect to recipient mail servers using SMTP, issue `VRFY`/`RCPT TO` probes, or send test messages. Many mail servers suppress mailbox-verification responses, use catch-all inboxes, rate-limit probes, or deliberately return misleading results. SMTP probing is also commonly blocked by hosting providers. Since this version uses DNS lookups only, it does not require outbound SMTP access (ports 25/465/587) and can still check basic domain mail-routing configuration on hosts that block SMTP. It cannot verify a specific mailbox, determine whether the mailbox is full, or guarantee delivery. DNS egress must be available; if the host blocks DNS lookups or the resolver times out, results will be `unknown`.

Use this only for legitimate list hygiene. Do not send messages to addresses you do not own or have permission to contact.

## Run locally

Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Deploy on Render (free web service where available)

1. Create a GitHub repository and upload this folder's files.
2. Sign in to Render and choose **New + → Web Service**.
3. Connect the repository. Render can detect `render.yaml`; alternatively set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
4. Deploy, then open the public `https://<your-service>.onrender.com` URL.
5. Test with an address you control and with an intentionally invalid address such as `not-an-email`.

The service processes up to 200 addresses per request and caps request size at 256 KB. It does not persist submitted addresses. Hosting providers may change free-tier availability, sleep behavior, and network policies.
