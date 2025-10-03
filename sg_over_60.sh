aws ec2 describe-security-groups --output json | jq '
.SecurityGroups[] |
{
  GroupId,
  GroupName,
  IngressCount: (
    ( [.IpPermissions[].IpRanges[]] | length ) +
    ( [.IpPermissions[].Ipv6Ranges[]] | length ) +
    ( [.IpPermissions[].PrefixListIds[]] | length ) +
    ( [.IpPermissions[].UserIdGroupPairs[]] | length )
  )
} | select(.IngressCount >= 60)'

# Describe security groups with 60 or more ingress rules
