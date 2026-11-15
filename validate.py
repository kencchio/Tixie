"""
validate.py - Checks the IP address the user types in.
Owner: Ken Sarji Ortega

We use Python's built-in "ipaddress" module, so nothing extra to install.
"""

import ipaddress


class PrivateAddressError(ValueError):
    """Raised when the address is valid but private (like 192.168.1.10).

    Private addresses only exist inside a local network, so the
    online API can't give any information about them.
    """


def check_ip(text):
    """Check what the user typed and return the cleaned-up IP address.

    Raises ValueError if it's not a real IPv4 or IPv6 address.
    Raises PrivateAddressError if it's a private or reserved address.
    """
    text = text.strip()  # remove spaces before and after

    try:
        ip = ipaddress.ip_address(text)  # works for both IPv4 and IPv6
    except ValueError:
        raise ValueError(f"'{text}' is not a valid IPv4 or IPv6 address.")

    # is_global is False for private, loopback and other reserved addresses.
    if not ip.is_global:
        raise PrivateAddressError(
            f"{ip} is a private or reserved address, so it can't be looked up online."
        )

    return str(ip)


# Quick self-test: run "python validate.py" to check a few examples.
if __name__ == "__main__":
    examples = ["8.8.8.8", "2001:4860:4860::8888", "192.168.1.10", "192.168.1.300", "hello"]
    for example in examples:
        try:
            print(f"{example:<22} -> OK: {check_ip(example)}")
        except PrivateAddressError as note:
            print(f"{example:<22} -> PRIVATE: {note}")
        except ValueError as error:
            print(f"{example:<22} -> INVALID: {error}")
