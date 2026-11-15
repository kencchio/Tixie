"""
history.py - Remembers the last check, so Tixie can tell if the IP changed.
Owner: Jon Christian Bobis

After every successful ticket, we save the IPv4, IPv6 and ISP to a small
file (tickets/history.json). On the next ticket we compare against it.
"""

import json
import os

TICKET_FOLDER = "tickets"
HISTORY_FILE = os.path.join(TICKET_FOLDER, "history.json")


def load_last():
    """Return the last saved check as a dictionary, or None if there isn't one."""
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, ValueError):
        return None  # no file yet, or the file is broken: treat as "first time"


def save_last(ipv4, ipv6, isp, now):
    """Save this check so the next ticket can compare against it."""
    os.makedirs(TICKET_FOLDER, exist_ok=True)
    data = {
        "ipv4": ipv4,
        "ipv6": ipv6,
        "isp": isp,
        "time": now.strftime("%Y-%m-%d %H:%M"),
    }
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def compare_with_last(last, ipv4, ipv6, isp):
    """Return one line of text describing what changed since the last ticket."""
    if last is None:
        return "First ticket from this computer, nothing to compare."

    changes = []
    checks = (("Public IPv4", "ipv4", ipv4),
              ("Public IPv6", "ipv6", ipv6),
              ("ISP", "isp", isp))

    for label, key, new_value in checks:
        if key == "isp" and new_value is None:
            continue  # the ISP lookup failed this time, so we can't say it changed
        old_value = last.get(key)
        if old_value != new_value:
            changes.append(f"{label} changed: {old_value or 'none'} -> {new_value or 'none'}")

    if changes:
        return "; ".join(changes)
    return f"No change since the last ticket ({last.get('time', 'unknown time')})."


# Quick self-test: run "python history.py" to see how comparing works.
if __name__ == "__main__":
    from datetime import datetime
    old = {"ipv4": "203.0.113.5", "ipv6": None, "isp": "Example ISP", "time": "2026-11-15 18:00"}
    print(compare_with_last(None, "1.1.1.1", None, "X"))
    print(compare_with_last(old, "203.0.113.5", None, "Example ISP"))
    print(compare_with_last(old, "198.51.100.7", "2001:db8::1", "Other ISP"))
