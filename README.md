# DNS Query Capture and Top-5 Domain Analysis

A lightweight Python network-monitoring project that uses **Scapy** to capture DNS queries, record queried domains with timestamps, and analyze the captured data to identify the most frequently queried domains.

## Project Objectives

1. Capture DNS queries using Scapy.
2. Run the packet capture for 2 minutes.
3. Extract the domain name from each DNS query.
4. Record the timestamp and domain in a log file.
5. Analyze the log and identify the top 5 most queried domains.

## Technologies Used

- Python 3
- Scapy
- DNS
- `collections.Counter`
- Linux

## Project Structure

```text
dns-query-analyzer/
├── README.md
├── dns_capture.py
├── analyze_dns.py
└── dns_queries.log
```

### File Descriptions

- `dns_capture.py` — captures DNS queries for 120 seconds and logs timestamp + domain.
- `analyze_dns.py` — reads the log and calculates the five most frequently queried domains.
- `dns_queries.log` — generated DNS query data. For a public GitHub repository, consider adding this file to `.gitignore` because DNS logs may reveal network activity.

## Installation

Check Python:

```bash
python3 --version
```

Install Scapy:

```bash
sudo python3 -m pip install scapy
```

If `pip` is not installed on Debian/Ubuntu:

```bash
sudo apt update
sudo apt install python3-pip
```

Then install Scapy:

```bash
sudo python3 -m pip install scapy
```

## Capturing DNS Queries

Run:

```bash
sudo python3 dns_capture.py
```

The program captures DNS queries for 120 seconds.

You should see:

```text
Starting DNS capture for 2 minutes...
Press Ctrl+C to stop early.
```

While the capture is running, DNS activity can be generated from another terminal:

```bash
nslookup google.com
nslookup github.com
nslookup microsoft.com
```

The resulting log is:

```text
dns_queries.log
```

Example:

```text
2026-09-29T16:42:51 veradigm.com
2026-09-29T16:42:53 vituity.com
2026-09-29T16:43:01 bata.com
2026-09-29T16:43:05 connectivity-check.ubuntu.com
```

## Analyzing the Log

After the capture finishes:

```bash
python3 analyze_dns.py
```

Example output:

```text
Top 5 most queried domains:
---------------------------------------------
1. connectivity-check.ubuntu.com       3 queries
2. veradigm.com                        2 queries
3. vituity.com                         2 queries
4. bata.com                            2 queries
5. crowdstrike.com                     2 queries
```

If several domains have the same count, their relative ordering is determined by the order in which they first appear in the log when using `Counter.most_common()`.

## How It Works

The capture program uses Scapy:

```python
sniff(
    filter="udp port 53",
    prn=process_packet,
    store=False,
    timeout=120
)
```

DNS packets are inspected for a DNS query record:

```python
if packet.haslayer(DNS) and packet.haslayer(DNSQR):
```

The program then checks:

```python
if dns.qr == 0:
```

`qr == 0` indicates a DNS query, while `qr == 1` indicates a DNS response.

The queried domain is extracted with:

```python
packet[DNSQR].qname
```

and written together with a timestamp to the log.

The analysis program uses:

```python
Counter(domains)
```

to count domain occurrences and:

```python
counts.most_common(5)
```

to retrieve the top five.

## Example Results

One test capture produced 23 logged DNS query records. The highest observed count was:

```text
connectivity-check.ubuntu.com — 3 queries
```

Several other domains were observed twice, including:

```text
veradigm.com
vituity.com
bata.com
crowdstrike.com
cisco.com
microsoft.com
nvidia.com
intel.com
essar.com
youtube.com
```

Duplicate entries can occur because of retransmissions, resolver behavior, network configuration, or packet-capture environment. This implementation counts each captured query record.

## Troubleshooting

### `ModuleNotFoundError: No module named 'scapy'`

Install Scapy:

```bash
sudo python3 -m pip install scapy
```

Verify:

```bash
python3 -c "import scapy; print(scapy.__version__)"
```

### Permission problems

Run the capture with elevated privileges:

```bash
sudo python3 dns_capture.py
```

### No queries captured

Generate a DNS query:

```bash
nslookup google.com
```

You can also check whether ordinary port-53 DNS traffic is visible:

```bash
sudo tcpdump -i any port 53
```

Modern systems may use encrypted DNS such as DNS-over-HTTPS or DNS-over-TLS. Such traffic will not necessarily expose the requested domain through a simple port-53 capture.

## Security and Authorization

Only capture network traffic on systems and networks where you have permission to monitor traffic. DNS queries can reveal information about applications and domains being accessed.

For a public GitHub repository, avoid committing real DNS logs unless the data is known to be safe to publish. A `.gitignore` entry such as the following is recommended:

```text
dns_queries.log
__pycache__/
*.pyc
```

## Learning Outcomes

This project demonstrates:

- Basic packet capture with Scapy
- DNS protocol inspection
- Distinguishing DNS queries from responses
- Domain extraction
- Timestamped network logging
- Frequency analysis with Python
- Basic network-security monitoring

## Future Improvements

Possible extensions include:

- Capture source IP addresses
- Record destination DNS servers
- Support both UDP and TCP DNS
- Export results to CSV
- Generate charts
- Add real-time statistics
- Build a web dashboard
- Categorize queried domains
- Detect unusually frequent DNS requests

## Conclusion

The project implements a complete DNS-monitoring workflow:

```text
Network Traffic
      ↓
Scapy Packet Capture
      ↓
DNS Query Detection
      ↓
Domain + Timestamp
      ↓
dns_queries.log
      ↓
Frequency Analysis
      ↓
Top 5 Domains
```

It provides a practical introduction to Python-based network monitoring and can serve as a foundation for more advanced DNS and network-security analysis tools.
