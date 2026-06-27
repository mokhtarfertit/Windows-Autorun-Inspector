from app.collectors.startup_collector import StartupCollector

def main():
    collector = StartupCollector()
    entries = collector.collect()

    print(f"Found {len(entries)} startup folder entries")

    for entry in entries:
        print("-" * 60)
        print(f"name: {entry['name']}")
        print(f"Path: {entry['path']}")
        print(f"Startup folder: {entry['startup_folder']}")
        print(f"Timestamp: {entry['timestamp']}")

if __name__ == "__main__":
    main()