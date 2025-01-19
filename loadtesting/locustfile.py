from locust import HttpUser, TaskSet, task, between
import random

class ApiUserBehavior(TaskSet):
    @task
    def test_api_endpoint(self):
        """
        Task to test an API endpoint.
        Replace 'your-endpoint-path' with your actual API endpoint path.
        """
        url = "/getRate"  # Replace with your API endpoint path
        payload = {
            "id": str(random.randint(1, 99)),  # Replace with actual data
        }
        headers = {
            "Content-Type": "application/json",
        }

        # Make the request
        response = self.client.post(url, json=payload, headers=headers)
        
        # Validate the response (Optional)
        if response.status_code != 200:
            print(f"Failed! Status code: {response.status_code}, Response: {response.text}")
        else:
            print(f"Success! Response: {response.json()}")

class ApiUser(HttpUser):
    tasks = [ApiUserBehavior]
    wait_time = between(0.5,1)  # Minimal wait time to achieve high TPS
