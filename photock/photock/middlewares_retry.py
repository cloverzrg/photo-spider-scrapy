import random
from scrapy.downloadermiddlewares.retry import RetryMiddleware


class MyRetryMiddleware(RetryMiddleware):
    def __init__(self):
        pass
