#!/usr/bin/env bash
set -Eeuo pipefail

readonly AWS_REGION_FIXED='ap-northeast-2'
readonly SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
readonly TEMPLATE_PATH="${SCRIPT_DIR}/../infra/template.yaml"

usage() {
  printf 'Usage: %s [stack-name] KEY_NAME SSH_CIDR\n' "$(basename "$0")" >&2
  printf 'Example: %s codyssey-web codyssey-key 203.0.113.10/32\n' "$(basename "$0")" >&2
}

if [[ "$#" -ne 3 ]]; then
  usage
  exit 2
fi

stack_name="${1:-codyssey-web}"
key_name="$2"
ssh_cidr="$3"

python3 - "$stack_name" "$ssh_cidr" <<'PY'
import ipaddress
import re
import sys

stack_name, ssh_cidr = sys.argv[1:]
if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]{0,127}", stack_name):
    raise SystemExit("stack name must start with a letter and contain only letters, digits, and hyphens")
try:
    network = ipaddress.ip_network(ssh_cidr, strict=False)
except ValueError as error:
    raise SystemExit(f"ssh CIDR is invalid: {error}")
if network.version != 4 or network.prefixlen < 16:
    raise SystemExit("ssh CIDR must be IPv4 with a /16 through /32 prefix")
PY

if [[ ! -s "$TEMPLATE_PATH" ]]; then
  printf 'CloudFormation template not found: %s\n' "$TEMPLATE_PATH" >&2
  exit 1
fi
if ! command -v aws >/dev/null 2>&1; then
  printf 'AWS CLI is required but was not found.\n' >&2
  exit 1
fi

printf 'Validating %s in %s...\n' "$TEMPLATE_PATH" "$AWS_REGION_FIXED"
aws cloudformation validate-template \
  --template-body "file://${TEMPLATE_PATH}" \
  --region "$AWS_REGION_FIXED" \
  --output json >/dev/null

printf 'Deploying stack %s in %s...\n' "$stack_name" "$AWS_REGION_FIXED"
aws cloudformation deploy \
  --template-file "$TEMPLATE_PATH" \
  --stack-name "$stack_name" \
  --region "$AWS_REGION_FIXED" \
  --parameter-overrides "SSHIngressCidr=${ssh_cidr}" "KeyName=${key_name}" \
  --no-fail-on-empty-changeset \
  --tags Project=codyssey

printf 'Deployment command completed for stack %s.\n' "$stack_name"
