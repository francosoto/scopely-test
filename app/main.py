import uvicorn

from app import config
from app.endpoints import app

if __name__ == "__main__":
    timeout_ka = config.MAX_CONCURRENT_REQUESTS * config.MAX_REQUEST_DURATION
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,
        timeout_keep_alive=timeout_ka,
        limit_concurrency=config.MAX_CONCURRENT_REQUESTS,
    )
