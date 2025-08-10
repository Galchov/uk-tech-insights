# Contributing to UK Tech Insights

Thank you for your interest in contributing to **UK Tech Insights**!  
We welcome contributions from developers, designers, and content creators who share our goal of building a comprehensive, data-driven platform about the UK technology industry.

This document explains our collaboration process, coding conventions, and how to submit changes effectively.

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Project Structure](#project-structure)
- [Branching & Workflow](#branching--workflow)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Coding Standards](#coding-standards)
- [Adding Features](#adding-features)
- [Reporting Issues](#reporting-issues)
- [Submitting Pull Requests](#submitting-pull-requests)
- [Style & UI Consistency](#style--ui-consistency)
- [License](#license)

---

## Code of Conduct
All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a respectful and productive environment.

---

## Project Structure

Key directories:

- apps/ -> All Django apps (news, companies, job_market, learning, etc.)
- common/ -> Shared templates, utilities, and components
- news/ -> News domain (internal & external articles)
- companies/ -> Companies domain and industry management
- job_market/ -> IT job market data and postings
- learning/ -> Tutorials, courses, articles
- config/ -> Django project configuration
- docs/ -> Documentation
- static/ -> Global static assets
- templates/ -> Global templates

---

## Branching & Workflow

We use a **feature-branch workflow**:

- **`main`** — stable, production-ready code
- **`develop`** — integration branch for ongoing development
- **Feature branches** — new features, prefixed with `feature/`
- **Bugfix branches** — fixes for bugs, prefixed with `fix/`
- **Hotfix branches** — urgent fixes to production, prefixed with `hotfix/`

Example:
```bash
git checkout develop
git checkout -b feature/add-job-filtering
```

## Commit Message Guidelines

Follow the Conventional Commits format:

```terminal
<type>(<scope>): <short description>
```

Types include:

- feat — new feature

- fix — bug fix

- docs — documentation only changes

- style — formatting, missing semi-colons, etc.

- refactor — code change without fixing a bug or adding a feature

- test — adding or updating tests

- chore — maintenance tasks

Example:

```terminal
feat(news): add external API integration for news articles
fix(companies): resolve missing industry filter bug
```

## Coding Standards

- Python: PEP 8, with black and isort for formatting

- Django: follow project’s app structure and DRY principles

- JavaScript: use ES6+ syntax

- CSS/Bootstrap: follow existing Bootstrap conventions and breakpoints

- Use descriptive variable names and docstrings for complex logic

- Keep functions and views small and single-purpose

## Adding Features

- When adding a new feature:

- Create a new branch from develop

- Write unit tests for new functionality

- Update relevant docs in /docs or in code docstrings

- Run tests and linters before pushing

## Reporting Issues

### If you find a bug:

- Search existing issues first

- Include steps to reproduce, expected behavior, and screenshots if relevant

- If security-related, please contact the maintainers privately

## Submitting Pull Requests

- Fork the repository and create your branch

- Push changes to your fork

- Submit a pull request to the develop branch

- Ensure all checks pass (tests, linting, CI/CD)

## Style & UI Consistency

- Forms: use Bootstrap btn, btn-primary, btn-outline-secondary, btn-danger

- Containers: max-width of 700px where applicable

- Keep templates consistent with other domain apps (News, Companies, Job Market)

- Use the common app for shared components (navbar, footer, buttons)
