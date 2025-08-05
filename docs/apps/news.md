# News Application

The News App is responsible for managing technology-related articles on the UK Tech Insights platform. It serves both original content authored internally and external content aggregated from trusted third-party APIs.

---

## Purpose

The goal of the News App is to:

- Provide timely and relevant news coverage about the tech industry
- Bridge global tech developments with their impact on the UK
- Offer a unified experience for browsing internally and externally sourced articles

---

## Article Types

There are two distinct types of articles:

| Type              | Source               | Editable via Admin | Linked to Author | API Availability |
|-------------------|----------------------|---------------------|------------------|------------------|
| InternalArticle   | Created by platform users or moderators | ✅ Yes           | ✅ Yes           | ✅ Yes           |
| ExternalArticle   | Fetched via external API (e.g., NewsAPI) | ❌ No            | ❌ No            | ✅ Yes           |

Both types inherit from a shared abstract model: `BaseArticle`.

---

## Features

- Create, edit, and manage internal news content
- Import external news from third-party APIs
- Display a unified list of all articles with filters and pagination
- Publish/unpublish internal articles via moderation
- Access articles through a public REST API

---

## External News Import

The platform includes a management command to **import articles from external news providers**, currently supporting:

- [NewsAPI.org](https://newsapi.org)

This functionality allows moderators and admins to populate the platform with fresh, relevant news without manual entry.

---

### Environment Configuration

To use the external import functionality, your `.env` file must include the api key, which you can get free from newsapi.org

```sql
NEWS_API_KEY=your_newsapi_key_here
```

---

## Usage: Import External Articles

Default settings:

**File:** `apps/news/management/commands/import_external_articles.py`
```python
def add_arguments(self, parser):
        parser.add_argument('--provider', type=str, default='newsapi')
        parser.add_argument('--query', type=str, default='tech')
        parser.add_argument('--language', type=str, default='en')
        parser.add_argument('--page_size', type=str, default=20)
```

You can run the following command to import articles directly into the system:

```bash
python manage.py import_external_articles
```

Example with custom choice:

```bash
python manage.py import_external_articles --provider=newsapi --query=security --language=en --page_size=5
```

The order and the number of the arguments is not stricly enforced. The ones you do not specify will follow the default settings. 