import json
import boto3
import time
# Initialize Kinesis client
client = boto3.client('kinesis', region_name="ap-southeast-2")
stream_name = "viewership-stream"
# CSV Header (Must match order in the CSV file)
columns = [
    "session_id", "user_id", "channel_id", "channel_name", "show_name", "genre", "timestamp",
    "duration_minutes", "region", "subscription_type", "device", "platform", "is_live",
    "ads_watched", "ad_revenue", "engagement_score", "buffer_count", "completion_percentage"
]
# Read and process CSV file
with open("viewership_logs.csv") as f:
    lines = f.readlines()[1:]  # Skip header
    for line in lines:
        # Convert line into dictionary
        values = line.strip().split(',')
        record = dict(zip(columns, values))
        # Print what is being streamed
        print("📤 Streaming Record →", json.dumps(record, indent=2))
        # Send to Kinesis
        response = client.put_record(
            StreamName=stream_name,
            Data=json.dumps(record),
            PartitionKey=record["user_id"]
        )
        # Optional: Print Kinesis response (Record ID)
        print("✅ Sent to Kinesis. SequenceNumber:", response['SequenceNumber'])
        # Simulate real-time
        time.sleep(0.01)

