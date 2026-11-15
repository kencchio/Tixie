"""
api.py - Gets IP address information from the internet (used by Tixie).
Owner: Ken Sarji Ortega

This file talks to two free online services (APIs):
  - ipify     -> tells us this computer's public IPv4 and IPv6 address
  - ipapi.co  -> tells us details about any public IP address
                 (location, ISP/organization, ASN, timezone)

Neither one needs an API key.
"""

import requests

# How many seconds to wait for a website before giving up.
# Without this, the app could freeze if a website is slow.
TIMEOUT = 5


def get_public_ip(version):
    """Return this computer's public IP address as text.

    version: 4 for IPv4, or 6 for IPv6.
    Returns None if the address can't be found, for example when
    there is no internet, or when the network has no IPv6.
    """
    if version == 4:
        url = "https://api.ipify.org"   # IPv4 only
    else:
        url = "https://api6.ipify.org"  # IPv6 only (fails if the network has no IPv6)

    try:
        response = requests.get(url, params={"format": "json"}, timeout=TIMEOUT)
        response.raise_for_status()      # treat error pages (like 500) as failures
        return response.json()["ip"]     # the reply looks like {"ip": "203.0.113.5"}
    except (requests.RequestException, ValueError, KeyError):
        return None


def get_ip_details(ip):
    """Return a dictionary of details about one public IP address.

    Example keys: ip, version, city, region, country_name, country_code,
    org, asn, timezone, latitude, longitude.

    Raises LookupError with a message we can show the user if anything fails.
    """
    url = f"https://ipapi.co/{ip}/json/"

    try:
        # Some APIs reject requests that don't say which app is calling,
        # so we send a simple "User-Agent" name.
        response = requests.get(url, timeout=TIMEOUT,
                                headers={"User-Agent": "ip-lens/1.0"})
    except requests.RequestException:
        raise LookupError("Could not reach ipapi.co. Check your internet connection.")

    # 429 means "too many requests": the free daily limit was reached.
    if response.status_code == 429:
        raise LookupError("The daily lookup limit on ipapi.co was reached. Try again later.")

    try:
        data = response.json()
    except ValueError:
        raise LookupError(f"ipapi.co sent an unexpected reply (status {response.status_code}).")

    # ipapi.co replies with {"error": true, "reason": "..."} when it can't look something up.
    if data.get("error"):
        reason = data.get("reason", "unknown reason")
        raise LookupError(f"ipapi.co could not look up {ip}: {reason}")

    return data


# Quick self-test: run "python api.py" to check that this file works on its own.
if __name__ == "__main__":
    print("My public IPv4:", get_public_ip(4))
    print("My public IPv6:", get_public_ip(6), "(None is normal if your network has no IPv6)")
    print("Details for 8.8.8.8:")
    try:
        print(get_ip_details("8.8.8.8"))
    except LookupError as error:
        print("Lookup failed:", error)
