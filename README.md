# Codyssey B3-1: AWS public web service

This repository defines the minimum Seoul-region AWS path required by the mission:

`External user → Internet Gateway → Public Subnet → Security Group → EC2 → Nginx`

## Implementation

- `infra/template.yaml`: CloudFormation stack for one VPC, public subnet, IGW, route table, restricted SG, and one EC2/Nginx server.
- `iam/cloudformation-deployer-policy.json`: least-privilege starting policy for the dedicated deployment IAM identity. It does not grant `AdministratorAccess`, S3, or RDS permissions.
- `scripts/deploy.sh`: validates inputs and deploys only to `ap-northeast-2`.
- `scripts/integration_test.py`: read-only stack/resource check plus external `GET /health` check.
- `scripts/cleanup.sh`: explicit-confirmation stack deletion and completion wait.
- `scripts/generate_architecture.py`: reproducibly generates the architecture PNG.
- `tests/test_template.py`: local structural and security checks.

The EC2 key pair must already exist in Seoul. Pass its name and the learner's public `/32` (or an intentionally narrow CIDR) to the deployment script. Never commit the private key.

```sh
python3 -m pip install -r requirements-test.txt
pytest -q
bash -n scripts/deploy.sh scripts/cleanup.sh
./scripts/deploy.sh codyssey-web <key-name> <your-public-ip>/32
python3 scripts/integration_test.py codyssey-web
./scripts/cleanup.sh codyssey-web --confirm
```

## Evidence status

| Artifact | Status |
| --- | --- |
| `docs/architecture.png` | Local design artifact available |
| Local unit/static tests | 4 passed during implementation; rerun after checkout changes |
| Live external `/health` response | Pending; no live deployment claimed |
| Live AWS screenshots | Pending |
| Cleanup confirmation | Pending until an authorized non-root deployment exists |

AWS credentials inspected for this task identify the root user. The mission explicitly forbids root access, so no AWS stack was created or deleted. Use a dedicated IAM user or role with the policy in `iam/cloudformation-deployer-policy.json`, then capture live evidence under `docs/evidence/live/`.

## Submission documents

- [Architecture](docs/architecture.png)
- [Troubleshooting report](docs/troubleshooting.md)
- [Cleanup checklist](docs/cleanup-checklist.md)
- [Evidence rules](docs/evidence/README.md)

The diagram and documents distinguish local artifacts from live AWS proof; they do not claim an external request succeeded until a timestamped live capture is added.
