# System Architecture

UK Tech Insights follows a modular architecture using Django, separating each functional domain into standalone applications. This promotes reusability, scalability, and clean domain boundaries.

## Key Architectural Concepts

### Modular Django Apps
Each app encapsulates its models, views, forms, templates, serializers, permissions, and URLs:
- `news` – for internal and external articles
- `companies` – for storing and presenting company profiles
- `job_market` – for job listings and market statistics
- `learning` – for educational content and tracking
- `forum` – for user discussion and community interaction
- `accounts` – for authentication, registration, and role-based access
- `api_docs` – for internal documentation of API endpoints

### Database
- **PostgreSQL** is used as the primary relational database.
- Generic relationships and many-to-many relations are used extensively to model complex associations (e.g., companies and industries, articles and authors).
- Django’s ORM handles schema migrations and query abstraction.

### API Layer
- Django REST Framework (DRF) provides versioned, paginated, and browsable APIs.
- APIs are available for public read access, while write permissions are restricted to authenticated and authorized users.
- Certain apps (e.g., News) support external data integration from third-party APIs.

### Frontend
- HTML templates styled with **Bootstrap**

### Permissions
- Users are assigned to groups:
  - Regular Users
  - Verified Users
  - Moderators
  - Administrators
- Group permissions determine access to CRUD operations across models and API endpoints.

For setup instructions, refer to [Setup Guide](setup.md).
