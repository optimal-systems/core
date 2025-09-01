# Optimal Core API

## Summary

The Optimal Core API repository serves as the backend service for Optimal Systems, providing a RESTful API for product management with authentication and authorization through Keycloak.

## Stack

* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
* [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
* [ruff](https://docs.astral.sh/ruff/) - Extremely fast Python linter and formatter
* [PostgreSQL](https://www.postgresql.org/) - Relational database
* [Keycloak](https://www.keycloak.org/) - Open source identity and access management
* [Uvicorn](https://www.uvicorn.org/) - ASGI server implementation

## Build

This repository uses a [uv](https://docs.astral.sh/uv/)-based build system for Python projects.

### Prerequisites

* [python 3.10+](https://www.python.org/downloads/)
* [uv](https://docs.astral.sh/uv/getting-started/installation.html)

### Installation and Setup

#### Install dependencies

```bash
cd core
uv sync
```

#### Run the application

```bash
cd core
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` by default.

## Deployment

### Infrastructure dependencies

- Python 3.10+
- PostgreSQL (latest version)
- Keycloak (for authentication and authorization)

### Environment variables

| Variable                | Description                                    | Example value                           |
|-------------------------|------------------------------------------------|-----------------------------------------|
| DEBUG                   | Enable debug mode                              | true                                    |
| KEYCLOAK_URL            | Keycloak server URL                            | http://localhost:8080                   |
| KEYCLOAK_REALM          | Keycloak realm name                            | master                                  |
| KEYCLOAK_CLIENT_ID      | Keycloak client ID                             | fastapi                                 |
| POSTGRES_HOST           | PostgreSQL host                                | localhost                               |
| POSTGRES_PORT           | PostgreSQL port                                | 5432                                    |
| POSTGRES_DB             | PostgreSQL database name                       | optimal                                 |
| POSTGRES_USER           | PostgreSQL username                            | optimal_backend                         |
| POSTGRES_PASSWORD       | PostgreSQL password                            | backend_supersecret                     |
| POSTGRES_MIN_CONN       | Minimum database connections                   | 1                                       |
| POSTGRES_MAX_CONN       | Maximum database connections                   | 10                                      |

### Project Structure

The project follows Clean Architecture principles with clear separation of concerns:

```
core/
├── api/                    # API layer (controllers, DTOs, error handling)
│   ├── controllers/        # FastAPI route handlers
│   ├── dtos/              # Data Transfer Objects
│   └── errors.py          # Global error handlers
├── application/           # Application layer (use cases)
│   ├── dtos/              # Application DTOs
│   └── use_cases/         # Business logic implementation
├── domain/                # Domain layer (entities, repositories)
│   ├── entities/          # Domain entities
│   └── repositories/      # Repository interfaces
├── infrastructure/        # Infrastructure layer (external services)
│   ├── auth/              # Authentication services
│   ├── database/          # Database configuration
│   └── repositories/      # Repository implementations
├── config/                # Configuration and logging
└── boot/                  # Application bootstrap
```

### API Features

The API provides the following functionality:

- **Product Search**: Search products by term with pagination
- **Product Listing**: List products with filtering and pagination
- **Authentication**: JWT-based authentication via Keycloak
- **Authorization**: Role-based access control
- **Health Check**: Basic health monitoring endpoint

### Authentication

The API uses Keycloak for authentication and authorization:

- OAuth2 Authorization Code flow
- JWT token validation
- Role-based access control (requires `optimal_reader` role by default)
- Automatic token validation on protected endpoints