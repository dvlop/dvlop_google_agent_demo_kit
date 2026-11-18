#!/usr/bin/env python3
"""Read-only verifier for Google-Agent request IP + User-Agent signals.

By default downloads Google's current published IP ranges over HTTPS.
Use --offline for a dated demo snapshot with no network access.
This is NOT Web Bot Auth signature verification and makes no firewall edits.
"""
import argparse
import ipaddress
import json
import sys
import urllib.request
from pathlib import Path

SOURCE = 'https://developers.google.com/static/crawling/ipranges/user-triggered-agents.json'
SNAPSHOT = Path(__file__).with_name('google-agent-ranges-2026-11-18.json')


def load_data(offline):
    if offline:
        return json.loads(SNAPSHOT.read_text(encoding='utf-8'))
    request = urllib.request.Request(SOURCE, headers={'User-Agent': 'GoogleAgentIPCheck/1.0'})
    with urllib.request.urlopen(request, timeout=12) as response:
        return json.load(response)


def check(ip_text, ua, data):
    ip = ipaddress.ip_address(ip_text)
    ranges = [ipaddress.ip_network(entry.get('ipv4Prefix') or entry.get('ipv6Prefix'))
              for entry in data['prefixes']]
    return ('Google-Agent' in ua, any(ip in net for net in ranges), len(ranges))


def main():
    p = argparse.ArgumentParser(description='Verify Google-Agent UA + published egress IP range')
    p.add_argument('ip', help='Actual network source IP (not untrusted X-Forwarded-For)')
    p.add_argument('user_agent', help='Full User-Agent value or Google-Agent for demo')
    p.add_argument('--offline', action='store_true', help='Use dated local Google ranges snapshot')
    args = p.parse_args()
    try:
        data = load_data(args.offline)
        ua_match, ip_match, n = check(args.ip, args.user_agent, data)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f'ERROR: Unable to check: {exc}', file=sys.stderr)
        return 2
    print(f'Source : {"OFFLINE GOOGLE SNAPSHOT" if args.offline else "GOOGLE HTTPS LIVE"}')
    print(f'Ranges : {n} | created: {data.get("creationTime", "unknown")}')
    print(f'UA     : {"MATCH" if ua_match else "NO MATCH"} (contains Google-Agent)')
    print(f'IP     : {"IN GOOGLE AGENT RANGES" if ip_match else "OUTSIDE GOOGLE AGENT RANGES"}')
    print('RESULT : ' + ('UA + IP consistent with Google-Agent' if ua_match and ip_match
                        else 'NOT verified: do not bypass bot protection'))
    print('NOTE   : If a request is signed, verify Web Bot Auth separately.')
    return 0 if ua_match and ip_match else 1


if __name__ == '__main__':
    sys.exit(main())
