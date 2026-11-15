# Tixie

A command-line Python helper for helpdesk technicians. When a user calls with a network problem,
Tixie checks their public IP situation and writes a **ready-to-paste support ticket**.
Made by **BaThreeBonia** for DEVASC Project Activity 3

## What it does

- Finds the computer's public **IPv4** and **IPv6** address
- Gets the **ISP, ASN, location (with country code) and timezone** for that address
- Says in plain English whether the network is **dual-stack, IPv4 only, IPv6 only, or offline**
- Remembers the last check and tells you if the **IP or ISP changed** since the previous ticket
- Writes a **timestamped ticket** and saves it as a text file in the `tickets/` folder
- Looks up **any other public IP** you type in (invalid and private addresses are caught)
- Shows a **progress bar** while it checks, then a **connection check** (green tick or red cross for each address, and how long it took)
- **Copies the ticket to the clipboard** so you can paste it straight into a helpdesk (Windows only)
- Shows extra details for any IP: UTC offset, postal code, currency, calling code and languages
- Handles problems: no internet, no IPv6, or the free API's daily limit (the ticket is still written)

## What a ticket looks like

```
=========== TIXIE SUPPORT TICKET ===========
Ticket ID:    TIX-20261115-182030
Created:      2026-11-15 18:20 (UTC+0800)
Technician:   Ken
User:         Maria
Issue:        Slow internet

--- NETWORK SNAPSHOT ---
Public IPv4:  203.0.113.5
Public IPv6:  Not available
IP status:    IPv4 only (no working IPv6 on this network)
ISP / Org:    Example ISP
ASN:          AS64500
Location:     Quezon City, Metro Manila, Philippines (PH)
Timezone:     Asia/Manila
Since last:   No change since the last ticket (2026-11-15 17:55).

--- TECHNICIAN NOTES ---

=============================================
```

## How to run it

1. Install Python 3 from https://www.python.org (on Windows, tick **"Add python.exe to PATH"**).
2. Open a terminal in this folder and install the two libraries:

   ```
   pip install -r requirements.txt
   ```

3. Start the app:

   ```
   python main.py
   ```

4. Type your name, then pick an option: `1` creates a ticket, `2` looks up another IP, `3` exits.
   After option 1, the ticket is already on your clipboard. Press Ctrl+V to paste it.

Tickets are saved in a `tickets/` folder that Tixie creates by itself.

## Files

| File | What it does | Owner |
| --- | --- | --- |
| `main.py` | Starts the app and runs the menu | Ken Sarji Ortega |
| `api.py` | Gets data from the ipify and ipapi.co APIs | Ken Sarji Ortega |
| `report.py` | Builds the ticket text and saves it to a file | Jon Christian Bobis |
| `display.py` | Shows the menu, tables, tickets and messages in color | Jon Christian Bobis |
| `history.py` | Remembers the last check and spots changes | Jon Christian Bobis |
| `validate.py` | Checks that a typed IP address is valid and public | Ken Sarji Ortega |
| `requirements.txt` | The libraries to install (`requests`, `rich`) | |

Each file can also be run on its own (for example `python api.py`) as a quick test.

## APIs used

- **ipify** (https://www.ipify.org): `api.ipify.org` for IPv4 and `api6.ipify.org` for IPv6. No key needed.
- **ipapi.co** (https://ipapi.co): `https://ipapi.co/<ip>/json/` for address details. No key needed, but the free tier has a daily limit.

## How to continue this project

To add a feature, create a new branch from `main`, make your changes, and open a pull request.
Another team member reviews it before it's merged.

## Backlog (future features for Project Activity 4)

- [ ] "Before and after" mode: compare a snapshot before and after a fix (router reboot, VPN on)
- [ ] Check the IPs in a log file and flag ones from unexpected countries
- [ ] Add a website name and report who hosts it
- [ ] Export all tickets to one CSV file
- [ ] Clipboard copy for Mac and Linux (it only works on Windows now)
- [ ] Simple window-based version (GUI)

## Team

- Ken Sarji Ortega (scrum leader)
- Jon Christian Bobis (recorder)
- Miko Andrei Pelpinosas (architecture owner)
