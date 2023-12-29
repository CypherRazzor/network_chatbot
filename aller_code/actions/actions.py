from datetime import datetime
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from calculateSubnet import calculate_subnet_details
from validators import IPAddressValidator

class ActionTellTime(Action):
    def name(self) -> Text:
        # Name der Action, der in der Domain-Datei verwendet wird
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender_id = tracker.sender_id
        # Holen der aktuellen Zeit
        current_time = datetime.now().strftime("%H:%M:%S")

        # Erstellen der Antwortnachricht
        response = f"Die aktuelle Uhrzeit ist {current_time}."

        # Senden der Antwortnachricht an den Benutzer
        dispatcher.utter_message(text=response)

        return []

class ActionCheckIPAddress(Action):
    def name(self):
        return "action_check_ip_address"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        ip = tracker.get_slot("ip")
        mask = tracker.get_slot("mask")
        combined_ip_and_mask = tracker.get_slot("combined_ip_and_mask")

        if combined_ip_and_mask:
            ip, mask = self.extract_ip_and_mask(combined_ip_and_mask)
            result = IPAddressValidator.validate_ip_and_mask(ip, mask)
        elif ip:
            # Validierung der IP-Adresse eingefügt
            is_ipv4 = IPAddressValidator.is_valid_ipv4(ip)
            is_ipv6 = IPAddressValidator.is_valid_ipv6(ip)
            if is_ipv4 or is_ipv6:
                result = {"valid": True, "message": f"Die IP-Adresse {ip} ist gültig."}
            else:
                result = {"valid": False, "message": f"Die IP-Adresse {ip} ist ungültig."}
        elif mask:
            # Validierung der Maske
            if IPAddressValidator.is_valid_subnet_mask(mask):
                result = {"valid": True, "message": f"Die Subnetzmaske {mask} ist gültig."}
            elif IPAddressValidator.is_valid_cidr_range_ipv4(mask) or IPAddressValidator.is_valid_cidr_range_ipv6(mask):
                result = {"valid": True, "message": f"Die CIDR-Range {mask} ist gültig."}
            else:
                result = {"valid": False, "message": f"Die Maske {mask} ist ungültig."}
        else:
            dispatcher.utter_message(text="Es wurde keine IP-Adresse oder Maske gefunden.")
            return []

        dispatcher.utter_message(text=result["message"])

        return []

    @staticmethod
    def extract_ip_and_mask(combined_ip_and_mask):
        ip, mask = combined_ip_and_mask.split('/')
        return ip, mask
class ActionCalculateNetworkDetails(Action):
    def name(self):
        return "action_calculate_network_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        ip = tracker.get_slot('ip')
        mask = tracker.get_slot('mask')
        combined_ip_and_mask = tracker.get_slot('combined_ip_and_mask')
        
        if combined_ip_and_mask is not None:
            subnet_input = combined_ip_and_mask
        elif ip is not None and mask is not None:
            subnet_input = ip + "/" + mask
        result = calculate_subnet_details(subnet_input)

        # Erzeugen einer Nachricht basierend auf dem Ergebnis
        if 'error' in result:
            response_message = result['error']
        else:
            response_message = (
                f"Netzwerkdetails: IP-Version: {result['ip_version']}, "
                f"Netzwerkadresse: {result['network_address']}, "
                f"Broadcast-Adresse: {result['broadcast_address']}, "
                f"Anzahl Hosts: {result['num_hosts']}, "
                f"Host-Bereich: {result['host_range']}, "
                f"CIDR: {result['cidr']}, "
                f"Netzmaske: {result['netmask']}"
            )

        dispatcher.utter_message(text=response_message)

        return []
    
import re
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionExtractIpAndMask(Action):
    def name(self):
        return "validate_network_form"

    @staticmethod
    def find_match(text, pattern_dict):
        for key, pattern in pattern_dict.items():
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return None

    async def run(self, dispatcher, tracker, domain):
        text = tracker.latest_message.get('text', '')

        # Dictionary der Regex-Muster für IP-Adressen
        ip_patterns = {
            "ipv4": r"(((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]{1}[0-9]|[0-9]).){1}((25[0-5]|2[0-4][0-9]|[1]{1}[0-9]{2}|[1-9]{1}[0-9]|[0-9]).){2}((25[0-5]|2[0-4][0-9]|[1]{1}[0-9]{2}|[1-9]{1}[0-9]|[0-9]){1}))",  # Beispiel für IPv4-Muster
            # Fügen Sie hier weitere Muster hinzu, falls erforderlich
        }

        # Dictionary der Regex-Muster für Subnetzmasken
        mask_patterns = {
            "cidr": r"\/(12[0-8]|1[0-1]\d|[1-9]?[0-9]|)\b",  # Beispiel für CIDR Subnetzmaske
            # Fügen Sie hier weitere Muster hinzu, falls erforderlich
        }

        # Suche nach einem passenden Muster in der Nutzereingabe
        ip = self.find_match(text, ip_patterns)
        mask = self.find_match(text, mask_patterns)

        # Setzen der Slots 'ip' und 'mask', falls Werte gefunden wurden
        return [SlotSet("ip", ip), SlotSet("mask", mask)]
