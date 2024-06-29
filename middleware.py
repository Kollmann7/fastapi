from fastapi import  HTTPException, Request
from logger.main_logger import logger
from starlette import status


import time

async def log_middleware(request : Request, call_next):
    start = time.time()
    
    # if not authenticate_request(request):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    response = await call_next(request)

    proccess_time = time.time() - start

    log_dict = {
        "url": request.url,
        "method": request.method,
        "client_ip": request.client.host,
        "proccess_time": proccess_time,
        # "headers": dict(request.headers),
        # "body": await request.body(),
    }
    logger.info(log_dict, extra=log_dict)

    return response

def authenticate_request(request: Request) -> bool:
    # Replace with your authentication logic
    # For example, checking for a specific header or token
    auth_header = request.headers.get("Authorization")
    if auth_header == "Bearer your_token":
        return True
    return False

