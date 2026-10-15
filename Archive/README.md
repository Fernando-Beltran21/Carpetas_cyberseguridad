# Nuclei + Docker Web Application Pentest Lab

This lab runs OWASP Juice Shop as an intentionally vulnerable training target and scans it with ProjectDiscovery Nuclei.

## Requirements
- Docker Engine or Docker Desktop
- Docker Compose v2
- Internet access to pull container images and Nuclei templates

## Start the target
```bash
mkdir -p reports
docker compose up -d juice-shop
```

Open http://localhost:3000 to verify Juice Shop is running.

## Run Nuclei
```bash
docker compose --profile scan run --rm nuclei
```

Results are written to `reports/nuclei-results.jsonl`.

## Inspect results
```bash
ls -lh reports/
jq . reports/nuclei-results.jsonl
```
The `jq` command is optional; install jq if it is not available.

## Scan a different authorized target
Edit `compose.yaml` and replace `http://juice-shop:3000` with the target's address reachable from the Nuclei container. For a service running on the host on Docker Desktop, `http://host.docker.internal:3000` may work.

## Stop the lab
```bash
docker compose down
```

## Safety
Only scan systems you own or have explicit permission to test. Juice Shop is deliberately vulnerable; keep it isolated and do not expose it to public networks. Nuclei templates and active checks can generate requests that affect targets, so review scan scope before using them outside this lab.
