import boto3
import random

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

# DynamoDB Table Name
table_name = 'HotelRates'

# Generate 100 vectors with 4 random numbers each
vectors = [
    {
        "id": {"S": str(i)},  # Unique number identifier for each vector
        "values": {"SS": [str(random.uniform(0.0,5000.0)) for _ in range(4)]}
    }
    for i in range(1, 100)
]


# Batch write to DynamoDB (25 items max per batch)
def batch_write(items):
    dynamodb.batch_write_item(
        RequestItems={
            table_name: [
                {"PutRequest": {"Item": item}} for item in items
            ]
        }
    )

# Chunk the data into groups of 25 (DynamoDB's batch write limit)
for i in range(0, len(vectors), 25):
    batch = vectors[i:i + 25]
    batch_write(batch)

print(f"Loaded {len(vectors)} vectors into {table_name}")