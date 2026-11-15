"""
display.py - Shows everything on screen with colors, tables and panels.
Owner: Jon Christian Bobis

We use the "rich" library so results show up as neat colored tables
instead of raw text.
"""

import subprocess

from rich import box
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# One shared "console" that every file uses to print.
console = Console()


def show_greeting():
    """Print Tixie's welcome message."""
    console.print(Panel(
        "[bold cyan]Hi, I'm Tixie![/bold cyan]  Your remote user triage helper.\n"
        "I check a user's network and write the support ticket for you.\n"
        "[dim]Tip: press Ctrl+C any time to quit.[/dim]",
        title="Tixie", border_style="cyan"))


def show_menu():
    """Print the main menu."""
    table = Table(box=box.ROUNDED, show_header=False, border_style="cyan")
    table.add_column(style="bold cyan", justify="center")
    table.add_column()
    table.add_row("1", "Create a new support ticket")
    table.add_row("2", "Look up another IP address")
    table.add_row("3", "Exit")
    console.print()
    console.print(table)


def show_status(ipv4, ipv6, online_ms):
    """Print a quick connection check: green tick or red cross per address."""
    def mark(value, missing):
        return f"[green]✔ {escape(value)}[/green]" if value else f"[red]✘ {missing}[/red]"
    console.print(Panel(
        f"IPv4: {mark(ipv4, 'not found')}\n"
        f"IPv6: {mark(ipv6, 'not available')}\n"
        f"Check took: [bold]{online_ms} ms[/bold]",
        title="Connection check", border_style="green" if (ipv4 or ipv6) else "red"))


def _clean(value):
    """Turn a value into safe text for the table. Empty values become '-'."""
    if value is None or value == "":
        return "-"
    # escape() stops text like "[something]" from being read as a color code.
    return escape(str(value))


def show_details(details, title="IP Information"):
    """Print the details of one IP address inside a panel."""
    country = details.get("country_name")
    if details.get("country_code"):
        country = f"{country} ({details.get('country_code')})"

    latitude = details.get("latitude")
    longitude = details.get("longitude")
    coordinates = f"{latitude}, {longitude}" if latitude is not None else None

    rows = [
        ("IP address", details.get("ip")),
        ("IP version", details.get("version")),
        ("City", details.get("city")),
        ("Region", details.get("region")),
        ("Country", country),
        ("ISP / Organization", details.get("org")),
        ("ASN", details.get("asn")),
        ("Timezone", details.get("timezone")),
        ("UTC offset", details.get("utc_offset")),
        ("Postal code", details.get("postal")),
        ("Currency", details.get("currency_name")),
        ("Calling code", details.get("country_calling_code")),
        ("Languages", details.get("languages")),
        ("Coordinates", coordinates),
    ]
    lines = Text()
    for label, value in rows:
        lines.append(f"{label + ':':<20}", style="bold")
        lines.append(f"{'-' if value in (None, '') else value}\n")
    lines.rstrip()

    console.print(Panel(lines, title=title, border_style="green"))


def show_report(text):
    """Print the finished ticket inside a panel."""
    # Text() prints the ticket exactly as written, with no color codes applied.
    console.print(Panel(Text(text), title="Your ticket", border_style="green"))


def copy_to_clipboard(text):
    """Put text on the clipboard. Returns True if it worked."""
    try:
        # "clip" is built into Windows and reads the piped text as UTF-16.
        # ponytail: Windows only, add pyperclip if Tixie must run on Mac/Linux
        subprocess.run("clip", input=text.encode("utf-16-le"), check=True)
        return True
    except Exception:
        return False


def show_success(message):
    """Print a success message in green."""
    console.print(f"[bold green]Done:[/bold green] {escape(message)}")


def show_error(message):
    """Print an error message in red."""
    console.print(f"[bold red]Error:[/bold red] {escape(message)}")


def show_note(message):
    """Print a warning or note in yellow."""
    console.print(f"[bold yellow]Note:[/bold yellow] {escape(message)}")


# Quick self-test: run "python display.py" to see what the output looks like.
if __name__ == "__main__":
    show_greeting()
    show_menu()
    show_details({"ip": "8.8.8.8", "version": "IPv4", "city": "Mountain View",
                  "region": "California", "country_name": "United States",
                  "country_code": "US", "org": "GOOGLE", "asn": "AS15169",
                  "timezone": "America/Los_Angeles", "latitude": 37.42,
                  "longitude": -122.08}, title="Sample table (fake data)")
    show_report("Sample ticket text [not a color code]")
    show_success("This is what success looks like.")
    show_error("This is what an error looks like.")
    show_note("This is what a note looks like.")
