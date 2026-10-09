# Evidence guide

This directory is reserved for evidence collected during an authorized run. Live AWS evidence is **pending** in this repository.

## Where screenshots go

Use these two logical locations under `docs/evidence/`:

- `live/` — screenshots or exported output captured from the live AWS console, an authorized live host, or a real request to the deployed endpoint.
- `local/` — local previews, file inspections, PNG metadata checks, and other artifacts that describe repository files only.

Create the subdirectory only when adding evidence. Do not mix live and local artifacts in the same folder.

## Naming convention

Use a stable, descriptive name with an evidence class and timestamp, for example:

```text
live/2026-10-10T1430Z-ec2-public-ip.png
live/2026-10-10T1435Z-nginx-http-response.png
local/2026-10-10T1440Z-architecture-png-check.txt
```

Use the actual capture time and timezone. Do not invent timestamps for evidence that has not been collected.

## Live versus local

Every evidence note or filename must make its source clear:

| Label | What it may establish | What it cannot establish |
| --- | --- | --- |
| `live` | A timestamped observation from the authorized AWS environment or deployed endpoint. | Anything outside the captured scope or time. |
| `local` | That a repository file, diagram, or local rendering exists and is readable. | That AWS resources, network paths, or Nginx are deployed or healthy. |
| `pending` | That evidence is required but has not been collected. | Any successful deployment or request. |

For live screenshots, retain enough context to identify the account/region and resource or endpoint, while redacting secrets and unrelated personal data. Add a short companion note describing what is visible, when it was captured, and what claim it supports.

## Current state

- Live AWS screenshots: **pending**
- Live endpoint response: **pending**
- Local documentation/PNG validation: may be recorded under `local/` after a local check
- Deployment claim: **none**
