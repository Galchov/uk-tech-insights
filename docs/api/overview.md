# API Overview

The **UK Tech Insights API** provides programmatic access to the platform’s core datasets, enabling developers, researchers, and other applications to query and integrate our curated information about the UK technology industry.  

Our API is designed to be:
- **Consistent** – All endpoints follow a common structure, naming convention, and response format.
- **RESTful** – Standard HTTP verbs (GET, POST, PUT, PATCH, DELETE) are used.
- **Extensible** – New endpoints can be added without breaking existing ones.
- **Human- and Machine-friendly** – Works seamlessly with browsers, tools like Postman, and integration scripts.

Currently, the API offers endpoints for:
- [**News API**](news_api.md) – Aggregates both internal articles and selected external sources.
- [**Companies API**](companies_api.md) – Information about technology companies operating in the UK.
- [**Job Market API**](job_market_api.md) – Live and historical IT job market data.

---

## Base URL

For local development:

http://localhost:8000/api/

For production (example):

https://techinsights.co.uk/api/

---

## Authentication

Some endpoints are **public** and can be accessed without authentication, while others require an authenticated user with the appropriate permissions.

- **Public Endpoints** – Read-only, no authentication needed (e.g., fetching public news articles).
- **Authenticated Endpoints** – Require a registered account and login session, or API token (if enabled).
- **Role-Based Access Control (RBAC)** – Certain write/update/delete actions are restricted to verified users, moderators, or admins.

Authentication methods:
- **Session-based** (default Django authentication)
- **Token-based** (if enabled via Django REST Framework)

See [Authentication & Permissions](#authentication--permissions) for more details.

---

## Request & Response Format

All endpoints support **JSON** request and response bodies.

**Request Example (POST):**
```json
{
      "name": "DeepWave Technologies",
      "slug": "deepwave-technologies",
      "logo": "http://127.0.0.1:8000/media/company_logo/deepwave-logo.png",
      "description": "DeepWave Technologies is a UK-based AI research and development company ...",
      "website": "https://www.deepwave.ai",
      "foundation_date": "2018-09-15",
      "formatted_foundation_date": "September 2018",
      "location": "London, United Kingdom",
      "address": "14 King Street, London, EC2V 8BB",
      "operating_countries": [
          "United Kingdom",
          "Germany",
          "Singapore"
      ],
      "industries": [
          "Artificial Intelligence",
          "Healthcare",
          "Autonomous Systems"
      ],
      "tech_stack": [
          "Python",
          "TensorFlow",
          "Docker",
          "Kubernetes"
      ]
  }
```

**Response Example (201 Created):**
```json
{
    "name": "DeepWave Technologies",
    "slug": "deepwave-technologies",
    "logo": "http://127.0.0.1:8000/media/company_logo/deepwave-logo.png",
    "description": "DeepWave Technologies is a UK-based AI research and development company ...",
    "website": "https://www.deepwave.ai",
    "foundation_date": "2018-09-15",
    "formatted_foundation_date": "September 2018",
    "location": "London, United Kingdom",
    "address": "14 King Street, London, EC2V 8BB",
    "operating_countries": [
        "United Kingdom",
        "Germany",
        "Singapore"
    ],
    "industries": [
        "Artificial Intelligence",
        "Healthcare",
        "Autonomous Systems"
    ],
    "tech_stack": [
        "Python",
        "TensorFlow",
        "Docker",
        "Kubernetes"
    ]
}
```

## Pagination

All list endpoints are paginated by default.

Default parameters:

- `page` – Current page number

- `page_size` – Items per page (default: 10)

Example:

```http
GET /api/news/articles/?page=2&page_size=20
```

## Filtering & Searching

The API supports query parameters for searching and filtering results.

Examples:

```http
GET /api/news/articles/?search=cybersecurity
GET /api/companies/?industry=Artificial%20Intelligence
GET /api/jobs/?location=London&language=Python
```

## Error Handling

Error responses follow standard HTTP status codes:

| **Status Code** | **Meaning** |
|-----------------|-------------|
| `200 OK`        | Successful request. |
| `201 Created`   | Resource created successfully. |
| `204 No Content`| Successful deletion. |
| `400 Bad Request` | Validation or formatting error. |
| `401 Unauthorized` | Authentication required. |
| `403 Forbidden` | Insufficient permissions. |
| `404 Not Found` | Resource not found. |
| `500 Internal Server Error` | Unexpected server issue. |

Example error response:

```json
{
  "detail": "You do not have permission to perform this action."
}
```
