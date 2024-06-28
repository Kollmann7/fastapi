from fastapi import  Request
from logger.main_logger import logger
import time

async def log_middleware(request : Request, call_next):
    start = time.time()
    
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