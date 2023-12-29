import unittest
from calculateSubnet import calculate_subnet_details
import random
import ipaddress

def random_ipv4_cidr():
    ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}." \
         f"{random.randint(0, 255)}.{random.randint(0, 255)}"
    cidr = random.randint(0, 32)  
    #print(f"{ip}/{cidr}")
    return f"{ip}/{cidr}"

class TestCalculateSubnetDetailsIPv4RandomCIDR(unittest.TestCase):
    
    def test_ipv4_random_valid_inputs(self):
        print("\nTest zufälliger gültiger IPv4-Adressen mit CIDR-Masken\n")
        test_data = [random_ipv4_cidr() for _ in range(10)]
        for ip in test_data:
            with self.subTest(ip=ip):
                try:
                    result = calculate_subnet_details(ip)
                    network = ipaddress.ip_network(ip, strict=False)
                    #print(f"Ergebnis für {ip}: {result}")
                    #print(result['subnet_input'] == ip)  # Die Zeile, die den Fehler verursacht

                    # Benutzerdefinierte Fehlermeldungen für jede Assertion
                    self.assertEqual(result['subnet_input'], ip, f"Fehler: Subnet-Input stimmt nicht überein bei {ip}")
                    self.assertEqual(result['ip_version'], "IPv4", f"Fehler: IP-Version stimmt nicht überein bei {ip}")
                    self.assertEqual(result['network_address'], str(network.network_address), f"Fehler: Netzwerk-Adresse stimmt nicht überein bei {ip}")
                    self.assertEqual(result['broadcast_address'], str(network.broadcast_address), f"Fehler: Broadcast-Adresse stimmt nicht überein bei {ip}")
                    self.assertEqual(result['num_hosts'], network.num_addresses - 2, f"Fehler: Anzahl der Hosts stimmt nicht überein bei {ip}")
                    first_host = str(network.network_address + 1)
                    last_host = str(network.broadcast_address - 1)
                    self.assertEqual(result['host_range'], f"{first_host} - {last_host}", f"Fehler: Host-Bereich stimmt nicht überein bei {ip}")
                    self.assertEqual(result['cidr'], str(network.prefixlen), f"Fehler: CIDR stimmt nicht überein bei {ip}")
                    self.assertEqual(result['netmask'], str(network.netmask), f"Fehler: Netmask stimmt nicht überein bei {ip}")

                    # Erfolgsmeldung
                    print(f"{ip} erfolgreich getestet.")

                except AssertionError as e:
                    # Benutzerdefinierte Fehlermeldung
                    print(f"Fehler: {ip}: {e}")

def random_ipv6_cidr():
    # Erzeugen einer vollständigen IPv6-Adresse
    full_ip = ":".join(f"{random.randint(0, 65535):x}" for _ in range(8))

    # Entscheiden, ob und wo die Adresse verkürzt werden soll
    if random.choice([True, False]):
        blocks = full_ip.split(':')
        # Suchen nach einer Sequenz von Nullen zum Kürzen
        best_seq_start, best_seq_len = 0, 0
        seq_start, seq_len = None, 0
        for i, block in enumerate(blocks):
            if block == "0":
                if seq_start is None:
                    seq_start = i
                seq_len += 1
                if seq_len > best_seq_len:
                    best_seq_start, best_seq_len = seq_start, seq_len
            else:
                seq_start, seq_len = None, 0

        # Kürzen der längsten Sequenz von Nullen, wenn vorhanden
        if best_seq_len > 1:
            full_ip = ":".join(blocks[:best_seq_start] + [""] + blocks[best_seq_start + best_seq_len:])
            full_ip = full_ip.replace(':::', '::')

    # Hinzufügen der CIDR-Notation
    cidr = random.randint(0, 128)
    return f"{full_ip}/{cidr}"

# Anpassung der Testklasse für IPv6
class TestCalculateSubnetDetailsIPv6Random(unittest.TestCase):
    
    def test_ipv6_random_valid_inputs(self):
        print("\nTest zufälliger gültiger IPv6-Adressen mit CIDR-Masken\n")
        test_data = [random_ipv6_cidr() for _ in range(10)]
        for ip in test_data:
            with self.subTest(ip=ip):
                try:
                    result = calculate_subnet_details(ip)  # Diese Funktion muss IPv6 unterstützen
                    network = ipaddress.ip_network(ip, strict=False)

                    self.assertEqual(result['subnet_input'], ip, f"Fehler: Subnet-Input stimmt nicht überein bei {ip}")
                    self.assertEqual(result['ip_version'], "IPv6", f"Fehler: IP-Version stimmt nicht überein bei {ip}")
                    self.assertEqual(result['network_address'], str(network.network_address), f"Fehler: Netzwerk-Adresse stimmt nicht überein bei {ip}")
                    self.assertEqual(result['broadcast_address'], "", f"Fehler: Broadcast-Adresse sollte leer sein bei {ip}")
                    self.assertEqual(result['num_hosts'], network.num_addresses - 1, f"Fehler: Anzahl der Hosts stimmt nicht überein bei {ip}")
                    first_host = str(network.network_address + 1)
                    last_host = str(network[-1])
                    self.assertEqual(result['host_range'], f"{first_host} - {last_host}", f"Fehler: Host-Bereich stimmt nicht überein bei {ip}")
                    self.assertEqual(result['cidr'], str(network.prefixlen), f"Fehler: CIDR stimmt nicht überein bei {ip}")
                    self.assertEqual(result['netmask'], "", f"Fehler: Netmask sollte leer sein bei {ip}")

                    print(f"{ip} erfolgreich getestet.")

                except AssertionError as e:
                    print(f"Fehler bei der Prüfung von {ip}: {e}")

def generate_random_ipv4_subnet():
    # Generiert eine zufällige IP-Adresse
    ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}." \
         f"{random.randint(0, 255)}.{random.randint(0, 255)}"
    
    # Generiert eine zufällige CIDR-Notation zwischen 1 und 31
    cidr = random.randint(0, 32)

    # Umwandlung der CIDR-Notation in eine Subnetzmaske
    mask = [0, 0, 0, 0]
    for i in range(cidr):
        mask[i//8] = mask[i//8] + (1 << (7 - i % 8))

    subnet_mask = '.'.join(map(str, mask))
    return f"{ip}/{subnet_mask}"

class TestCalculateSubnetDetailsIPv4RandomSubnet(unittest.TestCase):
    
    def test_ipv4_random_valid_inputs_subnets(self):
        print("\nTest zufälliger gültiger IPv4-Adressen mit Subnetzmasken\n")
        test_data = [generate_random_ipv4_subnet() for _ in range(10)]

        for ip in test_data:
            with self.subTest(ip=ip):
                try:
                    result = calculate_subnet_details(ip)
                    network = ipaddress.ip_network(ip, strict=False)
                    # Überprüfung und benutzerdefinierte Fehlermeldungen
                    self.assertEqual(result['subnet_input'], ip, f"Fehler: Subnet-Input stimmt nicht überein bei {ip}")
                    self.assertEqual(result['ip_version'], "IPv4", f"Fehler: IP-Version stimmt nicht überein bei {ip}")
                    self.assertEqual(result['network_address'], str(network.network_address), f"Fehler: Netzwerk-Adresse stimmt nicht überein bei {ip}")
                    self.assertEqual(result['broadcast_address'], str(network.broadcast_address), f"Fehler: Broadcast-Adresse stimmt nicht überein bei {ip}")
                    self.assertEqual(result['num_hosts'], network.num_addresses - 2, f"Fehler: Anzahl der Hosts stimmt nicht überein bei {ip}")
                    first_host = str(network.network_address + 1)
                    last_host = str(network.broadcast_address - 1)
                    self.assertEqual(result['host_range'], f"{first_host} - {last_host}", f"Fehler: Host-Bereich stimmt nicht überein bei {ip}")
                    self.assertEqual(result['cidr'], str(network.prefixlen), f"Fehler: CIDR stimmt nicht überein bei {ip}")
                    self.assertEqual(result['netmask'], str(network.netmask), f"Fehler: Netmask stimmt nicht überein bei {ip}")

                    # Erfolgsmeldung
                    print(f"{ip} erfolgreich getestet.")

                except AssertionError as e:
                    # Benutzerdefinierte Fehlermeldung
                    print(f"Fehler bei der Prüfung von {ip}: {e}")

#class TestCalculateSubnetDetailsInvalidIPv4v6(unittest.TestCase):
#    def assertSubnetCalculation(self, input_data, expected_error):
#        with self.subTest(input_data=input_data):
#            result = calculate_subnet_details(input_data)
#            self.assertIn("error", result)
#            self.assertIn(expected_error, result["error"])
#
#    def test_invalid_ipv6_addresses(self):
#        test_cases = [
#            ("2001:0db8:85a3:0000:0000:8a2e:0370:7334x/64", "Ungültige IP-Adresse"),
#            ("2001::85a3::8a2e:0370:7334/64", "Ungültige IP-Adresse"),
#            ("2001:db8:85a3:0:0:8a2e:370g:7334/64", "Ungültige IP-Adresse"),
#            ("1234:5678:9abc:def::/64", "Ungültige IP-Adresse"),
#            ("12345::6789/129", "Ungültige CIDR-Notation"),
#        ]
#        
#        for input_data, expected_error in test_cases:
#            self.assertSubnetCalculation(input_data, expected_error)
#
#    def test_invalid_cidr_masks_ipv6(self):
#        test_cases = [
#            ("2001:db8::/129", "Ungültige CIDR-Notation"),
#            ("::1/130", "Ungültige CIDR-Notation"),
#            ("2001:db8::/48/", "Ungültige CIDR-Notation"),
#            ("2001:db8::/-5", "Ungültige CIDR-Notation"),
#            ("2001:db8::/abc", "Ungültige CIDR-Notation"),
#        ]
#        
#        for input_data, expected_error in test_cases:
#            self.assertSubnetCalculation(input_data, expected_error)
#
#    def test_invalid_cidr_masks_ipv4(self):
#        test_cases = [
#            ("192.168.1.0/33", "Ungültige CIDR-Notation"),
#            ("192.168.1.0/-1", "Ungültige CIDR-Notation"),
#            ("192.168.1.0/abc", "Ungültige CIDR-Notation"),
#            ("192.168.1.256/24", "Ungültige IP-Adresse"),
#        ]
#        
#        for input_data, expected_error in test_cases:
#            self.assertSubnetCalculation(input_data, expected_error)
#
#    def test_other_invalid_inputs(self):
#        test_cases = [
#            ("/64", "Ungültige CIDR-Notation"),
#            ("1234", "Ungültige CIDR-Notation"),
#            ("2001:db8::/64/another/64", "Ungültige CIDR-Notation"),
#        ]
#        
#        for input_data, expected_error in test_cases:
#            self.assertSubnetCalculation(input_data, expected_error)

                    
if __name__ == '__main__':
    unittest.main(buffer=False)
