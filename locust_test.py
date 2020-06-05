from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    def on_start(self):
        self.client.get("/")


    @task
    def about(self):
        self.client.get("/v1/api/shop/")


class WebsiteUser(HttpLocust):
    host = 'http://47.89.23.172:8020'
    task_set = WebsiteTasks
    min_wait = 10
    max_wait = 10
    stop_timeout = 1



