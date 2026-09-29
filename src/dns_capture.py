from scapy.all import sniff, DNS, DNSQR
from datetime import datetime
import time

LOG_FILE = "dns_queries.log"
DURATION = 120  # 2 minutes


def process_packet(packet):
    if packet.haslayer(DNS) and packet.haslayer(DNSQR):
        dns = packet[DNS]

        # Only process DNS queries, not responses
        if dns.qr == 0:
            domain = packet[DNSQR].qname.decode("utf-8").rstrip(".")
            timestamp = datetime.now().isoformat(timespec="seconds")

            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"{timestamp} {domain}\n")

            print(f"{timestamp} {domain}")


print("Starting DNS capture for 2 minutes...")
print("Press Ctrl+C to stop early.")

sniff(
    filter="udp port 53",
    prn=process_packet,
    store=False,
    timeout=DURATION
)

print("DNS capture complete.")
print(f"Queries saved to {LOG_FILE}")

