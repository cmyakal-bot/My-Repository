from collections import Counter

LOG_FILE = "/home/macky/dns_queries.log"

domains = []

with open(LOG_FILE, "r", encoding="utf-8") as log:
    for line in log:
        line = line.strip()

        if not line:
            continue

        parts = line.split(maxsplit=1)

        if len(parts) == 2:
            timestamp, domain = parts
            domains.append(domain)

counts = Counter(domains)

print("\nTop 5 most queried domains:")
print("-" * 45)

for rank, (domain, count) in enumerate(counts.most_common(5), start=1):
    print(f"{rank}. {domain:<35} {count} queries")
