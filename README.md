# A Me Profile API with Cat Facts

A RESTful API endpoint that returns profile information along with dynamic cat facts. Built with FastAPI and Python.

## Features

- GET `/me` endpoint returning profile details and random cat facts
- Dynamic UTC timestamp in ISO 8601 format
- Integration with Cat Facts API
- Error handling with fallback responses
- CORS enabled
- Basic logging
- Environment variable configuration
- Rate Limiting: Limits requests to 5 per minute per client IP using slowapi.

## Prerequisites

- Python 3.8 or higher
- uv: Install the `uv` tool for dependency management.
- A `.env` file with required environment variables

## Installation

1. Clone the repository:
```bash
git clone https://github.com/edenis00/Stage-Zero
cd Stage-One
```

2. Install dependencies using UV:
```bash
uv sync
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

or using pip
create a virtual environment
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirments.txt
```

3. Create a `.env` file in the project root:
```env
EMAIL=john.doe@example.com
NAME=John Doe
STACK=Python/FastAPI
CAT_FACTS_API_URL=https://catfact.ninja/fact
```

## Running the Application

Start the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- Main endpoint: http://localhost:8000/me
- API documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Response Format

```json
{
  "status": "success",
  "user": {
    "email": "your.email@example.com",
    "name": "Your Full Name",
    "stack": "Python/FastAPI"
  },
  "timestamp": "2023-09-15T14:30:00.000Z",
  "fact": "Random cat fact from external API"
}
```

## Error Handling

The API implements graceful error handling for:
- Timeout errors (504)
- Network errors (503)
- External API failures (502)
- Unexpected errors (500)

## Development

- Uses FastAPI for high performance
- Async HTTP client (httpx) for external API calls
- Environment variables for configuration
- Basic logging for debugging
- CORS middleware enabled

## Testing

Test the /me endpoint using one of the following methods:
1. Using `curl`:
```bash
curl http://localhost:8000/me
```
To test rate limiting, send multiple requests in quick succession:
```bash
for i in {1..6}; do curl http://localhost:8000/me; done
```

2. ### Using Postman:

- Create a GET request to `http://localhost:8000/me`.
- Send multiple requests to verify success and rate limit responses.
