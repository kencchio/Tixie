"""
report.py - Builds the support ticket text and saves it to a file.
Owner: Jon Christian Bobis

The ticket is plain text, so a technician can paste it straight into a
helpdesk system, an email, or a chat message.
"""

import os

TICKET_FOLDER = "tickets"


def make_ticket_id(now):
    """Make a ticket number from the date and time, e.g. TIX-20261115-182030."""
    return now.strftime("TIX-%Y%m%d-%H%M%S")


def ip_status(ipv4, ipv6):
    """Return a plain-English verdict about the user's IP connectivity."""
    if ipv4 and ipv6:
        return "Dual-stack (IPv4 and IPv6 both working)"
    if ipv4:
        return "IPv4 only (no working IPv6 on this network)"
    if ipv6:
        return "IPv6 only"
    return "No public IP found (the user may be offline)"


def _location(details):
    """Join city, region and country into one line."""
    if not details:
        return "Not available"
    parts = [details.get("city"), details.get("region"), details.get("country_name")]
    text = ", ".join(part for part in parts if part)
    if details.get("country_code"):
        text += f" ({details.get('country_code')})"
    return text or "Not available"


def build_report(ticket_id, now, technician, user, issue, ipv4, ipv6, details, change_text):
    """Return the whole ticket as one block of text.

    details is the dictionary from api.get_ip_details(); it can be empty
    if that lookup failed, and the ticket still works.
    """
    time_text = now.strftime("%Y-%m-%d %H:%M") + " (UTC" + now.strftime("%z") + ")"
    details = details or {}

    lines = [
        "=========== TIXIE SUPPORT TICKET ===========",
        f"Ticket ID:    {ticket_id}",
        f"Created:      {time_text}",
        f"Technician:   {technician}",
        f"User:         {user}",
        f"Issue:        {issue}",
        "",
        "--- NETWORK SNAPSHOT ---",
        f"Public IPv4:  {ipv4 or 'Not found'}",
        f"Public IPv6:  {ipv6 or 'Not available'}",
        f"IP status:    {ip_status(ipv4, ipv6)}",
        f"ISP / Org:    {details.get('org') or 'Not available'}",
        f"ASN:          {details.get('asn') or 'Not available'}",
        f"Location:     {_location(details)}",
        f"Timezone:     {details.get('timezone') or 'Not available'}",
        f"Since last:   {change_text}",
        "",
        "--- TECHNICIAN NOTES ---",
        "",
        "=============================================",
    ]
    return "\n".join(lines)


def save_report(ticket_id, text):
    """Save the ticket to tickets/<ticket id>.txt and return that file path."""
    os.makedirs(TICKET_FOLDER, exist_ok=True)
    path = os.path.join(TICKET_FOLDER, f"{ticket_id}.txt")
    with open(path, "w", encoding="utf-8") as file:
        file.write(text + "\n")
    return path


# Quick self-test: run "python report.py" to print a sample ticket.
if __name__ == "__main__":
    from datetime import datetime
    sample = {"org": "Example ISP", "asn": "AS64500", "city": "Quezon City",
              "region": "Metro Manila", "country_name": "Philippines",
              "country_code": "PH", "timezone": "Asia/Manila"}
    moment = datetime.now().astimezone()
    print(build_report(make_ticket_id(moment), moment, "Ken", "Maria",
                       "Slow internet", "203.0.113.5", None, sample,
                       "First ticket from this computer, nothing to compare."))
