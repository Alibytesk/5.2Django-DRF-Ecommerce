# 5.2Django-DRF-Ecommerce

Project: Django E-commerce — API + Web (Decoupled Architecture with JWT)
This is an open-source e-commerce system built with Django, structured into two fully separated projects:

API Backend – built using Django REST Framework (DRF), responsible for all business logic and data handling.

Web Frontend – built using traditional Django templates (not React or SPA), acting as the user-facing website, communicating with the API via HTTP requests.

Key Features
Separation of Concerns: Web and API are decoupled into two independent Django projects. This architecture improves modularity and prepares the system for future frontends like mobile apps or React.

JWT Authentication:

User login/registration handled via API.

Access/Refresh tokens stored and used by the web frontend to authenticate users.

Secure Password Handling:

Passwords are hashed using Django's built-in set_password() method during registration.

API authenticates users and returns tokens using SimpleJWT.

Django Template Frontend:

Fully server-rendered UI using Django's template engine.

No frontend framework like React; all interaction happens via form submissions and backend rendering.

API-Driven Web:

The Web project does not access the database directly.

Instead, it consumes the API via HTTP (using requests library) and renders the received data to templates.

Project Structure
/ecommerce_api/    → Django project with DRF endpoints (JWT, users, products, cart, etc.)
/ecommerce_web/    → Django project rendering templates & interacting with the API

Authentication Flow
Web frontend sends login credentials to the API.

API validates credentials, returns JWT tokens.

Web stores tokens in Django session (or cookie).

For any protected API call (e.g., get user orders), Web adds Authorization: Bearer <token> in headers.

Goals
Show how to cleanly separate frontend and backend in Django without needing JS frameworks.

Provide a secure, extendable base for e-commerce systems or similar apps.

Help developers understand and use JWT in server-rendered environments (not just SPAs).

