""" Importing dependencies """
import os
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv
from fastapi import FastAPI, status, Request  # Add Request import
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import httpx
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.schemas.profile import ProfileResponse, User

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="A Me Profile API",
    description="API displaying my details along with a random cat fact.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


#rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# Validate environment variables
EMAIL = os.getenv("EMAIL")
NAME = os.getenv("NAME")
STACK = os.getenv("STACK")
CAT_FACTS_API_URL = os.getenv("CAT_FACTS_API_URL", "https://catfact.ninja/fact")


if not all([EMAIL, NAME, STACK, CAT_FACTS_API_URL]):
    logger.error("Missing required environment variables")
    raise ValueError("EMAIL, NAME, STACK and CAT_FACTS_API_URL must be set in .env")


# GET /me endpoint with rate limiting
@app.get(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute") 
async def me(request: Request): 
    """Endpoint to get my details along with a random cat fact."""

    timeout = httpx.Timeout(5.0, connect=5.0)
    headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
    default_fact = "Cats have fast reflexes, did you know?"

    try:
        async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
            resp = await client.get(CAT_FACTS_API_URL)
            resp.raise_for_status()
            data = resp.json()
            fact = data.get("fact", default_fact)
            logger.info("Successfully fetched random cat fact: %s", fact)

            timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds") + "Z"

            return ProfileResponse(
                status="success",
                user=User(
                    email=EMAIL,
                    name=NAME,
                    stack=STACK
                ),
                timestamp=timestamp,
                fact=fact
            )

    except httpx.TimeoutException as e:
        logger.error("Timeout error: %s", e)
        fact = default_fact
        return JSONResponse(
            status_code=504,
            content={
                "status": "error",
                "message": "Cat Facts API request timed out",
                "fact": fact
            }
        )

    except httpx.RequestError as e:
        logger.error("Network error: %s", e)
        fact = default_fact
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "message": "Cat Facts API timed out",
                "fact": fact
            }
        )

    except httpx.HTTPStatusError as e:
        logger.error("HTTP error: %s", e)
        fact = default_fact
        return JSONResponse(
            status_code=e.response.status_code,
            content={
                "status": "error",
                "message": f"Cat Facts API returned {e.response.status_code}",
                "fact": fact
            }
        )

    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        fact = default_fact
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "An unexpected error occurred", "fact": fact}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
