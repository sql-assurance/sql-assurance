from celery import Task


class SqlAssuranceTask(Task):
    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        pass

    def generate_file(self, data):
        pass

    def collect_data(self):
        pass