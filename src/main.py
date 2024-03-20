from prometheus_client import make_asgi_app, Counter, Histogram
from fastapi import FastAPI
from requests import get  # type: ignore
from json import loads
from time import time, sleep
from random import uniform, randint

import responses

app = FastAPI()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

is_mocking = False

REQUEST_COUNT = Counter(
    "app_request_count",
    "Application request count",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Application Request Latency",
    ["method", "endpoint"],
)


@app.get("/")
def root():
    return {"Message": "Hello World!"}


@app.get("/bored")
def bored():
    # Simulate some errors
    start_time = time()

    response = get("https://www.boredapi.com/api/activity")

    status_code = response.status_code
    text = response.text

    if randint(0, 3) == 2:
        status_code = 500
        text = "{\"Oops, You got the simulated error!\": \"Sorry\"}"

    print(text)
    # random delay
    sleep(uniform(0, 2))

    # Prom stuff
    REQUEST_COUNT.labels("GET", "/bored", status_code).inc()
    REQUEST_LATENCY.labels("GET", "/bored").observe(time() - start_time)

    return loads(text)


@app.get("/mock")
def mock():
    global is_mocking

    is_mocking = not is_mocking

    print(f"{is_mocking = }")

    while is_mocking:
        sleep(uniform(0, 0.2))
        bored()
