"""
main.py - Starts Tixie and runs the menu.
Owner: Ken Sarji Ortega

How to run:  python main.py
This file connects the other files together:
  api.py       (Ken)        gets the data from the internet
  report.py    (Christian)  builds and saves the ticket
  display.py   (Christian)  shows things on screen
  history.py   (Christian)  remembers the last check
  validate.py  (Ken)        checks what the user types
"""

import time
from datetime import datetime

from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn

from api import get_ip_details, get_public_ip
from display import (console, copy_to_clipboard, show_details, show_error, show_greeting,
                     show_menu, show_note, show_report, show_status, show_success)
from history import compare_with_last, load_last, save_last
from report import build_report, make_ticket_id, save_report
from validate import PrivateAddressError, check_ip


def ask(question, default="Not provided"):
    """Ask a question. If the answer is empty, use the default text."""
    answer = console.input(question).strip()
    return answer if answer else default


def create_ticket(technician):
    """Menu option 1: check this computer's network and write a ticket."""
    user = ask("Name of the user who called: ")
    issue = ask("What is the problem? (short description): ")

    # Progress bar: 3 steps (IPv4, IPv6, details). It disappears when done.
    started = time.perf_counter()
    details = {}
    lookup_error = None
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), BarColumn(),
                  TaskProgressColumn(), console=console, transient=True) as bar:
        task = bar.add_task("Finding public IPv4...", total=3)
        ipv4 = get_public_ip(4)
        bar.update(task, advance=1, description="Finding public IPv6...")
        ipv6 = get_public_ip(6)
        bar.update(task, advance=1, description="Looking up location and ISP...")
        online = ipv4 is not None or ipv6 is not None
        if online:
            try:
                details = get_ip_details(ipv4 or ipv6)
            except LookupError as error:
                lookup_error = error
        bar.update(task, advance=1)
    elapsed_ms = int((time.perf_counter() - started) * 1000)

    show_status(ipv4, ipv6, elapsed_ms)
    if not online:
        show_note("No public IP found. The ticket will say the user may be offline.")
    elif lookup_error:
        # Still write the ticket, just without location and ISP.
        show_note(f"{lookup_error} The ticket will be missing location and ISP details.")

    now = datetime.now().astimezone()
    isp = details.get("org")

    # Only compare and save when we actually got an IP, so an offline
    # ticket doesn't overwrite the last good check.
    if online:
        last = load_last()
        change_text = compare_with_last(last, ipv4, ipv6, isp)
        # If the ISP lookup failed this time, keep the ISP we saved before,
        # so the next ticket doesn't report a false "ISP changed".
        isp_to_save = isp or (last or {}).get("isp")
        save_last(ipv4, ipv6, isp_to_save, now)
    else:
        change_text = "Not checked (no connection)."

    ticket_id = make_ticket_id(now)
    text = build_report(ticket_id, now, technician, user, issue,
                        ipv4, ipv6, details, change_text)
    path = save_report(ticket_id, text)

    show_report(text)
    if copy_to_clipboard(text):
        show_success(f"Ticket saved to {path} and copied to your clipboard. Just paste (Ctrl+V) into your helpdesk.")
    else:
        show_success(f"Ticket saved to {path}. Copy the text above into your helpdesk.")


def look_up_other_ip():
    """Menu option 2: ask for any IP address and show its details."""
    text = console.input("Enter an IPv4 or IPv6 address: ")

    try:
        ip = check_ip(text)
    except PrivateAddressError as note:   # must come before ValueError
        show_note(str(note))
        return
    except ValueError as error:
        show_error(str(error))
        return

    try:
        with console.status(f"Looking up {ip}..."):
            details = get_ip_details(ip)
    except LookupError as error:
        show_error(str(error))
        return

    show_details(details, title=f"Details for {ip}")


def main():
    """Greet the technician, then keep showing the menu until they exit."""
    show_greeting()
    technician = ask("Technician name: ", default="Unknown technician")

    while True:
        show_menu()
        choice = console.input("Choose an option (1-3): ").strip()

        if choice == "1":
            create_ticket(technician)
        elif choice == "2":
            look_up_other_ip()
        elif choice == "3":
            console.print("Bye! Tixie is signing off.")
            break
        else:
            show_error("Please type 1, 2 or 3.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C closes the app quietly instead of showing a long error.
        console.print("\nBye! Tixie is signing off.")
