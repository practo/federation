from locust import HttpLocust, TaskSet, task


class StatusBehavior(TaskSet):
    def on_start(self):
        # on_start is called when a Locust start before any task is scheduled
        pass

    @task(1)
    def status(self):
        self.client.get('/status')


class PeopleBehavior(TaskSet):
    def on_start(self):
        pass

    @task(1)
    def index(self):
        self.client.get('/people')

    @task(2)
    def show(self):
        self.client.get('/people/1')


class HealthAgent(HttpLocust):
    task_set = StatusBehavior
    min_wait = 5000
    max_wait = 9000


class PeopleAgent(HttpLocust):
    task_set = PeopleBehavior
    min_wait = 5000
    max_wait = 9000
