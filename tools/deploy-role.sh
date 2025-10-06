#!/usr/bin/env bash
set -euo pipefail

STACK_NAME=${STACK_NAME:-github-actions-deploy-role}
AWS_REGION=${AWS_REGION:-us-east-1}
GITHUB_ORG=${GITHUB_ORG:?Set GITHUB_ORG}
REPO_NAME=${REPO_NAME:?Set REPO_NAME}
BRANCH=${BRANCH:-main}
SECRETS_ARN=${SECRETS_ARN:?Set SECRETS_ARN}

TEMPLATE="infra/cfn/github-actions-deploy-role.yml"

aws cloudformation deploy \
  --stack-name "$STACK_NAME" \
  --template-file "$TEMPLATE" \
  --region "$AWS_REGION" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    GitHubOrg="$GITHUB_ORG" \
    RepoName="$REPO_NAME" \
    Branch="$BRANCH" \
    SecretsManagerArn="$SECRETS_ARN" \
    RoleName=github-actions-deploy-role

aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$AWS_REGION" \
  --query "Stacks[0].Outputs" --output table


