#!/usr/bin/env python3
"""
Generates the conecta_nexus_sprint_1_tasks.csv file with all 28 granular tasks
for Sprint 1 (auth & profile) following the team's official specifications.
"""
import os
import csv

TASKS = [
    # ==========================================
    # AUTH (FastAPI) - 15 TASKS
    # ==========================================
    {
        "task_id": "AUTH-TASK-01",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-01",
        "parent_issue_number": "2",
        "title": "[AUTH-TASK-01] Database Engine & Connection Configuration",
        "assignee": "NelsonConde",
        "labels": "task,sprint-1",
        "objective": "Configure the async SQLAlchemy engine, session factory, connection pool, and pydantic-settings configuration for the db_auth database on PostgreSQL 16.",
        "specs": (
            "- Database: PostgreSQL 16 (db_auth)\n"
            "- Engine: SQLAlchemy async engine (create_async_engine) with asyncpg driver\n"
            "- Pool: pool_size=10, max_overflow=20, pool_pre_ping=True\n"
            "- Configuration: pydantic-settings BaseSettings loading DATABASE_URL, DB_ECHO, APP_ENV\n"
            "- Target Files: src/core/config.py, src/core/database.py"
        ),
        "deliverables": (
            "- [ ] Implement BaseSettings in src/core/config.py\n"
            "- [ ] Create async SQLAlchemy engine and async_sessionmaker in src/core/database.py\n"
            "- [ ] Provide get_db dependency yielding async sessions\n"
            "- [ ] Unit test verifying engine instantiation and session generation"
        ),
        "verification": "uv run python -c 'from src.core.database import async_engine; print(async_engine)'"
    },
    {
        "task_id": "AUTH-TASK-02",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-01",
        "parent_issue_number": "2",
        "title": "[AUTH-TASK-02] User Database Model & Alembic Migration",
        "assignee": "NelsonConde",
        "labels": "task,sprint-1",
        "objective": "Implement the core users SQLAlchemy model representing user accounts and credentials in db_auth, and generate the initial Alembic migration.",
        "specs": (
            "- Table: users in db_auth\n"
            "- Columns:\n"
            "  * id: UUID (Primary Key, default gen_random_uuid())\n"
            "  * email: VARCHAR(255) (UNIQUE NOT NULL, indexed)\n"
            "  * password_hash: VARCHAR(255) (NOT NULL)\n"
            "  * role: VARCHAR(20) (NOT NULL, CHECK role IN ('STUDENT', 'COMPANY', 'ADMIN'))\n"
            "  * is_active: BOOLEAN (NOT NULL, DEFAULT TRUE)\n"
            "  * is_email_verified: BOOLEAN (NOT NULL, DEFAULT FALSE)\n"
            "  * last_login_at: TIMESTAMPTZ (NULL)\n"
            "  * created_at: TIMESTAMPTZ (NOT NULL, DEFAULT CURRENT_TIMESTAMP)\n"
            "  * updated_at: TIMESTAMPTZ (NOT NULL, DEFAULT CURRENT_TIMESTAMP)\n"
            "- Target Files: src/models/user.py, alembic/versions/001_create_users_table.py"
        ),
        "deliverables": (
            "- [ ] Declarative Base model for User with all column types and CHECK constraints\n"
            "- [ ] Alembic environment configured to read SQLAlchemy models\n"
            "- [ ] Initial migration generated and applied cleanly against local PostgreSQL\n"
            "- [ ] Model tests verifying constraints and defaults"
        ),
        "verification": "uv run alembic upgrade head"
    },
    {
        "task_id": "AUTH-TASK-03",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-01",
        "parent_issue_number": "2",
        "title": "[AUTH-TASK-03] Password Hashing & Domain Security Service",
        "assignee": "NelsonConde",
        "labels": "task,sprint-1",
        "objective": "Implement the password hashing and verification service using Argon2 or bcrypt, and validate institutional and corporate email domains.",
        "specs": (
            "- Algorithm: Argon2id or bcrypt via passlib / pwd_context\n"
            "- Validation Rules:\n"
            "  * Minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 number, 1 symbol\n"
            "  * Students must register with institutional domain @ufps.edu.co\n"
            "  * Companies must register with verified corporate domain (blacklist free webmails: gmail, hotmail, yahoo)\n"
            "- Target Files: src/core/security.py, src/services/validation_service.py"
        ),
        "deliverables": (
            "- [ ] hash_password(plain_password: str) -> str\n"
            "- [ ] verify_password(plain_password: str, hashed_password: str) -> bool\n"
            "- [ ] validate_email_domain(email: str, role: str) -> bool\n"
            "- [ ] Unit tests covering password hashing, verification, and domain validation edge cases"
        ),
        "verification": "uv run pytest tests/test_security.py"
    },
    {
        "task_id": "AUTH-TASK-04",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-01",
        "parent_issue_number": "2",
        "title": "[AUTH-TASK-04] User Registration Pydantic Schemas & Repository",
        "assignee": "NelsonConde",
        "labels": "task,sprint-1",
        "objective": "Create Pydantic v2 validation schemas for user registration and implement the UserRepository for database operations.",
        "specs": (
            "- Schemas:\n"
            "  * UserCreate: email, password, role ('STUDENT' or 'COMPANY')\n"
            "  * UserResponse: id, email, role, is_active, is_email_verified, created_at (excludes password_hash)\n"
            "- Repository Methods in UserRepository:\n"
            "  * get_by_email(db, email: str) -> User | None\n"
            "  * get_by_id(db, user_id: UUID) -> User | None\n"
            "  * create(db, user_in: UserCreate, hashed_password: str) -> User\n"
            "- Target Files: src/schemas/user.py, src/repositories/user_repository.py"
        ),
        "deliverables": (
            "- [ ] Pydantic UserCreate schema with strict type and email validation\n"
            "- [ ] Pydantic UserResponse schema with model_config = ConfigDict(from_attributes=True)\n"
            "- [ ] UserRepository class with async SQLAlchemy queries\n"
            "- [ ] Unit tests for schema validation and repository CRUD operations"
        ),
        "verification": "uv run pytest tests/test_user_repository.py"
    },
    {
        "task_id": "AUTH-TASK-05",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-01",
        "parent_issue_number": "2",
        "title": "[AUTH-TASK-05] User Registration Router & Endpoint",
        "assignee": "NelsonConde",
        "labels": "task,sprint-1",
        "objective": "Implement the public user registration endpoint with role restrictions and duplicate email handling.",
        "specs": (
            "- Endpoint: POST /api/v1/auth/register\n"
            "- Request Body: UserCreate\n"
            "- Response: HTTP 201 Created with UserResponse\n"
            "- Business Rules:\n"
            "  * Reject role ADMIN on public registration with HTTP 403 / 422\n"
            "  * Check duplicate email and return HTTP 409 Conflict with clear error message\n"
            "  * Persist new account with hashed password and is_active = True\n"
            "- Target Files: src/routers/auth.py, src/services/auth_service.py"
        ),
        "deliverables": (
            "- [ ] POST /api/v1/auth/register endpoint integrated into APIRouter\n"
            "- [ ] Duplicate email conflict handling returning HTTP 409\n"
            "- [ ] ADMIN creation prohibition logic\n"
            "- [ ] Integration tests covering successful registration, duplicate email, and ADMIN blocking"
        ),
        "verification": "uv run pytest tests/test_register.py"
    },
    {
        "task_id": "AUTH-TASK-06",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-01",
        "parent_issue_number": "2",
        "title": "[AUTH-TASK-06] User Account Status Endpoint (ADMIN)",
        "assignee": "NelsonConde",
        "labels": "task,sprint-1",
        "objective": "Expose administrative endpoint to activate or suspend user accounts, secured with RBAC scope checks.",
        "specs": (
            "- Endpoint: PATCH /api/v1/auth/users/{user_id}/status\n"
            "- Request Body: UserStatusUpdate (is_active: bool, reason: str | None)\n"
            "- Security: Restricted to role ADMIN and OAuth2 scope user:status:write (RF03, RF32)\n"
            "- Response: HTTP 200 OK with updated UserResponse\n"
            "- Target Files: src/routers/users.py, src/services/user_service.py"
        ),
        "deliverables": (
            "- [ ] PATCH /api/v1/auth/users/{user_id}/status route implementation\n"
            "- [ ] RBAC scope dependency verifying user:status:write\n"
            "- [ ] Account status toggling in db_auth\n"
            "- [ ] Unit tests testing authorized admin status change and unauthorized 403 rejections"
        ),
        "verification": "uv run pytest tests/test_user_status.py"
    },
    {
        "task_id": "AUTH-TASK-07",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-02",
        "parent_issue_number": "1",
        "title": "[AUTH-TASK-07] RSA Key Pair Management & Cryptographic Setup (ADR-002)",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Implement asymmetric cryptography management for RS256 token signing (ADR-002) using RSA 2048-bit key pairs.",
        "specs": (
            "- ADR-002: RS256 asymmetric cryptographic signing\n"
            "- Keys:\n"
            "  * jwt_private.pem: 2048-bit RSA private key (exclusive to auth service)\n"
            "  * jwt_public.pem: RSA public key (shared with Gateway and profile)\n"
            "- Loading: Support loading from file path, environment variable, or volume mount\n"
            "- Security: .pem files must be excluded from Git via .gitignore\n"
            "- Target Files: src/core/crypto.py, scripts/generate_keys.py"
        ),
        "deliverables": (
            "- [ ] Key loading utility reading PEM formatted RSA keys\n"
            "- [ ] Script to generate local development RSA key pair\n"
            "- [ ] Fallback error handling if private key is missing\n"
            "- [ ] Unit tests verifying RSA key loading and sign/verify roundtrip"
        ),
        "verification": "uv run python -c 'from src.core.crypto import load_rsa_keys; priv, pub = load_rsa_keys(); print(\"Keys loaded\")'"
    },
    {
        "task_id": "AUTH-TASK-08",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-02",
        "parent_issue_number": "1",
        "title": "[AUTH-TASK-08] Refresh Token & Password Reset Models & Migrations",
        "assignee": "NelsonConde",
        "labels": "task,sprint-1",
        "objective": "Create database models and migrations for session management (refresh_tokens) and password reset tokens in db_auth.",
        "specs": (
            "- Tables in db_auth:\n"
            "  1. refresh_tokens:\n"
            "     * id: UUID (Primary Key, maps to claim jti)\n"
            "     * user_id: UUID (NOT NULL, FK users.id ON DELETE CASCADE)\n"
            "     * token_hash: VARCHAR(255) (UNIQUE NOT NULL, SHA-256)\n"
            "     * expires_at: TIMESTAMPTZ (NOT NULL)\n"
            "     * is_revoked: BOOLEAN (NOT NULL, DEFAULT FALSE)\n"
            "     * revoked_at: TIMESTAMPTZ (NULL)\n"
            "     * ip_address: INET (NULL)\n"
            "     * user_agent: VARCHAR(512) (NULL)\n"
            "     * created_at: TIMESTAMPTZ (NOT NULL, DEFAULT CURRENT_TIMESTAMP)\n"
            "  2. password_reset_tokens:\n"
            "     * id: UUID (PK), user_id: UUID (FK), token_hash: VARCHAR(255) (UNIQUE NOT NULL)\n"
            "     * expires_at: TIMESTAMPTZ (NOT NULL), is_used: BOOLEAN (DEFAULT FALSE)\n"
            "     * created_at: TIMESTAMPTZ (NOT NULL, DEFAULT CURRENT_TIMESTAMP)\n"
            "- Target Files: src/models/token.py, alembic/versions/002_create_token_tables.py"
        ),
        "deliverables": (
            "- [ ] SQLAlchemy models for RefreshToken and PasswordResetToken\n"
            "- [ ] Foreign keys with cascading delete linked to users.id\n"
            "- [ ] Alembic migration generated and applied cleanly\n"
            "- [ ] Model tests for token revocation and expiration fields"
        ),
        "verification": "uv run alembic upgrade head"
    },
    {
        "task_id": "AUTH-TASK-09",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-02",
        "parent_issue_number": "1",
        "title": "[AUTH-TASK-09] JWT Token Service & OAuth2 Claims Builder (RS256)",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Implement the core JWT encoding/decoding service with RS256 signing, claims builder, and role-based scope injection.",
        "specs": (
            "- Algorithm: RS256 with 2048-bit RSA private key\n"
            "- Lifespan: Access Token = 15 minutes, Refresh Token = 7 days\n"
            "- Payload Claims:\n"
            "  * iss: https://auth.conectanexus.ufps.edu.co\n"
            "  * aud: ['conecta-nexus-gateway', 'conecta-nexus-services']\n"
            "  * sub: str(user.id)\n"
            "  * jti: str(token_id)\n"
            "  * role: user.role\n"
            "  * scope: Scopes mapped from Section 4.1 RBAC matrix\n"
            "- Target Files: src/services/jwt_service.py, src/core/security.py"
        ),
        "deliverables": (
            "- [ ] create_access_token(user: User, jti: UUID) -> str\n"
            "- [ ] create_refresh_token(user: User, jti: UUID) -> str\n"
            "- [ ] decode_token(token: str) -> dict\n"
            "- [ ] Scope mapping function for STUDENT, COMPANY, ADMIN\n"
            "- [ ] Unit tests for token encoding, decoding, expiration, and scope verification"
        ),
        "verification": "uv run pytest tests/test_jwt_service.py"
    },
    {
        "task_id": "AUTH-TASK-10",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-02",
        "parent_issue_number": "1",
        "title": "[AUTH-TASK-10] OAuth2 Login & Refresh Token Persistence Endpoint",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Implement OAuth2 password login endpoint, issuing RS256 JWT access and refresh tokens, and recording session metadata.",
        "specs": (
            "- Endpoint: POST /api/v1/auth/login\n"
            "- Input: OAuth2PasswordRequestForm or LoginRequest (email, password)\n"
            "- Response: HTTP 200 OK with TokenResponse (access_token, refresh_token, token_type: bearer, expires_in: 900)\n"
            "- Business Rules:\n"
            "  * Verify user exists and verify_password matches\n"
            "  * Verify is_active == True (return HTTP 403 if inactive)\n"
            "  * Update last_login_at\n"
            "  * Hash refresh token (SHA-256) and persist in refresh_tokens table with client IP and User-Agent\n"
            "  * Target response time < 50 ms\n"
            "- Target Files: src/routers/auth.py, src/services/auth_service.py"
        ),
        "deliverables": (
            "- [ ] POST /api/v1/auth/login route implementation\n"
            "- [ ] Credential authentication and active state check\n"
            "- [ ] Refresh token hash persistence in db_auth\n"
            "- [ ] Integration tests covering valid login, invalid password, and inactive user"
        ),
        "verification": "uv run pytest tests/test_login.py"
    },
    {
        "task_id": "AUTH-TASK-11",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-02",
        "parent_issue_number": "1",
        "title": "[AUTH-TASK-11] Token Refresh & Rotation Endpoint",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Implement refresh token rotation endpoint to renew access tokens while invalidating used refresh tokens.",
        "specs": (
            "- Endpoint: POST /api/v1/auth/refresh\n"
            "- Input: TokenRefreshRequest (refresh_token: str)\n"
            "- Response: HTTP 200 OK with new TokenResponse (access_token, refresh_token)\n"
            "- Business Rules:\n"
            "  * Decode refresh token and find by token_hash in db_auth\n"
            "  * Check that token is not expired and is_revoked == False\n"
            "  * Strict Rotation: Mark old token is_revoked = True, revoked_at = CURRENT_TIMESTAMP\n"
            "  * Issue and store new refresh token and new access token\n"
            "- Target Files: src/routers/auth.py, src/services/auth_service.py"
        ),
        "deliverables": (
            "- [ ] POST /api/v1/auth/refresh route\n"
            "- [ ] Refresh token validation and revocation logic\n"
            "- [ ] Issue new rotated token pair\n"
            "- [ ] Integration tests for valid refresh, re-use of revoked token, and expired token"
        ),
        "verification": "uv run pytest tests/test_token_refresh.py"
    },
    {
        "task_id": "AUTH-TASK-12",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-02",
        "parent_issue_number": "1",
        "title": "[AUTH-TASK-12] Session Revocation & Logout Endpoint",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Implement explicit logout endpoint revoking active sessions and invalidating refresh tokens.",
        "specs": (
            "- Endpoint: POST /api/v1/auth/logout\n"
            "- Input: LogoutRequest (refresh_token: str) or Authorization header\n"
            "- Response: HTTP 200 OK with LogoutResponse (message: 'Successfully logged out')\n"
            "- Business Rules:\n"
            "  * Extract session jti from token\n"
            "  * Set is_revoked = True and revoked_at = CURRENT_TIMESTAMP in refresh_tokens\n"
            "  * Subsequent attempts to use revoked token must return HTTP 401\n"
            "- Target Files: src/routers/auth.py, src/services/auth_service.py"
        ),
        "deliverables": (
            "- [ ] POST /api/v1/auth/logout route\n"
            "- [ ] Session revocation in db_auth\n"
            "- [ ] Invalidation check integration\n"
            "- [ ] Integration tests for logout and attempted reuse"
        ),
        "verification": "uv run pytest tests/test_logout.py"
    },
    {
        "task_id": "AUTH-TASK-13",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-02",
        "parent_issue_number": "1",
        "title": "[AUTH-TASK-13] High-Performance Session Verification Endpoint (/verify)",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Implement ultra-fast session verification endpoint for API Gateway and downstream microservices with < 50ms latency.",
        "specs": (
            "- Endpoint: GET /api/v1/auth/verify\n"
            "- Header: Authorization: Bearer <access_token>\n"
            "- Response: HTTP 200 OK with VerifyResponse (valid: bool, user_id: str, email: str, role: str, scopes: list[str])\n"
            "- SLA: Response time strictly < 50 ms\n"
            "- Business Rules:\n"
            "  * Validate RS256 signature with public key\n"
            "  * Verify iss, aud, and exp\n"
            "  * Return HTTP 401 Unauthorized if invalid or expired\n"
            "- Target Files: src/routers/auth.py, src/services/jwt_service.py"
        ),
        "deliverables": (
            "- [ ] GET /api/v1/auth/verify route\n"
            "- [ ] Fast stateless JWT validation path\n"
            "- [ ] Standard error responses for Gateway routing\n"
            "- [ ] Benchmark/test ensuring sub-50ms execution"
        ),
        "verification": "uv run pytest tests/test_verify.py"
    },
    {
        "task_id": "AUTH-TASK-14",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-02",
        "parent_issue_number": "1",
        "title": "[AUTH-TASK-14] Password Reset Flow Endpoints",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Implement password recovery flow: request temporary token and confirm password update with session invalidation.",
        "specs": (
            "- Endpoints:\n"
            "  1. POST /api/v1/auth/password-reset/request (email: str) -> generates 15-min single-use token\n"
            "  2. POST /api/v1/auth/password-reset/confirm (token: str, new_password: str) -> updates password\n"
            "- Business Rules:\n"
            "  * Single use token: mark is_used = True upon consumption\n"
            "  * Update password_hash with new password\n"
            "  * Invalidate/revoke all active refresh tokens for the user\n"
            "- Target Files: src/routers/password_reset.py, src/services/password_reset_service.py"
        ),
        "deliverables": (
            "- [ ] POST /api/v1/auth/password-reset/request route\n"
            "- [ ] POST /api/v1/auth/password-reset/confirm route\n"
            "- [ ] Token single-use validation and password updating\n"
            "- [ ] Integration tests covering full password reset cycle"
        ),
        "verification": "uv run pytest tests/test_password_reset.py"
    },
    {
        "task_id": "AUTH-TASK-15",
        "repo": "auth",
        "service": "auth",
        "parent_story": "HU-01, HU-02",
        "parent_issue_number": "2",
        "title": "[AUTH-TASK-15] Unit & Integration Test Suite for Auth",
        "assignee": "NelsonConde",
        "labels": "task,sprint-1",
        "objective": "Implement full Pytest test suite with async fixtures covering all authentication, registration, token, and revocation paths.",
        "specs": (
            "- Framework: pytest, pytest-asyncio, httpx AsyncClient\n"
            "- Target Coverage: >= 80% line coverage\n"
            "- Test Scenarios:\n"
            "  * Registration: valid student/company, duplicate email, blocked admin\n"
            "  * Login: correct credentials, wrong password, inactive user\n"
            "  * Token: expiration, refresh rotation, re-use detection, logout revocation\n"
            "  * Verification: /verify valid and invalid tokens\n"
            "- Target Files: tests/conftest.py, tests/test_*.py"
        ),
        "deliverables": (
            "- [ ] Test database fixtures and helper client\n"
            "- [ ] Comprehensive test cases for all auth routes\n"
            "- [ ] Coverage report verification confirming >= 80%\n"
            "- [ ] GitHub Actions CI workflow check compatibility"
        ),
        "verification": "uv run pytest --cov=src --cov-report=term-missing"
    },

    # ==========================================
    # PROFILE (Django DRF) - 13 TASKS
    # ==========================================
    {
        "task_id": "PROFILE-TASK-01",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-03",
        "parent_issue_number": "1",
        "title": "[PROFILE-TASK-01] Database Connection & DRF Core Settings",
        "assignee": "juandiegosb",
        "labels": "task,sprint-1",
        "objective": "Configure PostgreSQL 16 database connection for db_profiles, modular app structure, and Django REST Framework global settings.",
        "specs": (
            "- Database: PostgreSQL 16 (db_profiles)\n"
            "- Modular Apps: apps.consents, apps.students, apps.companies, apps.core\n"
            "- DRF Settings: DEFAULT_RENDERER_CLASSES, DEFAULT_PARSER_CLASSES, custom exception handler\n"
            "- Target Files: config/settings.py, config/urls.py, apps/core/exceptions.py"
        ),
        "deliverables": (
            "- [ ] Configure DATABASES setting pointing to db_profiles\n"
            "- [ ] Register apps in INSTALLED_APPS\n"
            "- [ ] Custom API exception handler returning standard JSON errors\n"
            "- [ ] Verify setup with manage.py check"
        ),
        "verification": "uv run python manage.py check"
    },
    {
        "task_id": "PROFILE-TASK-02",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-03",
        "parent_issue_number": "1",
        "title": "[PROFILE-TASK-02] Stateless RS256 JWT Authentication & Scopes RBAC",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Implement stateless RS256 JWT authentication in DRF using jwt_public.pem and custom permission classes for OAuth2 scopes.",
        "specs": (
            "- ADR-002: Stateless token validation using RSA public key (no DB queries to db_auth)\n"
            "- Classes to Implement:\n"
            "  * RS256JWTAuthentication: decodes Bearer token, validates iss, aud, exp with jwt_public.pem\n"
            "  * StatelessJWTUser: in-memory user object (id=sub, email, role, scopes: list[str])\n"
            "  * HasScope('...') & Role permissions (IsStudent, IsCompany, IsAdmin)\n"
            "- Target Files: apps/core/authentication.py, apps/core/permissions.py"
        ),
        "deliverables": (
            "- [ ] RS256JWTAuthentication class\n"
            "- [ ] StatelessJWTUser class\n"
            "- [ ] Custom scope-based DRF permission classes\n"
            "- [ ] Unit tests testing valid token decode, expired token, and scope enforcement"
        ),
        "verification": "uv run pytest apps/core/tests/test_authentication.py"
    },
    {
        "task_id": "PROFILE-TASK-03",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-03",
        "parent_issue_number": "1",
        "title": "[PROFILE-TASK-03] Data Consent Model & Database Migrations",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Implement the DataConsent Django model representing legal consent under Colombian Law 1581 of 2012, and generate migrations.",
        "specs": (
            "- Table: data_consents in db_profiles\n"
            "- Fields:\n"
            "  * id: UUIDField (primary_key=True, default=uuid.uuid4)\n"
            "  * user_id: UUIDField (db_index=True, logical ref to auth users.id)\n"
            "  * policy_version: CharField(max_length=20, default='v1.0-2026')\n"
            "  * is_accepted: BooleanField (CHECK is_accepted = TRUE)\n"
            "  * ip_address: GenericIPAddressField()\n"
            "  * user_agent: TextField()\n"
            "  * accepted_at: DateTimeField(auto_now_add=True, immutable UTC)\n"
            "- Target Files: apps/consents/models.py, apps/consents/migrations/0001_initial.py"
        ),
        "deliverables": (
            "- [ ] DataConsent Django model with CheckConstraint on is_accepted\n"
            "- [ ] Initial migration created and applied\n"
            "- [ ] Admin registration for consent inspection\n"
            "- [ ] Model tests verifying immutability of accepted_at and user_id index"
        ),
        "verification": "uv run python manage.py migrate"
    },
    {
        "task_id": "PROFILE-TASK-04",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-03",
        "parent_issue_number": "1",
        "title": "[PROFILE-TASK-04] Consent Serializer & Blocking Permission Validator",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Create DRF serializers for consent submission and a reusable permission class that blocks profile operations if consent is missing.",
        "specs": (
            "- Serializers:\n"
            "  * DataConsentCreateSerializer (policy_version, is_accepted)\n"
            "  * DataConsentStatusSerializer (is_accepted, policy_version, accepted_at)\n"
            "- Permission Class:\n"
            "  * HasAcceptedConsent: checks if user_id exists in DataConsent table. If not, raises PermissionDenied (HTTP 403, code: 'CONSENT_REQUIRED')\n"
            "- Target Files: apps/consents/serializers.py, apps/consents/permissions.py"
        ),
        "deliverables": (
            "- [ ] DataConsentCreateSerializer with validation\n"
            "- [ ] DataConsentStatusSerializer\n"
            "- [ ] HasAcceptedConsent DRF permission class\n"
            "- [ ] Unit tests testing consent verification and blocking"
        ),
        "verification": "uv run pytest apps/consents/tests/test_permissions.py"
    },
    {
        "task_id": "PROFILE-TASK-05",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-03",
        "parent_issue_number": "1",
        "title": "[PROFILE-TASK-05] Consent Registration & Status Endpoints",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Expose endpoints for users to record electronic consent and query their consent status for the Nuxt 4 legal modal.",
        "specs": (
            "- Endpoints:\n"
            "  1. POST /api/v1/profiles/consent:\n"
            "     * Captures IP from request.META (REMOTE_ADDR / HTTP_X_FORWARDED_FOR)\n"
            "     * Captures User-Agent from request.META['HTTP_USER_AGENT']\n"
            "     * Creates DataConsent record and returns HTTP 201 Created\n"
            "  2. GET /api/v1/profiles/consent/me:\n"
            "     * Returns consent status for the authenticated user\n"
            "- Target Files: apps/consents/views.py, apps/consents/urls.py"
        ),
        "deliverables": (
            "- [ ] POST /api/v1/profiles/consent view\n"
            "- [ ] GET /api/v1/profiles/consent/me view\n"
            "- [ ] URL routing configuration\n"
            "- [ ] Integration tests verifying IP/User-Agent extraction and consent querying"
        ),
        "verification": "uv run pytest apps/consents/tests/test_views.py"
    },
    {
        "task_id": "PROFILE-TASK-06",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-04",
        "parent_issue_number": "2",
        "title": "[PROFILE-TASK-06] Student Profile Model & PostgreSQL Constraints",
        "assignee": "juandiegosb",
        "labels": "task,sprint-1",
        "objective": "Implement the StudentProfile model with semester check constraints (6 to 10) and JSONB fields for skills/courses.",
        "specs": (
            "- Table: student_profiles in db_profiles\n"
            "- Fields:\n"
            "  * id: UUIDField (PK)\n"
            "  * user_id: UUIDField (UNIQUE NOT NULL)\n"
            "  * full_name: CharField(max_length=150)\n"
            "  * student_code: CharField(max_length=15, unique=True) (Immutable RB-08)\n"
            "  * academic_program: CharField(max_length=120, default='Ingeniería de Sistemas')\n"
            "  * current_semester: PositiveSmallIntegerField (CHECK current_semester BETWEEN 6 AND 10)\n"
            "  * completed_courses: JSONField(default=list)\n"
            "  * technical_skills: JSONField(default=list)\n"
            "  * interest_areas: JSONField(default=list)\n"
            "  * bio: TextField(null=True, blank=True)\n"
            "  * contact_email: EmailField()\n"
            "  * contact_phone: CharField(max_length=25, null=True, blank=True)\n"
            "  * is_profile_complete: BooleanField(default=False)\n"
            "  * created_at, updated_at: DateTimeField\n"
            "- Target Files: apps/students/models.py, apps/students/migrations/0001_initial.py"
        ),
        "deliverables": (
            "- [ ] StudentProfile Django model with CheckConstraint on current_semester\n"
            "- [ ] Unique constraints on user_id and student_code\n"
            "- [ ] Django migration generated and applied\n"
            "- [ ] Model tests verifying semester constraint and default values"
        ),
        "verification": "uv run python manage.py migrate"
    },
    {
        "task_id": "PROFILE-TASK-07",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-04",
        "parent_issue_number": "2",
        "title": "[PROFILE-TASK-07] Student Profile Serializers & Immutability Logic",
        "assignee": "juandiegosb",
        "labels": "task,sprint-1",
        "objective": "Create DRF serializers enforcing student code immutability (RB-08 / RF10) and contact masking (RF08).",
        "specs": (
            "- Business Rules:\n"
            "  * RB-08 / RF10: student_code and academic_program are strictly immutable after creation. Reject changes with ValidationError (HTTP 400)\n"
            "  * RF06: current_semester must be between 6 and 10\n"
            "  * RF08: StudentProfilePublicSerializer must omit contact_email and contact_phone\n"
            "- Serializers:\n"
            "  * StudentProfileCreateSerializer\n"
            "  * StudentProfileUpdateSerializer\n"
            "  * StudentProfilePrivateSerializer (owner view)\n"
            "  * StudentProfilePublicSerializer (restricted public view)\n"
            "- Target Files: apps/students/serializers.py"
        ),
        "deliverables": (
            "- [ ] Serializers with validation for current_semester\n"
            "- [ ] Immutability validator blocking changes to student_code\n"
            "- [ ] Public serializer omitting direct contact details\n"
            "- [ ] Serializer unit tests covering boundary values and immutability rejection"
        ),
        "verification": "uv run pytest apps/students/tests/test_serializers.py"
    },
    {
        "task_id": "PROFILE-TASK-08",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-04",
        "parent_issue_number": "2",
        "title": "[PROFILE-TASK-08] Student Profile CRUD & Public Restricted Endpoints",
        "assignee": "juandiegosb",
        "labels": "task,sprint-1",
        "objective": "Expose endpoints for student profile creation, private inspection, partial updates, and public catalog queries.",
        "specs": (
            "- Endpoints:\n"
            "  1. POST /api/v1/profiles/students/me: Create initial profile (requires HasAcceptedConsent, role STUDENT)\n"
            "  2. GET /api/v1/profiles/students/me: Private full profile view for owner\n"
            "  3. PATCH /api/v1/profiles/students/me: Partial update (skills, courses, bio) with immutability enforcement\n"
            "  4. GET /api/v1/profiles/students/{user_id}/public: Public restricted view (masked contacts)\n"
            "- Target Files: apps/students/views.py, apps/students/urls.py"
        ),
        "deliverables": (
            "- [ ] Student profile views implementing CRUD operations\n"
            "- [ ] Consent requirement check on write operations\n"
            "- [ ] URL routing configuration\n"
            "- [ ] Integration tests covering all student endpoints"
        ),
        "verification": "uv run pytest apps/students/tests/test_views.py"
    },
    {
        "task_id": "PROFILE-TASK-09",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-05",
        "parent_issue_number": "3",
        "title": "[PROFILE-TASK-09] Company Profile Model & Database Migrations",
        "assignee": "juandiegosb",
        "labels": "task,sprint-1",
        "objective": "Implement the CompanyProfile model representing corporate allied partners in db_profiles, with migrations.",
        "specs": (
            "- Table: company_profiles in db_profiles\n"
            "- Fields:\n"
            "  * id: UUIDField (PK)\n"
            "  * user_id: UUIDField (UNIQUE NOT NULL)\n"
            "  * nit: CharField(max_length=25, unique=True)\n"
            "  * business_name: CharField(max_length=200)\n"
            "  * economic_sector: CharField(max_length=100)\n"
            "  * description: TextField()\n"
            "  * website_url: URLField(null=True, blank=True)\n"
            "  * public_links: JSONField(default=list)\n"
            "  * contact_name: CharField(max_length=150)\n"
            "  * contact_email: EmailField()\n"
            "  * contact_phone: CharField(max_length=25)\n"
            "  * is_verified: BooleanField(default=True)\n"
            "  * created_at, updated_at: DateTimeField\n"
            "- Target Files: apps/companies/models.py, apps/companies/migrations/0001_initial.py"
        ),
        "deliverables": (
            "- [ ] CompanyProfile Django model with unique constraints on nit and user_id\n"
            "- [ ] Django migration generated and applied\n"
            "- [ ] Admin registration for company inspection\n"
            "- [ ] Model tests verifying constraints and timestamps"
        ),
        "verification": "uv run python manage.py migrate"
    },
    {
        "task_id": "PROFILE-TASK-10",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-05",
        "parent_issue_number": "3",
        "title": "[PROFILE-TASK-10] Company Profile Serializers & NIT Validator",
        "assignee": "juandiegosb",
        "labels": "task,sprint-1",
        "objective": "Create DRF serializers for Company Profiles with Colombian DIAN NIT format/check-digit validation and contact masking.",
        "specs": (
            "- Business Rules:\n"
            "  * Validate Colombian NIT format (e.g. 900123456-7) with modulo 11 check-digit verification\n"
            "  * Enforce immutability of validated NIT on update (ValidationError HTTP 400)\n"
            "  * CompanyProfilePublicSerializer must omit contact_email, contact_phone, and contact_name per RF08\n"
            "- Serializers:\n"
            "  * CompanyProfileCreateSerializer, CompanyProfileUpdateSerializer\n"
            "  * CompanyProfilePrivateSerializer, CompanyProfilePublicSerializer\n"
            "- Target Files: apps/companies/serializers.py, apps/companies/validators.py"
        ),
        "deliverables": (
            "- [ ] Colombian DIAN NIT validation utility\n"
            "- [ ] Serializers with NIT format checks and immutability enforcement\n"
            "- [ ] Public serializer omitting direct contact channels\n"
            "- [ ] Unit tests for valid/invalid NITs and public serialization"
        ),
        "verification": "uv run pytest apps/companies/tests/test_serializers.py"
    },
    {
        "task_id": "PROFILE-TASK-11",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-05",
        "parent_issue_number": "3",
        "title": "[PROFILE-TASK-11] Company Profile CRUD & Public Restricted Endpoints",
        "assignee": "juandiegosb",
        "labels": "task,sprint-1",
        "objective": "Expose endpoints for company profile registration, private consultation, updates, and public company catalog views.",
        "specs": (
            "- Endpoints:\n"
            "  1. POST /api/v1/profiles/companies/me: Initial company registration (requires HasAcceptedConsent, role COMPANY)\n"
            "  2. GET /api/v1/profiles/companies/me: Private full company profile view\n"
            "  3. PATCH /api/v1/profiles/companies/me: Update sector, description, website (NIT immutable)\n"
            "  4. GET /api/v1/profiles/companies/{user_id}/public: Public view for students (masked contacts)\n"
            "- Target Files: apps/companies/views.py, apps/companies/urls.py"
        ),
        "deliverables": (
            "- [ ] Company profile views implementing CRUD operations\n"
            "- [ ] Consent enforcement on company registration\n"
            "- [ ] URL routing configuration\n"
            "- [ ] Integration tests covering all company endpoints"
        ),
        "verification": "uv run pytest apps/companies/tests/test_views.py"
    },
    {
        "task_id": "PROFILE-TASK-12",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-04, HU-05",
        "parent_issue_number": "2",
        "title": "[PROFILE-TASK-12] Internal Eligibility & Contact Channel Endpoint",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-1",
        "objective": "Implement synchronous internal endpoint for application service to verify student semester eligibility and reveal contact channels upon acceptance.",
        "specs": (
            "- Endpoint: GET /api/v1/profiles/internal/{user_id}/eligibility\n"
            "- Security: Internal service token or scope profile:read_internal\n"
            "- Response Body:\n"
            "  * is_eligible: bool (consent accepted AND current_semester between 6 and 10)\n"
            "  * current_semester: int\n"
            "  * has_consent: bool\n"
            "  * contact_info: { email, phone } (revealed per RB-05 / RF31 upon formal application acceptance)\n"
            "- Target Files: apps/core/views.py, apps/core/urls.py"
        ),
        "deliverables": (
            "- [ ] GET /api/v1/profiles/internal/{user_id}/eligibility view\n"
            "- [ ] Eligibility validation logic against DataConsent and StudentProfile\n"
            "- [ ] Contact info payload generation\n"
            "- [ ] Unit tests testing eligible, ineligible (semester < 6), and missing consent responses"
        ),
        "verification": "uv run pytest apps/core/tests/test_eligibility.py"
    },
    {
        "task_id": "PROFILE-TASK-13",
        "repo": "profile",
        "service": "profile",
        "parent_story": "HU-03, HU-04, HU-05",
        "parent_issue_number": "1",
        "title": "[PROFILE-TASK-13] Unit & Integration Test Suite for Profile",
        "assignee": "juandiegosb",
        "labels": "task,sprint-1",
        "objective": "Implement full Pytest-django test suite covering consent blocking, semester validation boundaries, immutability rules, and NIT validation.",
        "specs": (
            "- Framework: pytest, pytest-django, DRF APIClient\n"
            "- Target Coverage: >= 80% line coverage\n"
            "- Test Scenarios:\n"
            "  * Consent: blocking without consent, successful consent recording with IP/User-Agent\n"
            "  * Student: semester 6-10 boundaries (reject <6 or >10), student_code immutability rejection\n"
            "  * Company: NIT check-digit validation, immutable NIT rejection\n"
            "  * Privacy: verify contact_email and contact_phone are omitted from all public serializers\n"
            "  * Internal: eligibility validation endpoint\n"
            "- Target Files: tests/conftest.py, apps/*/tests/*.py"
        ),
        "deliverables": (
            "- [ ] Pytest fixtures for mock JWT tokens and test database\n"
            "- [ ] Comprehensive test cases across consents, students, companies, and core\n"
            "- [ ] Coverage report confirming >= 80%\n"
            "- [ ] Green CI test execution"
        ),
        "verification": "uv run pytest --cov=apps --cov-report=term-missing"
    }
]


def build_markdown_body(task: dict) -> str:
    """Builds the standardized markdown body following .github/ISSUE_TEMPLATE/task.md"""
    parent_repo = task["repo"]
    parent_issue = task["parent_issue_number"]
    return (
        f"### 1. Task Metadata & Traceability\n"
        f"- **Module / Microservice:** `{task['service']}`\n"
        f"- **Parent User Story:** {task['parent_story']} (Closes part of conecta-nexus/{parent_repo}#{parent_issue})\n"
        f"- **Assigned Developer:** @{task['assignee']}\n"
        f"- **Sprint:** Sprint 1 (12 Oct – 22 Oct 2026)\n"
        f"- **Labels:** `task`, `sprint-1`\n\n"
        f"---\n\n"
        f"### 2. Objective & Description\n"
        f"{task['objective']}\n\n"
        f"---\n\n"
        f"### 3. Technical Specifications & Constraints\n"
        f"{task['specs']}\n\n"
        f"---\n\n"
        f"### 4. Acceptance Criteria & Deliverables\n"
        f"{task['deliverables']}\n\n"
        f"---\n\n"
        f"### 5. Verification Command\n"
        f"```bash\n{task['verification']}\n```"
    )


def main():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conecta_nexus_sprint_1_tasks.csv")
    fieldnames = [
        "task_id", "repo", "service", "parent_story", "parent_issue_number",
        "title", "assignee", "labels", "objective", "specs", "deliverables",
        "verification", "body"
    ]
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for task in TASKS:
            row = dict(task)
            row["body"] = build_markdown_body(task)
            writer.writerow(row)
    print(f"✔ Generated {len(TASKS)} tasks into '{filename}'.")


if __name__ == "__main__":
    main()
