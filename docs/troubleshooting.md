# Troubleshooting report

This report records a reproducible **local pre-deployment configuration incident**. It is not a claim that the AWS stack was deployed. The intended path is shown in [`architecture.png`](architecture.png).

## Incident: SSH could not be guaranteed by the first template draft

| Required field | Record |
| --- | --- |
| Symptom | The first draft described SSH access but did not pass an EC2 key pair to the instance, and its deployment helper supplied a documentation-only `203.0.113.0/32` default. A live operator could create an instance that could not be reached by SSH. |
| Hypothesis | The instance definition lacked a `KeyName` property, while the default CIDR was not the operator's real public address. |
| Verification | Local inspection of `infra/template.yaml`, `scripts/deploy.sh`, and `tests/test_template.py` showed no `KeyName` parameter/property and a non-routable example CIDR. The structural test suite was extended to assert the key-pair reference and the deployment script was changed to require an explicit key name and CIDR. |
| Action | Added `KeyName` as an `AWS::EC2::KeyPair::KeyName` parameter, referenced it from `WebServer`, removed the unsafe default deployment path, and kept CIDR validation at `/16` through `/32`. |
| Result | The local template tests pass after the change. Live SSH connectivity remains **pending** because root credentials were not used and no stack was created. |
| Prevention | Require the key name and source CIDR as deployment inputs; review the SG and key-pair settings before deployment; capture the public IP and SSH test as live evidence before cleanup. |

## Live diagnostic order for an authorized run

Use the shortest boundary-first sequence and record each result:

## Before diagnosing

1. Record the exact timestamp, URL or public IP tested, and the observed status or error.
2. Confirm whether the observation came from a live AWS console/request or from a local file check.
3. Preserve the original screenshot or command output before changing anything.
4. Mark the result as **live**, **local**, or **pending** in the evidence notes.

### Symptom-to-check table

| Symptom | Likely boundary | Checks to perform in an authorized live environment |
| --- | --- | --- |
| No public address is available | EC2/subnet addressing | Confirm the instance is in the intended public subnet and has a public IPv4 address or reachable public endpoint. |
| Request times out | Route, IGW, SG, network ACL, or instance | Confirm the subnet route table has a default route to the IGW, the IGW is attached to the VPC, and the SG/NACL rules allow the intended HTTP path. |
| Connection is refused | EC2 or Nginx process | Confirm the instance is running, Nginx is installed and active, and a listener is bound to the expected port. |
| HTTP 403/404 is returned | Nginx configuration/content | Check the active server block, document root, file permissions, and the requested path. |
| HTTP 502/503 is returned | Nginx upstream configuration | Check whether the configuration expects an upstream application that is not running; a static Nginx page should not require one. |
| The console and screenshot disagree | Evidence capture | Recheck account/region, resource identifiers, timestamp, and whether the screenshot is live AWS evidence or a local rendering. |

1. **Address:** Is the endpoint actually public and is the request aimed at the correct address?
2. **Routing:** Does the public subnet have a default route to the IGW?
3. **Filtering:** Does the SG allow only the intended ingress, and is egress sufficient for the response path?
4. **Host:** Is the EC2 instance healthy and reachable through an authorized management path?
5. **Service:** Is Nginx active and listening on the expected port?
6. **Response:** Does the returned status and body match the expected Nginx content?

Do not broaden firewall access as a first response. Capture the current rule set, make the smallest authorized change, and re-test from the same client when possible.

## Evidence rule

A local PNG render, Markdown preview, or file inspection can prove only that the local documentation artifact is readable. It cannot prove that an AWS route, security group, EC2 instance, public endpoint, or Nginx service exists. Live AWS claims require timestamped, attributable screenshots or command output collected from the authorized environment.
