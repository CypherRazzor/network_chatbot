import ipaddress
from typing import Text

class IPAddressValidator:
    @staticmethod
    def is_valid_ipv4(address: Text) -> bool:
        """
        Ueberprueft, ob die angegebene IP-Adresse eine gueltige IPv4-Adresse darstellt.

        Args:
            address (Text): Der zu ueberpruefende IP-Adresse-String.
        
        Returns:
            bool: True, wenn die Adresse eine gueltige IPv4-Adresse ist, sonst False.
        """
        try:
            # Versucht, die Adresse als IPv4-Adresse zu interpretieren.
            ipaddress.IPv4Address(address)
            # Keine Ausnahme bedeutet, dass es eine gueltige IPv4-Adresse ist.
            return True
        except ipaddress.AddressValueError:
            # Wenn eine AddressValueError ausgeloest wird, ist die Adresse keine gueltige IPv4-Adresse.
            return False

    @staticmethod
    def is_valid_ipv6(address: Text) -> bool:
        """
        Ueberprueft, ob die angegebene IP-Adresse eine gueltige IPv6-Adresse darstellt.

        Args:
            address (Text): Der zu ueberpruefende IP-Adresse-String.
        
        Returns:
            bool: True, wenn die Adresse eine gueltige IPv6-Adresse ist, sonst False.
        """
        try:
            # Versucht, die Adresse als IPv6-Adresse zu interpretieren.
            ipaddress.IPv6Address(address)
            # Keine Ausnahme bedeutet, dass es eine gueltige IPv6-Adresse ist.
            return True
        except ipaddress.AddressValueError:
            # Wenn eine AddressValueError ausgeloest wird, ist die Adresse keine gueltige IPv6-Adresse.
            return False

    @staticmethod
    def is_valid_subnet_mask(mask: Text) -> bool:
        """
        Überprüft, ob die angegebene Subnetzmaske eine gültige Subnetzmaske für IPv4 darstellt.

        Args:
            mask (Text): Der zu überprüfende Subnetzmasken-String.
        
        Returns:
            bool: True, wenn die Subnetzmaske gültig ist, sonst False.
        """
        try:
            # Überprüft, ob '/' im String vorhanden ist. Falls nicht, fügt es hinzu.
            if not mask.startswith('/'):
                mask = f'/{mask}'

            # Versucht, ein IPv4 Netzwerk mit der angegebenen Maske zu erstellen.
            # Verwendet die Basisadresse '0.0.0.0' für den Test.
            ipaddress.IPv4Network(f'0.0.0.0{mask}')
            # Keine Ausnahme bedeutet, dass die Maske eine gültige Subnetzmaske ist.
            return True
        except ValueError:
            # Wenn ein ValueError ausgelöst wird, ist die Maske keine gültige Subnetzmaske.
            return False

    @staticmethod
    def is_valid_cidr_range_ipv6(mask: Text) -> bool:
        """
        Überprüft, ob der angegebene String eine gültige CIDR-Notation repräsentiert.
        
        Args:
            mask (Text): Der zu überprüfende CIDR-Notations-String.
        
        Returns:
            bool: True, wenn die Notation gültig ist und sich im Bereich von 0 bis 128 befindet,
                sonst False.
        """
        try:
            # Überprüft, ob '/' im String vorhanden ist.
            if '/' in mask:
                # Teilt den String bei '/' und konvertiert den zweiten Teil in einen Integer.
                prefix = int(mask.split('/')[1])
            else:
                # Annahme, dass der gesamte String die Präfixlänge ist.
                prefix = int(mask)

            # Überprüft, ob der Integerwert innerhalb des gültigen Bereichs für CIDR liegt.
            if 0 <= prefix <= 128:
                return True
            else:
                return False
        except (ValueError, IndexError):
            # Fehlerbehandlung
            return False
        
    @staticmethod
    def is_valid_cidr_range_ipv4(mask: Text) -> bool:
        """
        Überprüft, ob der angegebene String eine gültige CIDR-Notation repräsentiert.
        
        Args:
            mask (Text): Der zu überprüfende CIDR-Notations-String.
        
        Returns:
            bool: True, wenn die Notation gültig ist und sich im Bereich von 0 bis 32 befindet,
                sonst False.
        """
        try:
            # Überprüft, ob '/' im String vorhanden ist.
            if '/' in mask:
                # Teilt den String bei '/' und konvertiert den zweiten Teil in einen Integer.
                prefix = int(mask.split('/')[1])
            else:
                # Annahme, dass der gesamte String die Präfixlänge ist.
                prefix = int(mask)

            # Überprüft, ob der Integerwert innerhalb des gültigen Bereichs für CIDR liegt.
            if 0 <= prefix <= 32:
                return True
            else:
                return False
        except (ValueError, IndexError):
            # Fehlerbehandlung
            return False

    @staticmethod
    def validate_ip_and_mask(ip: Text, mask: Text) -> dict[Text, any]:
        """
        Überprüft die Gültigkeit einer IP-Adresse und einer zugehörigen Subnetzmaske oder CIDR-Range.

        Args:
            ip (Text): Die zu überprüfende IP-Adresse.
            mask (Text): Die zu überprüfende Subnetzmaske oder CIDR-Range.

        Returns:
            Dict[Text, Any]: Ein Dictionary, das den Status der Validierung ('valid': True/False)
                             und eine Nachricht ('message': Text) enthält.
        """
        is_ipv4 = IPAddressValidator.is_valid_ipv4(ip)
        is_ipv6 = IPAddressValidator.is_valid_ipv6(ip)

        if not (is_ipv4 or is_ipv6):
            return {"valid": False, "message": "IP-Adresse ist weder eine gültige IPv4 noch eine IPv6 Adresse."}

        if is_ipv4 == is_ipv6:  # Beide True oder beide False
            return {"valid": False, "message": "IP-Adresse kann nicht gleichzeitig gültig für IPv4 und IPv6 sein."}

        if is_ipv4:
            is_subnet = IPAddressValidator.is_valid_subnet_mask(mask)
            is_cidr_ipv4 = IPAddressValidator.is_valid_cidr_range_ipv4(mask)
            if not (is_subnet or is_cidr_ipv4):
                return {"valid": False, "message": "Bei einer IPv4-Adresse muss entweder die Subnetzmaske oder die CIDR-Range gültig sein, aber nicht beides."}
            return {"valid": True, "message": "IPv4-Adresse und Subnetzmaske/CIDR-Range sind gültig."}

        if is_ipv6:
            if not IPAddressValidator.is_valid_cidr_range_ipv6(mask):
                return {"valid": False, "message": "CIDR-Range ist für eine IPv6-Adresse ungültig."}
            return {"valid": True, "message": "IPv6-Adresse und CIDR-Range sind gültig."}

        return {"valid": False, "message": "Unbekannter Fehler bei der Überprüfung der IP-Adresse und Maske."}
