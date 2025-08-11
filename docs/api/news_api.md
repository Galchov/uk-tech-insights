# News API

The **News API** provides programmatic access to both internal and external news articles related to the UK technology sector.  
It supports **public read-only endpoints** for general users and **management endpoints** for authorized administrators.

---

## Base URL

For local development:

http://localhost:8000/api/news/

For production (example):

https://techinsights.co.uk/api/news/


---

## Public Read-Only Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/news/articles/` | List all published news articles (internal + external). |
| GET | `/api/news/articles/<slug>/` | Retrieve a single article by slug. |
| GET | `/api/news/articles/?search=AI` | Search by keyword in title, summary, or content. |
| GET | `/api/news/articles/?category=Cybersecurity` | Filter by category name. |
| GET | `/api/news/articles/?type=internal` | List only internal articles. |
| GET | `/api/news/articles/?type=external` | List only external articles. |
| GET | `/api/news/articles/?ordering=-published_at` | Sort results (e.g., by date or title). |
| GET | `/api/news/articles/?page=2` | Paginate results (default 10 per page). |

---

## Internal Article Management (Admins Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/news/internal-articles/` | Create a new internal article. |
| GET | `/api/news/internal-articles/<slug>/` | Retrieve a single internal article by slug. |
| PUT | `/api/news/internal-articles/<slug>/` | Replace the entire internal article. |
| PATCH | `/api/news/internal-articles/<slug>/` | Partially update an internal article. |
| DELETE | `/api/news/internal-articles/<slug>/` | Delete an internal article. |

**Note:**  
These endpoints are protected and can only be accessed by **admins**.  
Moderators may have partial permissions depending on project configuration.

---

## Request & Response Format

All endpoints accept and return **JSON**.

### Request Example (POST)
```json
POST /api/news/internal-articles/
Content-Type: application/json

{
    "title": "Future of Quantum Processors in AI",
    "slug": "future-of-quantum-processors",
    "summary": "Quantum computing is poised to revolutionize AI by providing unprecedented processing ...",
    "content": "Researchers have been exploring how quantum processors can outperform classical architectures ...",
    "published_at": "2025-08-05T12:00:00Z",
    "category": "Technology",
    "image_url": "https://example.com/images/quantum-chip.jpg",
    "source_name": "TechRadar",
    "source_url": "https://www.techradar.com/articles/future-of-quantum-processors",
    "author": "Jane Doe"
}
```

Response Example (201 Created)

```json
{
    "id": 105,
    "title": "Future of Quantum Processors in AI",
    "slug": "future-of-quantum-processors",
    "summary": "Quantum computing is poised to revolutionize AI by providing unprecedented processing ...",
    "content": "Researchers have been exploring how quantum processors can outperform classical architectures ...",
    "published_at": "2025-08-05T12:00:00Z",
    "category": "Technology",
    "image_url": "https://example.com/images/quantum-chip.jpg",
    "source_name": "TechRadar",
    "source_url": "https://www.techradar.com/articles/future-of-quantum-processors",
    "author": "Jane Doe",
    "type": "internal"
}
```

## Filtering, Searching & Sorting

The News API supports query parameters for flexible results:

| **Parameter** | **Example** | **Description** |
|--------------|-------------|-----------------|
| `search`     | `?search=AI` | Keyword search in title, summary, or content. |
| `category`   | `?category=Cybersecurity` | Filter by category name. |
| `type`       | `?type=internal` | Filter by article type (`internal` or `external`). |
| `ordering`   | `?ordering=-published_at` | Sort results (e.g., by `title`, `published_at`). |
| `page`       | `?page=2` | Pagination (default: 10 per page). |

## Pagination

All list endpoints are paginated.

Default parameters:

- `page` – Current page number

- `page_size` – Items per page (default: 10)

Example:

```http
GET /api/news/articles/?page=2&page_size=20
```

Example Usage

```json
GET /api/news/articles/?search=quantum-computing
GET /api/news/internal-articles/future-of-quantum-processors/
POST /api/news/internal-articles/
{
    "title": "Future of Quantum Processors in AI",
    "slug": "future-of-quantum-processors",
    "summary": "Quantum computing is poised to revolutionize AI by providing unprecedented processing ...",
    "content": "Researchers have been exploring how quantum processors can outperform classical architectures ...",
    "published_at": "2025-08-05T12:00:00Z",
    "category": "Technology",
    "image_url": "https://example.com/images/quantum-chip.jpg",
    "source_name": "TechRadar",
    "source_url": "https://www.techradar.com/articles/future-of-quantum-processors",
    "author": "Jane Doe"
}
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

Example error:

```json
{
    "detail": "You do not have permission to perform this action."
}
```
