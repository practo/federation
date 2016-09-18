from locust import HttpLocust, TaskSet, task


class PeopleBehavior(TaskSet):
    def on_start(self):
        # on_start is called when a Locust start before any task is scheduled
        pass

    @task(1)
    def status(self):
        self.client.get("/api/health")


class HealthAgent(HttpLocust):
    task_set = StatusBehavior
    min_wait=5000
    max_wait=9000
