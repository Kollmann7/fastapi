from fastapi import HTTPException, Request
from logger.main_logger import logger
from starlette import status
from auth import verify_token  # Assuming you have a function to verify token
import time

# List of specific routes or prefixes that don't require authentication
EXEMPT_PREFIXES = ["/auth", "/docs", "/redoc", "/openapi.json"]

async def log_middleware(request: Request, call_next):
    start = time.time()

    # Check if the route is exempt from authentication
    if any(request.url.path.startswith(prefix) for prefix in EXEMPT_PREFIXES):
        response = await call_next(request)
        proccess_time = time.time() - start
        log_dict = {
            "url": request.url,
            "method": request.method,
            "client_ip": request.client.host,
            "proccess_time": proccess_time,
        }
        logger.info(log_dict, extra=log_dict)
        return response

    if not authenticate_request(request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    response = await call_next(request)
    proccess_time = time.time() - start

    log_dict = {
        "url": request.url,
        "method": request.method,
        "client_ip": request.client.host,
        "proccess_time": proccess_time,
        # "headers": dict(request.headers),
        "body": await request.body(),
    }
    logger.info(log_dict, extra=log_dict)

    return response

def authenticate_request(request: Request) -> bool:
    logger.info(f"Token: {token}")
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]
        logger.info(f"Token: {token}")
        try:
            payload = verify_token(token)
            request.state.user = payload 
            return True
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return False
    return False
