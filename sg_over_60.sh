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
