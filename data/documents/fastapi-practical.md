# FastAPI in Practice

## Request validation with Pydantic

FastAPI uses Pydantic models to describe and validate request bodies. A request model makes required fields, types, and constraints visible in code and in generated OpenAPI documentation. Invalid data should produce a clear 422 response instead of reaching business logic in an unknown shape.

## Application lifespan

Load expensive shared resources such as a vector store or model connection during the FastAPI lifespan. Keeping initialization outside the request handler avoids rebuilding resources for every question and gives the service one predictable startup path. The application should fail loudly during startup if a required artifact is missing.

## Testing an API

An API test suite should cover a healthy request, invalid input, and an error from a dependency. Test the response contract as well as the status code, especially for structured answers and citations. A small TestClient suite catches regressions in routing, validation, and response serialization.
