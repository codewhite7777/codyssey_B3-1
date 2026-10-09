#!/usr/bin/env bash
set -Eeuo pipefail

readonly AWS_REGION_FIXED='ap-northeast-2'

usage() {
  printf 'Usage: %s STACK_NAME --confirm\n' "$(basename "$0")" >&2
  printf 'The --confirm flag is required because this deletes the CloudFormation stack.\n' >&2
}

if [[ "$#" -ne 2 || "$2" != '--confirm' ]]; then
  usage
  exit 2
fi

stack_name="$1"
if [[ ! "$stack_name" =~ ^[A-Za-z][A-Za-z0-9-]{0,127}$ ]]; then
  printf 'Invalid stack name: %s\n' "$stack_name" >&2
  exit 2
fi
if ! command -v aws >/dev/null 2>&1; then
  printf 'AWS CLI is required but was not found.\n' >&2
  exit 1
fi

if ! aws cloudformation describe-stacks \
  --stack-name "$stack_name" \
  --region "$AWS_REGION_FIXED" \
  --output json >/dev/null 2>&1; then
  printf 'Stack %s was not found in %s; nothing was deleted.\n' "$stack_name" "$AWS_REGION_FIXED"
  exit 0
fi

printf 'Deleting stack %s in %s...\n' "$stack_name" "$AWS_REGION_FIXED"
aws cloudformation delete-stack \
  --stack-name "$stack_name" \
  --region "$AWS_REGION_FIXED"
aws cloudformation wait stack-delete-complete \
  --stack-name "$stack_name" \
  --region "$AWS_REGION_FIXED"
if aws cloudformation describe-stacks \
  --stack-name "$stack_name" \
  --region "$AWS_REGION_FIXED" \
  --output json >/dev/null 2>&1; then
  printf 'Stack %s still exists after deletion wait.\n' "$stack_name" >&2
  exit 1
fi
printf 'Stack %s deleted from %s.\n' "$stack_name" "$AWS_REGION_FIXED"
