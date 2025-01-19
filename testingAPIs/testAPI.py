import time
import requests

# Replace with the URL of the API you want to test
API_URL = "endpoint/getRate"
API_HEALTH_CHECK ="endpoint/ping" 

# Initialize an empty list to store latencies
latencies = []

# Number of times to call the API
NUM_CALLS = 1000
index = 0

print(f"Starting API latency test with {NUM_CALLS} calls...")

healthCheck = requests.get(API_HEALTH_CHECK)
for i in range(NUM_CALLS):
    try:
        index = index + 1
        if(index==100):
            index = 1
        # Make the API request
        response = requests.post(API_URL, json={"id":str(index)})
        healthCheck = requests.get(API_HEALTH_CHECK)
        # print the response
        # print(response.text)
        # Store the latency
        latencies.append(response.elapsed.total_seconds()*1000)
        # Check the response status
        if response.status_code == 200:
            print(f"Call {i + 1}: Success - Latency: {response.elapsed.total_seconds()*1000:.2f} ms")
        else:
            print(f"Call {i + 1}: Failed - Status Code: {response.status_code}")

    except Exception as e:
        print(f"Call {i + 1}: Exception occurred - {e}")

# Calculate the average, minimum, and maximum latency
if latencies:
    average_latency = sum(latencies) / len(latencies)
    min_latency = min(latencies)
    max_latency = max(latencies)
    print(f"\nAverage Latency: {average_latency:.2f} ms")
    print(f"Minimum Latency: {min_latency:.2f} ms")
    print(f"Maximum Latency: {max_latency:.2f} ms")
    print(f"Health Check Latency: {healthCheck.elapsed.total_seconds()*1000:.2f} ms")
else:
    print("\nNo successful API calls to calculate latency statistics.")
