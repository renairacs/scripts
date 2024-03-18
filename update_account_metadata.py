import boto3


def get_primary_key_name(table_name):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.describe_table(TableName=table_name)
    return response['Table']['KeySchema'][0]['AttributeName']


def validate_primary_value(allowed_by, current_primary):
    if 'kite' in allowed_by:
        return 'pillow'
    elif 'Transition' in allowed_by and 'renaira_account' in allowed_by:
        return 'renaira_account'
    elif 'IT-Area' in allowed_by:
        return 'IT-Area'
    else:
        return list(allowed_by)[-1]


def update_primary_attribute(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    primary_key_name = get_primary_key_name(table_name)

    response = table.scan()
    items = response['Items']

    for item in items:
        allowed_by = item.get('allowed_by', set())
        current_primary = item.get('primary', None)

        validated_primary = validate_primary_value(allowed_by, current_primary)

        if 'primary' not in item or item['primary'] != validated_primary:
            update_expression = "SET #primary = :primary_value"
            expression_attribute_names = {"#primary": "primary"}
            expression_attribute_values = {":primary_value": validated_primary}

            key = {primary_key_name: item[primary_key_name]}

            table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values
            )


print("done")

if __name__ == "__main__":
    update_primary_attribute('database_name') #change this guy
