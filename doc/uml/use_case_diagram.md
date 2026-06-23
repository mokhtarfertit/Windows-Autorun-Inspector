# Use Case Diagram

The use case diagram shows the main actions that the user can perform with **WinPersist Hunter**.

```mermaid
flowchart LR
    User["Security Analyst / User"]

    User --> Scan["Run Scan"]
    User --> Baseline["Create Baseline"]
    User --> Compare["Compare With Baseline"]
    User --> View["View Results"]
    User --> Report["Generate Report"]

    Scan --> Analyze["Analyze Persistence Entries"]
    Compare --> Analyze
    Analyze --> View
    View --> Report
```

## Explanation

- **Run Scan:** Inspect Windows persistence locations.
- **Create Baseline:** Save the current clean system state.
- **Compare With Baseline:** Detect new, removed, or modified entries.
- **View Results:** Show detected entries and risk levels.
- **Generate Report:** Export the final analysis report.