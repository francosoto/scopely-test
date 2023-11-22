from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger(logger_name="log_middleware")


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        logger.info(
            "Incoming HTTP request",
            custom_data={
                "req": {
                    "method": request.method,
                    "url": str(request.url),
                    "src_ip_addr": str(request.client.host),
                },
                "res": {
                    "status_code": response.status_code,
                },
            },
        )

        return response
