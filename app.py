from flask import Flask, render_template, request, jsonify
import re
import dns.resolver
import dns.exception

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 256 * 1024  # 256 KB request limit

EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$")

def check_email(raw):
    email = raw.strip()
    result = {"email": email, "status": "unknown", "reason": ""}
    if not email:
        return None

    if len(email) > 254 or not EMAIL_RE.fullmatch(email):
        result.update(status="likely_bounce", reason="The address does not match the expected email format.")
        return result

    domain = email.rsplit("@", 1)[1].rstrip(".").lower()
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=3)
        if any(str(record.exchange).strip(".") != "" for record in answers):
            result.update(
                status="likely_delivered",
                reason="The domain publishes mail servers. The individual mailbox has not been verified."
            )
            return result

        result.update(status="likely_bounce", reason="The domain has no usable mail exchanger (MX) record.")
        return result
    except dns.resolver.NoAnswer:
        # Some domains accept mail through their address records when no MX exists (RFC 5321 fallback).
        try:
            dns.resolver.resolve(domain, "A", lifetime=2)
            result.update(status="unknown", reason="No MX record found; the domain may use fallback mail routing, so delivery is uncertain.")
        except Exception:
            try:
                dns.resolver.resolve(domain, "AAAA", lifetime=2)
                result.update(status="unknown", reason="No MX record found; fallback mail routing may be possible, so delivery is uncertain.")
            except Exception:
                result.update(status="likely_bounce", reason="No MX record or usable address record could be found for the domain.")
        return result
    except dns.resolver.NXDOMAIN:
        result.update(status="likely_bounce", reason="The email domain does not exist in DNS.")
        return result
    except (dns.resolver.NoNameservers, dns.exception.Timeout, dns.resolver.LifetimeTimeout):
        result.update(status="unknown", reason="DNS lookup failed or timed out; the address could not be assessed.")
        return result
    except Exception:
        result.update(status="unknown", reason="The domain could not be checked reliably.")
        return result

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/check")
def api_check():
    payload = request.get_json(silent=True) or {}
    raw_text = payload.get("emails", "")
    if not isinstance(raw_text, str):
        return jsonify({"error": "Please submit email addresses as text."}), 400
    lines = [line.strip() for line in re.split(r"[\n,;\t ]+", raw_text) if line.strip()]
    if not lines:
        return jsonify({"error": "Paste at least one email address."}), 400
    if len(lines) > 200:
        return jsonify({"error": "Please check 200 addresses or fewer per batch."}), 400
    results = [check_email(item) for item in lines]
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
