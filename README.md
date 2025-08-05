# UK Tech Insights

UK Tech Insights is a comprehensive platform that analyzes and presents data about the technology sector with a specific focus on the United Kingdom. The project covers the latest trends, companies, jobs, news, learning resources, and forums—targeted toward developers, researchers, and policymakers interested in the impact of technology on the UK and beyond.

The platform is developed using Django and Django Rest Framework, and it is modular by design, supporting public APIs, asynchronous operations, user role management, and detailed domain-specific insights.

---

## Table of Contents

- [Overview](#overview)
- [Apps and Modules](#apps-and-modules)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
  - [Database Setup](#database-setup)
  - [Running the Project](#running-the-project)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

UK Tech Insights aims to bridge the gap between raw tech data and meaningful insight within the context of the UK. Whether you're a developer, analyst, researcher, or decision-maker, the platform provides the tools and knowledge to:

- Track the latest technology trends
- Explore tech companies based in or operating within the UK
- Monitor job market movements and postings
- Learn from structured educational content
- Engage in forum-based community discussions
- Access data through public APIs for further analysis or integration

---

## Apps and Modules

The platform is organized into modular Django apps:

| App              | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **News**         | Aggregates internal and external articles focused on the tech world         |
| **Companies**    | Showcases the tech companies                                                |
| **Job Market**   | Lists tech jobs and visualizes employment trends                            |
| **Learning**     | Offers tutorials, guides, and other learning materials                      |
| **Forum**        | Community-driven discussions on tech topics                                 |
| **API**          | RESTful endpoints for all public data models                                |

More details can be found in the [full documentation](docs/index.md).

---

## Technology Stack

This project uses the following core technologies:

- Python 3.12+
- Django 5.2
- Django Rest Framework
- PostgreSQL
- Bootstrap (frontend styling)
- Poetry (for dependency management)

Dependencies from `pyproject.toml` include:

```toml
dependencies = [
    "psycopg2 (>=2.9.10,<3.0.0)",
    "python-decouple (>=3.8,<4.0)",
    "django (>=5.2.3,<6.0.0)",
    "pillow (>=11.2.1,<12.0.0)",
    "django-countries (>=7.6.1,<8.0.0)",
    "django-widget-tweaks (>=1.5.0,<2.0.0)",
    "djangorestframework (>=3.16.0,<4.0.0)",
    "requests (>=2.32.4,<3.0.0)"
]
```
