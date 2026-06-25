from app.collectors.registry_collector import RegistryCollector

def main():
    collector = RegistryCollector()
    entries = collector.collect()

    print(f"Found {len(entries)} registry autorun entries")

    for entrey in entries:
        print("-" * 60)
        print(f"Name: {entrey['name']}")
        print(f"Command: {entrey['command']}")
        print(f"Registry path: {entrey['registry_path']}")
        print(f"Timestamp: {entrey['timestamp']}")

if __name__ == "__main__":
    main()