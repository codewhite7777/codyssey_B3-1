# Cleanup checklist

This checklist is prepared for a future authorized lab run. No cleanup actions have been executed by this documentation-only task.

Mark each item only after verifying the resource in the correct AWS account and region. If a resource was never created, record **not created** rather than implying deletion.

## AWS resources

- [ ] Confirm the deployment account and region.
- [ ] Record the resource IDs needed for cleanup and evidence retention.
- [ ] Terminate the EC2 instance, then verify its state and final termination.
- [ ] Release any standalone Elastic IP that is no longer needed.
- [ ] Remove unused security groups after dependent network interfaces are gone.
- [ ] Delete the public subnet if it was created for the lab.
- [ ] Detach and delete the Internet Gateway if it was created for the lab.
- [ ] Delete the lab route table and its routes after subnet dependencies are removed.
- [ ] Delete the lab VPC after all dependent resources are gone.
- [ ] Check for leftover EBS volumes, snapshots, load balancers, CloudWatch resources, and key pairs created only for the lab.
- [ ] Review the billing console or cost explorer for unexpected ongoing charges.

## Evidence and local files

- [ ] Preserve only the minimum live screenshots required by the submission or review.
- [ ] Remove secrets, tokens, private keys, and unrelated account details from evidence.
- [ ] Label each retained artifact as `live`, `local`, or `pending`.
- [ ] Keep the architecture diagram marked as a design reference, not live proof.
- [ ] Verify that no evidence file claims a deployment or successful request that was not observed.

## Final record

- Cleanup execution date: **pending**
- AWS account/region checked: **pending**
- Resources confirmed removed: **pending**
- Remaining cost-bearing resources: **pending**
- Reviewer or operator: **pending**
