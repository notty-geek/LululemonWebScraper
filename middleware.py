from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

from utils.logger import logger


async def logger_error_middleware(request: Request, call_next):
    try:
        logger.info(f"Request: {request.method} {request.url.path}")

        response = await call_next(request)

        logger.info(f"Response: {response.status_code}")

        return response

    except RequestValidationError as validation_error:
        logger.error(f"Validation error: {validation_error}")

        return JSONResponse(
            status_code=422,
            content={"message": "Validation error", "detail": validation_error.errors()},
        )

    except HTTPException as http_exception:
        logger.error(f"HTTP exception: {http_exception}")

        return JSONResponse(
            status_code=http_exception.status_code,
            content={"message": "HTTP exception", "detail": str(http_exception)},
        )

    except Exception as e:
        logger.exception(f"Exception: {e}")

        return JSONResponse(
            status_code=500,
            content={"message": "Server error", "detail": str(e)},
        )
