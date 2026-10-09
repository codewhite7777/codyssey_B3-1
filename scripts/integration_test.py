#!/usr/bin/env python3
"""Read-only smoke test for a deployed codyssey CloudFormation stack."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any


REGION = "ap-northeast-2"
EXPECTED_RESOURCE_TYPES = {
    "AWS::EC2::VPC",
    "AWS::EC2::Subnet",
    "AWS::EC2::InternetGateway",
    "AWS::EC2::RouteTable",
    "AWS::EC2::Route",
    "AWS::EC2::SecurityGroup",
    "AWS::EC2::Instance",
}


def aws_json(*arguments: str) -> dict[str, Any] | list[Any]:
    command = ["aws", *arguments, "--region", REGION, "--output", "json"]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as error:
        raise RuntimeError("AWS CLI is required") from error
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or "AWS CLI request failed"
        raise RuntimeError(detail) from error
    return json.loads(result.stdout)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stack_name", help="CloudFormation stack to inspect")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        stack_response = aws_json("cloudformation", "describe-stacks", "--stack-name", args.stack_name)
        resource_response = aws_json(
            "cloudformation", "describe-stack-resources", "--stack-name", args.stack_name
        )
        stack = stack_response["Stacks"][0]
        resources = resource_response["StackResources"]
        outputs = {item["OutputKey"]: item["OutputValue"] for item in stack.get("Outputs", [])}
    except (RuntimeError, KeyError, IndexError, json.JSONDecodeError) as error:
        print(f"FAIL: could not inspect stack: {error}", file=sys.stderr)
        return 1

    status = stack.get("StackStatus", "")
    if status not in {"CREATE_COMPLETE", "UPDATE_COMPLETE"}:
        print(f"FAIL: stack status is {status or 'missing'}", file=sys.stderr)
        return 1

    resource_types = {resource["ResourceType"] for resource in resources}
    missing_types = EXPECTED_RESOURCE_TYPES - resource_types
    if missing_types:
        print(f"FAIL: missing resource types: {', '.join(sorted(missing_types))}", file=sys.stderr)
        return 1

    health_url = outputs.get("HealthUrl")
    public_ip = outputs.get("WebPublicIp")
    if not health_url or not public_ip:
        print("FAIL: WebPublicIp and HealthUrl outputs are required", file=sys.stderr)
        return 1

    try:
        with urllib.request.urlopen(health_url, timeout=10) as response:
            body = response.read().decode("utf-8").strip()
            if response.status != 200 or body != "OK":
                print(f"FAIL: {health_url} returned HTTP {response.status}: {body!r}", file=sys.stderr)
                return 1
    except (urllib.error.URLError, TimeoutError, UnicodeDecodeError) as error:
        print(f"FAIL: health check at {health_url} failed: {error}", file=sys.stderr)
        return 1

    print(f"PASS: {args.stack_name} is healthy at {health_url} ({public_ip})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
