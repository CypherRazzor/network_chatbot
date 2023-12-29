import ipaddress
from validators import IPAddressValidator

def calculate_subnet_details(subnet_input):
    if not subnet_input:
        return {"error": "Leere Eingabe"}

    try:
        ip, mask = subnet_input.split('/')
    except ValueError:
        return {"error": "Ungültiges Eingabeformat. Erwartet wird 'IP/Maske'."}

    # Validierung der IP-Adresse und der Maske/CIDR-Range
    validation_result = IPAddressValidator.validate_ip_and_mask(ip, mask)
    if not validation_result["valid"]:
        return {"error": validation_result["message"]}

    # Erstellung des Netzwerks und Berechnung der Details
    try:
        network = ipaddress.ip_network(subnet_input, strict=False)

        network_address = str(network.network_address)
        cidr = str(network.prefixlen)

        if network.version == 4:
            ip_version = "IPv4"
            broadcast_address = str(network.broadcast_address)
            netmask = str(network.netmask)
            num_hosts = network.num_addresses - 2
            first_host = str(network.network_address + 1)
            last_host = str(network.broadcast_address - 1)
        else:
            ip_version = "IPv6"
            broadcast_address = ""
            netmask = ""
            num_hosts = network.num_addresses - 1
            first_host = str(network.network_address + 1)
            last_host = str(network[-1])

        host_range = f"{first_host} - {last_host}"

        return {
            "subnet_input": subnet_input,
            "ip_version": ip_version,
            "network_address": network_address,
            "broadcast_address": broadcast_address,
            "num_hosts": num_hosts,
            "host_range": host_range,
            "cidr": cidr,
            "netmask": netmask
        }
    except Exception as e:
        return {"error": f"Fehler bei der Berechnung der Details: {e}"}
