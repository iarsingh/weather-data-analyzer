# Weather Data Analyzer: process flows

## Domain request

Endpoint: `POST /analyze`. Input: rows with city and temp_c. The processing stages below summarize [analyze.py](../src/weather/analyze.py); they are local function behavior, not externally executed tools.

```mermaid
flowchart TD
  A["POST /analyze"] --> B{"Non-empty list of objects?"}
  B -->|"No"| E["HTTP 422"]
  B -->|"Yes"| P["Try float conversion for each temp_c"]
  P --> S["Skip invalid, boolean, non-finite, or out-of-range values"]
  S --> C{"At least one numeric value?"}
  C -->|"No"| E
  C -->|"Yes"| V["Sort valid values; group by city"]
  V --> O["Return summary, standard deviation, and city sample counts"]
```

Refusal responses, where implemented, are normal domain results rather than successful execution of a requested write. Detailed edge cases are covered in [INTERVIEW_QA.md](../INTERVIEW_QA.md).

## Workspace and job approval

```mermaid
flowchart TD
  C["Create tenant-scoped workspace"] --> J["Submit job: workspace + payload + target"]
  J --> V{"Workspace belongs to selected tenant?"}
  V -->|"No"| E["HTTP 404"]
  V -->|"Yes"| P{"Normalized target is prod or production?"}
  P -->|"Yes"| Q["pending_approval"]
  P -->|"No"| L["queued"]
  Q --> A["Approval request"]
  A --> X["HTTP 403: production apply disabled"]
  L --> B["Approval request"]
  B --> K["approved: status update only"]
  K --> S["No executor / no production apply"]
```

Approval first checks job ownership using the selected tenant. Status changes and audit records remain in memory. Repeated lab approval returns the original approval without duplicating its event or counter. Ops transitions are protected by an in-process lock. The domain request flow and this job-record flow are independent. Source: [ops.py](../src/weather/ops.py).
