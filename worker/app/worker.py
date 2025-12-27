import os
import logging
import redis
from rq import Worker, Queue, Connection

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
listen = ['ingestion']
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    conn = redis.from_url(redis_url)
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
