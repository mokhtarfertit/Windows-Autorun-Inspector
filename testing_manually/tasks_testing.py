from app.collectors.tasks_collector import TaskCollector

def main():
    collector = TaskCollector()
    entries = collector.collect()

    print(f"Found {len(entries)} scheduled task entries")

    for entry in entries[:20]:
        print("-" * 60)
        print(f"Name: {entry['name']}")
        print(f"Path: {entry['path']}")
        print(f"State: {entry['state']}")
        print(f"Source: {entry['source']}")
        print(f"MITRE: {entry['mitre_technique']}")
        print(f"timestamp: {entry['timestamp']}")


if __name__ == "__main__":
    main()
