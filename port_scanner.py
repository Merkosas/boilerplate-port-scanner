import socket
import common_ports

def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    # Validate IP address or hostname
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        if target.replace('.', '').isnumeric():
            return "Error: Invalid IP address"
        else:
            return "Error: Invalid hostname"

    # Scan ports
    for port in range(port_range[0], port_range[1] + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Increased timeout value
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    # Debugging: Print detected open ports
    print(f"Detected open ports for {target}: {open_ports}")

    # Return results
    if verbose:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = None

        if hostname and hostname != ip:
            output = f"Open ports for {hostname} ({ip})\n"
        else:
            output = f"Open ports for {ip}\n"

        output += "PORT     SERVICE\n"
        for port in open_ports:
            service = common_ports.ports_and_services.get(port, "unknown")
            output += f"{port:<9}{service}\n"
        return output.strip()
    else:
        return open_ports
