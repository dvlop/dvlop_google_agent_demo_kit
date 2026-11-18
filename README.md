# Google-Agent request identity check (read-only)

Official Google guidance (published Nov 17, 2026):
https://developers.google.com/crawling/docs/crawlers-fetchers/allow-google-agent

Google's published agent IP list:
https://developers.google.com/static/crawling/ipranges/user-triggered-agents.json

Run from this folder on Mac, Python 3.9+:

```bash
python3 check_agent.py 74.125.232.5 'Google-Agent'
python3 check_agent.py 203.0.113.42 'Google-Agent'
```

These are **test inputs only**. The first is an IP in Google's published range at the time of publication; the second is reserved TEST-NET-3. **They are not real requests or proof of actual visits.** By default script fetches the *latest* official Google ranges over HTTPS.

If offline, use `--offline` to check against a local snapshot of the official Google JSON, captured from the documentation on Nov 18, 2026:

```bash
python3 check_agent.py --offline 74.125.232.5 'Google-Agent'
python3 check_agent.py --offline 203.0.113.42 'Google-Agent'
```

Use the **actual network source IP** as observed by your trusted CDN/edge. Do not accept arbitrary X-Forwarded-For headers. This tool only matches two signals; it does not validate Web Bot Auth signatures. When present, verify signature according to Google. It does not modify WAF settings or authorize access.

For production, use provider-supported verified-bot checks or keep the published ranges current; review rule order, page/challenge rules, APIs and shared-IP limits. Only allow the bot where you intentionally permit agent access.
