from fastapi import APIRouter
import time
from logger.main_logger import logger
from starlette import status

orders_router = APIRouter()

@orders_router.get("/", status_code=status.HTTP_200_OK)
async def get_orders():
    start_time = time.time()
    logger.critical('The database is dead !')
    return {"message": "Hello", "duration": time.time() - start_time}
