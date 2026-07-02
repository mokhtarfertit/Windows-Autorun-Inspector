from app.collectors.services_collector import ServiceCollector


def main():
    collector = ServiceCollector()
    entries = collector.collect()

    print(f"Found {len(entries)} service entries")

    for entry in entries[:20]:
        print("-" * 60)
        print(f"Name: {entry['name']}")
        print(f"Display name: {entry['display_name']}")
        print(f"State: {entry['state']}")
        print(f"Start mode: {entry['start_mode']}")
        print(f"Path: {entry['path']}")
        print(f"timestamp: {entry['timestamp']}")


if __name__ == "__main__":
    main()