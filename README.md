# Backend Application - Custom Auth System

## Description
The application implements an authentication and authorization system for an online store's backend API. Authentication is built on JWT tokens, which are generated and verified manually without using third-party libraries. Authorization is implemented through a role-based access model: each role has granular permissions for every object in the system, with a clear distinction between access to the user's own data only or access to all data.

## Stack: Django, Django REST Framework, PostgreSQL, PyJWT, bcrypt.

## How to Run
- Create a virtual environment and install dependencies:
   `python -m venv venv`
   `venv\Scripts\activate`
   `pip install django djangorestframework psycopg2-binary pyjwt bcrypt python-dotenv`
- Create a PostgreSQL database auth_project_db
- Create a .env file in the project root (next to manage.py) with the following variables:
   `SECRET_KEY=your-django-secret-key`
   `DB_NAME=auth_project_db`
   `DB_USER=postgres`
   `DB_PASSWORD=your-postgres-password`
   `DB_HOST=localhost`
   `DB_PORT=5432`
- You can generate a secret key with:
   `python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Apply migrations:
   `python manage.py migrate`
- Create a superuser to access the admin panel:
   `python manage.py createsuperuser`
- Start the server:
   `python manage.py runserver`

Test data (roles, business elements, access rules) is created manually through /admin/.

## Authentication
Password hashing — via the bcrypt library (hash_password/check_password functions in accounts/auth.py). Passwords are never stored in plain text.
JWT token — generated and verified manually using the PyJWT library (generate_token/decode_token functions in accounts/auth.py). The payload contains user_id and an expiration time (exp, 1 hour).
Identifying the user per request — a custom Middleware (accounts/middleware.py, JWTAuthMiddleware class). On every request, the middleware reads the Authorization: Bearer <token> header, verifies the token, looks up an active user, and attaches it to the request object. If there is no token, or the token is invalid, expired, or blacklisted — the user is treated as unauthenticated.
Logout — implemented via a token blacklist table (BlacklistedToken in accounts/models.py). On logout, the token is added to this table, and the middleware checks against it before treating any token as valid.
Soft delete — deleting an account (DELETE /api/accounts/profile/) does not remove the record from the database; it sets is_active=False. After that, the user can no longer log in (checked in LoginView) and cannot be authenticated with a previously issued token (the same is_active=True check in the middleware).
 
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/accounts/register/ | Registration (first name, last name, email, password, password confirmation) |
| POST | /api/accounts/login/ | Login with email and password, returns a JWT token |
| GET | /api/accounts/profile/ | Get own profile data (admin gets data for all users) |
| PUT | /api/accounts/profile/ | Update own profile data |
| DELETE | /api/accounts/profile/ | Soft delete own account |
| POST | /api/accounts/logout/ | Log out (token is added to the blacklist) |

## Authorization
The access rights system does not rely on Django's built-in groups/permissions — it is implemented through three custom tables:
- roles — user roles (admin, merchant, customer, guest)
- business_elements — application objects that access rules apply to (products, orders, reviews, access_rules)
- access_roles_rules — defines what a given role can do with a given element:
  - read_permission / read_all_permission
  - create_permission
  - update_permission / update_all_permission
  - delete_permission / delete_all_permission

### Pair logic: 
- read_permission=true, read_all_permission=false means the role can only see objects it owns. 
- read_all_permission=true grants access to all objects of that type, regardless of ownership. The same logic applies to update/delete. create_permission has no "own/all" distinction — it simply means "allowed to create."

### "Deny by Default" Principle
If there is no record for a (role, element) pair in access_roles_rules, access to that element for that role is fully denied.

### Permission Checking
All permission logic is centralized in the get_user_permission function (permissions/checker.py). It takes a user, a business element name, and an action (read/create/update/delete), and returns one of three results:
- none — no access
- own — access only to objects owned by the user
- all — access to all objects of that type

## Admin 
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/permissions/access-rules/ | List of all access rules |
| POST | /api/permissions/access-rules/ | Create a new rule |
| PUT | /api/permissions/access-rules/{id}/ | Update an existing rule |

## Mock Business Objects
The domain area is an online store. As required by the assignment, these are Views backed by in-memory data rather than database models.

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/business/products/ | List products |
| POST | /api/business/products/ | Create a product |
| GET | /api/business/orders/ | List orders |
| POST | /api/business/orders/ | Create an order |
| GET | /api/business/reviews/ | List reviews |
| POST | /api/business/reviews/ | Create a review |
| PUT | /api/business/reviews/{id}/ | Update a review (own only) |

## Limitations
A user can only have one role.
JWT token lifetime is 1 hour; the user must log in again after it expires.

## Response Codes
- 200 — success
- 201 — created
- 204 — deleted (soft delete)
- 400 — validation error
- 401 — unauthorized (no token / invalid token)
- 403 — forbidden (role lacks the required permission)
- 404 — not found
