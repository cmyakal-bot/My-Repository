from collections import Counter

LOG_FILE = "/home/macky/dns_queries.log"


def read_domains():
    """Read the DNS log and extract domain names."""
    domains = []

    with open(LOG_FILE, "r", encoding="utf-8") as log:
        for line in log:
            line = line.strip()

            if not line:
                continue

            # Expected format: timestamp domain
            parts = line.split(maxsplit=1)

            if len(parts) == 2:
                timestamp, domain = parts
                domains.append(domain)

    return domains


def main():
    domains = read_domains()
    counts = Counter(domains)

    print("\nTop 5 most queried domains:")
    print("-" * 50)

    for rank, (domain, count) in enumerate(
        counts.most_common(5),
        start=1
    ):
        print(f"{rank}. {domain:<35} {count} queries")


if __name__ == "__main__":
    main()
