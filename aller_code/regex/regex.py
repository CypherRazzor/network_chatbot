import re
import random
import string
def is_valid_string(test_string, pattern):
    """ Überprüft, ob die gegebene IP-Adresse dem Regex-Muster entspricht. """
    if re.match(pattern, test_string):
        return True
    else:
        return False

def add_random_chars_around_string(s, num_chars=5):
    """ Fügt eine bestimmte Anzahl von Nicht-Zahlen-Zeichen sowohl vor als auch hinter einem String hinzu. """
    # Erzeugt eine zufällige Zeichenfolge aus Buchstaben und Sonderzeichen für beide Seiten
    random_chars_before = ''.join(random.choices(string.ascii_letters + string.punctuation, k=num_chars))
    random_chars_after = ''.join(random.choices(string.ascii_letters + string.punctuation, k=num_chars))

    # Fügt die zufälligen Zeichenfolgen vor und hinter dem gegebenen String ein
    return random_chars_before + s + random_chars_after

ipv4_edge_cases = [
    "-1.-1.-1.-1",
    "1.0.0.0",
    "1.1.0.0",
    "1.1.1.0",
    "1.1.1.1",
    "0.1.0.0",
    "0.0.1.0",
    "0.0.0.1",
    "0.0.0.0",
    "1.0.1.1",
    "10.0.0.0",
    "127.0.10.0",
    "255.255.255.255",
    "256.256.256.256"
]

false_ip_addresses = [
    "650.267.760.931",
    "536.904.645.408",
    "692.403.787.776",
    "704.450.590.430",
    "533.420.664.781",
    "295.839.337.740",
    "299.561.968.796",
    "368.649.993.434",
    "826.912.678.623",
    "325.707.589.504",
    "758.482.645.268",
    "265.845.287.952",
    "768.862.269.772",
    "574.710.331.530",
    "839.730.973.495",
    "465.296.407.783",
    "464.378.425.942",
    "389.729.551.438",
    "978.605.891.733",
    "529.836.654.272"
]

correct_ip_addresses = [
    "183.250.98.226",
    "23.170.178.254",
    "108.235.106.210",
    "178.84.152.191",
    "131.250.70.137",
    "232.34.17.15",
    "40.177.146.255",
    "20.192.151.15",
    "35.211.166.254",
    "83.0.83.74",
    "247.228.21.246",
    "226.93.224.199",
    "153.226.227.157",
    "95.48.224.34",
    "11.38.97.240",
    "67.176.109.84",
    "35.20.183.73",
    "109.84.198.247",
    "59.62.227.197",
    "238.223.173.198",
    "33.144.173.116",
    "239.65.24.136",
    "144.255.60.48",
    "158.12.125.18",
    "136.132.154.90",
    "64.101.220.18",
    "99.45.219.89",
    "215.95.39.98",
    "2.204.146.156",
    "88.0.60.121",
    "18.232.83.23",
    "11.99.101.227",
    "61.97.132.34",
    "93.102.225.2",
    "45.202.47.180",
    "154.178.223.86",
    "243.105.192.211",
    "86.39.28.197",
    "47.183.86.153",
    "138.134.27.19"
]

all_subnetmasks = [
    "128.0.0.0",
    "192.0.0.0",
    "224.0.0.0",
    "240.0.0.0",
    "248.0.0.0",
    "252.0.0.0",
    "254.0.0.0",
    "255.0.0.0",
    "255.128.0.0",
    "255.192.0.0",
    "255.224.0.0",
    "255.240.0.0",
    "255.248.0.0",
    "255.252.0.0",
    "255.254.0.0",
    "255.255.0.0",
    "255.255.128.0",
    "255.255.192.0",
    "255.255.224.0",
    "255.255.240.0",
    "255.255.248.0",
    "255.255.252.0",
    "255.255.254.0",
    "255.255.255.0",
    "255.255.255.128",
    "255.255.255.192",
    "255.255.255.224",
    "255.255.255.240",
    "255.255.255.248",
    "255.255.255.252",
    "255.255.255.254",
    "255.255.255.255",
]

# Regex-Muster für eine IPv4-Adresse
ipv4_pattern = r'(((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]).){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]))'

# Testen des Skripts
for test_array in [ipv4_edge_cases, false_ip_addresses, correct_ip_addresses, all_subnetmasks]:
    for test in test_array:
        test_with_random_chars = add_random_chars_around_string(test, num_chars=5)
        if is_valid_string(test_with_random_chars, ipv4_pattern):
            print(f"Gültiger String: {test_with_random_chars}")
        else:
            print(f"Ungültiger String: {test_with_random_chars}")