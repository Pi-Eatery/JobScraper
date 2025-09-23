# Performance tests will be added here using Locust
# Example:
# from locust import HttpUser, task, between

# class UserBehavior(HttpUser):
#     wait_time = between(1, 2)

#     @task
#     def login(self):
#         self.client.post("/api/auth/login", json={"username": "testuser", "password": "testpassword"})

#     @task
#     def get_applications(self):
#         self.client.get("/api/applications", headers={"Authorization": "Bearer YOUR_TOKEN"})