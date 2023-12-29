import requests
import unittest
import uuid
import subprocess
import sys
import time

# Docker-Container-Steuerung
class MyServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            # Pfad zur docker-compose.yml Datei
            docker_compose_file = "../docker-compose.yml"

            # Erstellen der Docker-Images
            subprocess.run(["docker-compose", "-f", docker_compose_file, "build"], check=True)

            # Starten der Container
            subprocess.run(["docker-compose", "-f", docker_compose_file, "up", "-d"], check=True)

            # Warten bis der Container hochgefahren ist
            cls.wait_for_container_start()
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Aufbauen oder Starten der Docker-Container: {e}", file=sys.stderr)
            sys.exit(1)

    @classmethod
    def wait_for_container_start(cls, timeout=60):
        start_time = time.time()
        while True:
            try:
                # Ersetzen Sie die URL mit der URL Ihres Dienstes
                response = requests.get("http://localhost:5055/health")
                if response.status_code == 200:
                    break
            except requests.ConnectionError:
                pass

            if time.time() - start_time > timeout:
                raise TimeoutError("Docker Container noch nicht gestartet. Warte 1 Minute.")
            time.sleep(60)  # Warten für 15 Sekunde vor dem nächsten Versuch

    @classmethod
    def tearDownClass(cls):
        try:
            # Pfad zur docker-compose.yml Datei
            docker_compose_file = "../docker-compose.yml"

            # Stoppen der Container
            subprocess.run(["docker-compose", "-f", docker_compose_file, "down"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Stoppen der Docker-Container: {e}", file=sys.stderr)

# Rasa Actions Tests
class TestActions(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5055/webhook/"
        self.sender_id = str(uuid.uuid4())

    def create_network_details_input(self, ip=None, mask=None, combined_ip_and_mask=None):
        slots = {
            "ip": ip,
            "mask": mask,
            "combined_ip_and_mask": combined_ip_and_mask
        }

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
    
    def perform_network_details_test(self, ip=None, mask=None, combined_ip_and_mask=None, expected_text=None):
        # Erstellen des Eingabeobjekts mit den entsprechenden Slots
        network_details_input = self.create_network_details_input(ip, mask, combined_ip_and_mask)

        # Senden der Anfrage und Empfangen der Antwort
        response = requests.post(self.url, json=network_details_input)
        response_data = response.json()

        # Überprüfen, ob die Antwort wie erwartet ist
        self.assertIn('text', response_data['responses'][0])
        self.assertEqual(response_data['responses'][0]['text'], expected_text)

    def test_valid_ip_and_mask(self):
        ip = "192.168.1.1"
        mask = "24"
        expected_text = (
            "Netzwerkdetails: IP-Version: IPv4, "
            "Netzwerkadresse: 192.168.1.0, "
            "Broadcast-Adresse: 192.168.1.255, "
            "Anzahl Hosts: 254, "
            "Host-Bereich: 192.168.1.1 - 192.168.1.254, "
            "CIDR: 24, "
            "Netzmaske: 255.255.255.0"
        )
        self.perform_network_details_test(ip=ip, mask=mask, expected_text=expected_text)


if __name__ == '__main__':
    # Kombiniertes Ausführen beider Testklassen
    unittest.main()
