import requests
import unittest
import uuid

class TestActions(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5055/webhook/"
        self.sender_id = str(uuid.uuid4())

    def create_check_ip_input(self, ipv6=None, ipv4=None, subnet_mask=None, cidr_mask=None):
        slots = {}
        if ipv6 is not None:
            slots["ipv6"] = ipv6
        if ipv4 is not None:
            slots["ipv4"] = ipv4
        if subnet_mask is not None:
            slots["subnet_mask"] = subnet_mask
        if cidr_mask is not None:
            slots["cidr_mask"] = cidr_mask

        return {
            "next_action": "action_check_ip_address",
            "sender_id": self.sender_id,
            "tracker": {
                "sender_id": self.sender_id,
                "slots": slots,
                "latest_message": {
                    "intent": {
                        "name": "check_ip_address"
                    }
                }
            }
        }
    
    def perform_check_ip_test(self, ipv6=None, ipv4=None, subnet_mask=None, cidr_mask=None, expected_text=None):
            # Erstellen des Eingabeobjekts mit den entsprechenden Slots
            check_ip_input = self.create_check_ip_input(ipv6, ipv4, subnet_mask, cidr_mask)

            # Senden der Anfrage und Empfangen der Antwort
            response = requests.post(self.url, json=check_ip_input)
            response_data = response.json()

            # Überprüfen, ob die Antwort wie erwartet ist
            self.assertEqual(response_data['responses'][0]['text'], expected_text)

    def test_full_ipv6_address(self):
        ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        expected_text = f"Die Adresse {ipv6} ist eine gueltige IPv6-Adresse. Wie kann ich dir mit dieser IPv6-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_compressed_ipv6_address(self):
        ipv6 = "2001:db8:85a3::8a2e:370:7334"
        expected_text = f"Die Adresse {ipv6} ist eine gueltige IPv6-Adresse. Wie kann ich dir mit dieser IPv6-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_loopback_address(self):
        ipv6 = "::1"
        expected_text = f"Die Adresse {ipv6} ist eine gueltige IPv6-Adresse. Wie kann ich dir mit dieser IPv6-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_link_local_address(self):
        ipv6 = "fe80::1"
        expected_text = f"Die Adresse {ipv6} ist eine gueltige IPv6-Adresse. Wie kann ich dir mit dieser IPv6-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_multicast_address(self):
        ipv6 = "ff02::1"
        expected_text = f"Die Adresse {ipv6} ist eine gueltige IPv6-Adresse. Wie kann ich dir mit dieser IPv6-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_unique_local_address(self):
        ipv6 = "fc00::1"
        expected_text = f"Die Adresse {ipv6} ist eine gueltige IPv6-Adresse. Wie kann ich dir mit dieser IPv6-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_simplified_address(self):
        ipv6 = "2001:db8::1"
        expected_text = f"Die Adresse {ipv6} ist eine gueltige IPv6-Adresse. Wie kann ich dir mit dieser IPv6-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_with_leading_zeros(self):
        ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:0001"
        expected_text = f"Die Adresse {ipv6} ist eine gueltige IPv6-Adresse. Wie kann ich dir mit dieser IPv6-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_all_zeros(self):
        ipv6 = "0000:0000:0000:0000:0000:0000:0000:0001"
        expected_text = f"Die Adresse {ipv6} ist eine gueltige IPv6-Adresse. Wie kann ich dir mit dieser IPv6-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_all_zeros(self):
        ipv6 = "0000:0000:0000:0000:0000:0000:0000:0000"
        expected_text = f"Die Adresse {ipv6} ist eine gueltige IPv6-Adresse. Wie kann ich dir mit dieser IPv6-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_too_long(self):
        ipv6 = "2001:0db8:0000:0000:0000:0000:8a2e:0370:7334"
        expected_text = f"Die Adresse {ipv6} ist keine gueltige IPv6-Adresse. Gib mir bitte eine gueltige IPv6-Adresse."
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_missing_segments(self):
        ipv6 = "2001:0db8:85a3:8a2e:370"
        expected_text = f"Die Adresse {ipv6} ist keine gueltige IPv6-Adresse. Gib mir bitte eine gueltige IPv6-Adresse."
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_with_invalid_characters(self):
        ipv6 = "2001:0db8:85a3:0000:0000:8g2e:0370:7334"
        expected_text = f"Die Adresse {ipv6} ist keine gueltige IPv6-Adresse. Gib mir bitte eine gueltige IPv6-Adresse."
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_with_leading_zeros(self):
        ipv6 = "00001:0db8:85a3:0000:0000:8a2e:0370:7334"
        expected_text = f"Die Adresse {ipv6} ist keine gueltige IPv6-Adresse. Gib mir bitte eine gueltige IPv6-Adresse."
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_with_extra_colon(self):
        ipv6 = "2001:0db8::85a3::8a2e:0370:7334"
        expected_text = f"Die Adresse {ipv6} ist keine gueltige IPv6-Adresse. Gib mir bitte eine gueltige IPv6-Adresse."
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_with_decimal(self):
        ipv6 = "2001.0db8.85a3.0000.0000.8a2e.0370.7334"
        expected_text = f"Die Adresse {ipv6} ist keine gueltige IPv6-Adresse. Gib mir bitte eine gueltige IPv6-Adresse."
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_with_incorrect_compression(self):
        ipv6 = "2001:0db8::85a3:0000:8a2e:0370::7334"
        expected_text = f"Die Adresse {ipv6} ist keine gueltige IPv6-Adresse. Gib mir bitte eine gueltige IPv6-Adresse."
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_with_letters_beyond_f(self):
        ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7g34"
        expected_text = f"Die Adresse {ipv6} ist keine gueltige IPv6-Adresse. Gib mir bitte eine gueltige IPv6-Adresse."
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_ipv6_address_with_special_characters(self):
        ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334#"
        expected_text = f"Die Adresse {ipv6} ist keine gueltige IPv6-Adresse. Gib mir bitte eine gueltige IPv6-Adresse."
        self.perform_check_ip_test(ipv6=ipv6, expected_text=expected_text)

    def test_valid_ipv4_address_1(self):
        ipv4 = "192.168.1.1"
        expected_text = f"Die Adresse {ipv4} ist eine gueltige IPv4-Adresse. Wie kann ich dir mit dieser IPv4-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_valid_ipv4_address_2(self):
        ipv4 = "10.0.0.1"
        expected_text = f"Die Adresse {ipv4} ist eine gueltige IPv4-Adresse. Wie kann ich dir mit dieser IPv4-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_valid_ipv4_address_3(self):
        ipv4 = "172.16.0.1"
        expected_text = f"Die Adresse {ipv4} ist eine gueltige IPv4-Adresse. Wie kann ich dir mit dieser IPv4-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_valid_ipv4_address_4(self):
        ipv4 = "8.8.8.8"
        expected_text = f"Die Adresse {ipv4} ist eine gueltige IPv4-Adresse. Wie kann ich dir mit dieser IPv4-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_valid_ipv4_address_5(self):
        ipv4 = "127.0.0.1"
        expected_text = f"Die Adresse {ipv4} ist eine gueltige IPv4-Adresse. Wie kann ich dir mit dieser IPv4-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_valid_ipv4_address_6(self):
        ipv4 = "255.255.255.255"
        expected_text = f"Die Adresse {ipv4} ist eine gueltige IPv4-Adresse. Wie kann ich dir mit dieser IPv4-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_valid_ipv4_address_7(self):
        ipv4 = "192.0.2.1"
        expected_text = f"Die Adresse {ipv4} ist eine gueltige IPv4-Adresse. Wie kann ich dir mit dieser IPv4-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_valid_ipv4_address_8(self):
        ipv4 = "203.0.113.1"
        expected_text = f"Die Adresse {ipv4} ist eine gueltige IPv4-Adresse. Wie kann ich dir mit dieser IPv4-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_valid_ipv4_address_9(self):
        ipv4 = "100.64.0.1"
        expected_text = f"Die Adresse {ipv4} ist eine gueltige IPv4-Adresse. Wie kann ich dir mit dieser IPv4-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_valid_ipv4_address_10(self):
        ipv4 = "169.254.0.1"
        expected_text = f"Die Adresse {ipv4} ist eine gueltige IPv4-Adresse. Wie kann ich dir mit dieser IPv4-Adresse weiterhelfen?"
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_invalid_ipv4_address_1(self):
        ipv4 = "192.168.1.256"
        expected_text = f"Die Adresse {ipv4} ist keine gueltige IPv4-Adresse. Gib mir bitte eine gueltige IPv4-Adresse."
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_invalid_ipv4_address_2(self):
        ipv4 = "10.0.0.300"
        expected_text = f"Die Adresse {ipv4} ist keine gueltige IPv4-Adresse. Gib mir bitte eine gueltige IPv4-Adresse."
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_invalid_ipv4_address_3(self):
        ipv4 = "172.16.0.-1"
        expected_text = f"Die Adresse {ipv4} ist keine gueltige IPv4-Adresse. Gib mir bitte eine gueltige IPv4-Adresse."
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_invalid_ipv4_address_4(self):
        ipv4 = "8.8.8.8.8"
        expected_text = f"Die Adresse {ipv4} ist keine gueltige IPv4-Adresse. Gib mir bitte eine gueltige IPv4-Adresse."
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_invalid_ipv4_address_5(self):
        ipv4 = "127.0.0.0.1"
        expected_text = f"Die Adresse {ipv4} ist keine gueltige IPv4-Adresse. Gib mir bitte eine gueltige IPv4-Adresse."
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_invalid_ipv4_address_6(self):
        ipv4 = "255.255.255.255.255"
        expected_text = f"Die Adresse {ipv4} ist keine gueltige IPv4-Adresse. Gib mir bitte eine gueltige IPv4-Adresse."
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_invalid_ipv4_address_7(self):
        ipv4 = "192.0.2.1.1"
        expected_text = f"Die Adresse {ipv4} ist keine gueltige IPv4-Adresse. Gib mir bitte eine gueltige IPv4-Adresse."
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_invalid_ipv4_address_8(self):
        ipv4 = "203.0.113"
        expected_text = f"Die Adresse {ipv4} ist keine gueltige IPv4-Adresse. Gib mir bitte eine gueltige IPv4-Adresse."
        self.perform_check_ip_test(ipv4=ipv4, expected_text=expected_text)

    def test_invalid_cidr_mask_1(self):
        cidr_mask = "/33"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist gueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_invalid_cidr_mask_2(self):
        cidr_mask = "/0"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist gueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_invalid_cidr_mask_3(self):
        cidr_mask = "/-1"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist ungueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_invalid_cidr_mask_4(self):
        cidr_mask = "/40"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist gueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_invalid_cidr_mask_4_5(self):
        cidr_mask = "/128"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist gueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_invalid_cidr_mask_4_4(self):
        cidr_mask = "/129"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist ungueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_invalid_cidr_mask_5(self):
        cidr_mask = "/abc"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist ungueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_valid_cidr_mask_1(self):
        cidr_mask = "/24"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist gueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_valid_cidr_mask_2(self):
        cidr_mask = "/16"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist gueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_valid_cidr_mask_3(self):
        cidr_mask = "/8"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist gueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_valid_cidr_mask_4(self):
        cidr_mask = "/32"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist gueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_valid_cidr_mask_5(self):
        cidr_mask = "/30"
        expected_text = f"Die CIDR-Maske {cidr_mask} ist gueltig."
        self.perform_check_ip_test(cidr_mask=cidr_mask, expected_text=expected_text)

    def test_invalid_subnet_mask_1(self):
        subnet_mask = "255.255.255.255"
        expected_text = f"Die Subnetzmaske {subnet_mask} ist gueltig."
        self.perform_check_ip_test(subnet_mask=subnet_mask, expected_text=expected_text)

    def test_invalid_subnet_mask_2(self):
        subnet_mask = "255.255.255.1"
        expected_text = f"Die Subnetzmaske {subnet_mask} ist ungueltig."
        self.perform_check_ip_test(subnet_mask=subnet_mask, expected_text=expected_text)

    def test_invalid_subnet_mask_3(self):
        subnet_mask = "255.0.255.0"
        expected_text = f"Die Subnetzmaske {subnet_mask} ist ungueltig."
        self.perform_check_ip_test(subnet_mask=subnet_mask, expected_text=expected_text)

    def test_invalid_subnet_mask_4(self):
        subnet_mask = "0.0.0.0"
        expected_text = f"Die Subnetzmaske {subnet_mask} ist gueltig."
        self.perform_check_ip_test(subnet_mask=subnet_mask, expected_text=expected_text)

    def test_invalid_subnet_mask_5(self):
        subnet_mask = "255.255.0.255"
        expected_text = f"Die Subnetzmaske {subnet_mask} ist ungueltig."
        self.perform_check_ip_test(subnet_mask=subnet_mask, expected_text=expected_text)

    def test_valid_subnet_mask_1(self):
        subnet_mask = "255.255.255.0"
        expected_text = f"Die Subnetzmaske {subnet_mask} ist gueltig."
        self.perform_check_ip_test(subnet_mask=subnet_mask, expected_text=expected_text)

    def test_valid_subnet_mask_2(self):
        subnet_mask = "255.255.0.0"
        expected_text = f"Die Subnetzmaske {subnet_mask} ist gueltig."
        self.perform_check_ip_test(subnet_mask=subnet_mask, expected_text=expected_text)

    def test_valid_subnet_mask_3(self):
        subnet_mask = "255.0.0.0"
        expected_text = f"Die Subnetzmaske {subnet_mask} ist gueltig."
        self.perform_check_ip_test(subnet_mask=subnet_mask, expected_text=expected_text)

    def test_valid_subnet_mask_4(self):
        subnet_mask = "255.255.255.128"
        expected_text = f"Die Subnetzmaske {subnet_mask} ist gueltig."
        self.perform_check_ip_test(subnet_mask=subnet_mask, expected_text=expected_text)

    def test_valid_subnet_mask_5(self):
        subnet_mask = "255.255.255.192"
        expected_text = f"Die Subnetzmaske {subnet_mask} ist gueltig."
        self.perform_check_ip_test(subnet_mask=subnet_mask, expected_text=expected_text)

    def test_valid_ipadress_no_input(self):
        expected_text = "Keine Subnetz-, CIDR-, IPv4- oder IPv6-Adresse angegeben."
        self.perform_check_ip_test(expected_text=expected_text)

    def create_network_details_input(self, ipv6=None, ipv4=None, subnet_mask=None, cidr_mask=None):
        slots = {}
        if ipv6 is not None:
            slots["ipv6"] = ipv6
        if ipv4 is not None:
            slots["ipv4"] = ipv4
        if subnet_mask is not None:
            slots["subnet_mask"] = subnet_mask
        if cidr_mask is not None:
            slots["cidr_mask"] = cidr_mask

        return {
            "next_action": "action_calculate_network_details",
            "sender_id": self.sender_id,
            "tracker": {
                "sender_id": self.sender_id,
                "slots": slots,
                "latest_message": {
                    "intent": {
                        "name": "calculate_network_details"
                    }
                }
            }
        }

    def perform_network_details_test(self, ipv6=None, ipv4=None, subnet_mask=None, cidr_mask=None, expected_text=None):
        # Erstellen des Eingabeobjekts mit den entsprechenden Slots
        network_details_input = self.create_network_details_input(ipv6, ipv4, subnet_mask, cidr_mask)
        # Senden der Anfrage und Empfangen der Antwort
        response = requests.post(self.url, json=network_details_input)
        response_data = response.json()
        # Überprüfen, ob die Antwort wie erwartet ist
        self.assertEqual(response_data['responses'][0]['text'], expected_text)
      
    def test_ipv4_with_valid_cidr_mask_1(self):
            ipv4 = "198.51.100.0"
            cidr_mask = "27"
            expected_text = "Netzadresse: 198.51.100.0\nBroadcastadresse: 198.51.100.31\nAnzahl der Hosts: 30\nHostbereich: 198.51.100.1 - 198.51.100.30"
            self.perform_network_details_test(ipv4=ipv4, cidr_mask=cidr_mask, expected_text=expected_text)

    def test_ipv4_with_valid_cidr_mask_2(self):
            ipv4 = "192.0.2.0"
            cidr_mask = "29"
            expected_text = "Netzadresse: 192.0.2.0\nBroadcastadresse: 192.0.2.7\nAnzahl der Hosts: 6\nHostbereich: 192.0.2.1 - 192.0.2.6"
            self.perform_network_details_test(ipv4=ipv4, cidr_mask=cidr_mask, expected_text=expected_text)

    def test_ipv4_with_valid_cidr_mask_3(self):
            ipv4 = "172.16.0.0"
            cidr_mask = "20"
            expected_text = "Netzadresse: 172.16.0.0\nBroadcastadresse: 172.16.15.255\nAnzahl der Hosts: 4094\nHostbereich: 172.16.0.1 - 172.16.15.254"
            self.perform_network_details_test(ipv4=ipv4, cidr_mask=cidr_mask, expected_text=expected_text)

    def test_ipv4_with_valid_cidr_mask_4(self):
            ipv4 = "10.0.0.0"
            cidr_mask = "16"
            expected_text = "Netzadresse: 10.0.0.0\nBroadcastadresse: 10.0.255.255\nAnzahl der Hosts: 65534\nHostbereich: 10.0.0.1 - 10.0.255.254"
            self.perform_network_details_test(ipv4=ipv4, cidr_mask=cidr_mask, expected_text=expected_text)

    def test_ipv4_with_valid_cidr_mask_5(self):
            ipv4 = "192.168.0.0"
            cidr_mask = "24"
            expected_text = "Netzadresse: 192.168.0.0\nBroadcastadresse: 192.168.0.255\nAnzahl der Hosts: 254\nHostbereich: 192.168.0.1 - 192.168.0.254"
            self.perform_network_details_test(ipv4=ipv4, cidr_mask=cidr_mask, expected_text=expected_text)

    def test_ipv4_with_valid_cidr_mask_6(self):
            ipv4 = "0.0.0.0"
            cidr_mask = "0"
            expected_text = "Netzadresse: 0.0.0.0\nBroadcastadresse: 255.255.255.255\nAnzahl der Hosts: 4294967294\nHostbereich: 0.0.0.1 - 255.255.255.254"
            self.perform_network_details_test(ipv4=ipv4, cidr_mask=cidr_mask, expected_text=expected_text)

    def test_ipv4_with_valid_cidr_mask_7(self):
            ipv4 = "123.123.123.123"
            cidr_mask = "32"
            expected_text = "Netzadresse: 123.123.123.123\nBroadcastadresse: 123.123.123.123\nAnzahl der Hosts: 1\nHostbereich: 123.123.123.123 - 123.123.123.123"
            self.perform_network_details_test(ipv4=ipv4, cidr_mask=cidr_mask, expected_text=expected_text)

if __name__ == '__main__':
    unittest.main()
