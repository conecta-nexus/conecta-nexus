#!/usr/bin/env python3
"""
Conecta Nexus - Sprint 2 Full Technical Tasks Generator
Decomposes Sprint 2 User Stories (HU-06 to HU-10) into 30 granular engineering tasks
across the entire microservice ecosystem:
- 'challenge' microservice (14 backend tasks)
- 'frontend' Nuxt 4 app (10 frontend tasks)
- 'infra' GCP Terraform & local Compose (4 infrastructure tasks)
- 'gateway' Nginx API Gateway (2 gateway tasks)

Equitably distributed (exactly 10 tasks each) among the 3 developers:
@juandiegosb, @NelsonConde, and @AnorakTeam.
"""

import os
import csv

TASKS = [
    # =========================================================================
    # HU-06: Business Need and Challenge Publication (8 pts - Must Have)
    # =========================================================================
    {
        "task_id": "CHALLENGE-TASK-01",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-06",
        "parent_issue_number": "1",
        "title": "[CHALLENGE-TASK-01] Database Engine & Connection Configuration",
        "assignee": "NelsonConde",
        "labels": "task,sprint-2",
        "objective": "Configure the async SQLAlchemy engine, connection pool, session factory, and pydantic-settings configuration for db_challenges on PostgreSQL 16.",
        "specs": (
            "- Database: PostgreSQL 16 (db_challenges)\n"
            "- Engine: SQLAlchemy async engine (create_async_engine) with asyncpg driver\n"
            "- Pool: pool_size=10, max_overflow=20, pool_pre_ping=True\n"
            "- Configuration: pydantic-settings BaseSettings loading DATABASE_URL, DB_ECHO, APP_ENV\n"
            "- Target Files: src/core/config.py, src/core/database.py"
        ),
        "deliverables": (
            "- [ ] Implement Settings class in src/core/config.py using pydantic-settings\n"
            "- [ ] Configure async_engine and async_sessionmaker in src/core/database.py\n"
            "- [ ] Provide get_db async generator dependency for FastAPI routers\n"
            "- [ ] Unit tests verifying database connection and session yield"
        ),
        "verification": "uv run python -c 'from src.core.database import async_engine; print(async_engine)'"
    },
    {
        "task_id": "CHALLENGE-TASK-02",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-06",
        "parent_issue_number": "1",
        "title": "[CHALLENGE-TASK-02] Stateless RS256 JWT Authentication & Scopes RBAC (ADR-002)",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-2",
        "objective": "Implement stateless RS256 JWT token verification (ADR-002) using the RSA public key and role-based scope dependencies in FastAPI.",
        "specs": (
            "- ADR-002: Stateless token validation using RSA public key (jwt_public.pem), no database lookup to auth\n"
            "- Token Claims: sub (User UUID), role (COMPANY, STUDENT, ADMIN), scope (list of strings), exp, iss, aud\n"
            "- Dependencies: get_current_user, require_role(role: str), require_scope(scope: str)\n"
            "- Target Files: src/core/security.py, src/core/dependencies.py"
        ),
        "deliverables": (
            "- [ ] RSA public key loader in src/core/security.py\n"
            "- [ ] decode_token utility validating signature, issuer, and expiration\n"
            "- [ ] FastAPI security dependencies for role and scope enforcement\n"
            "- [ ] Unit tests verifying valid token decoding, expired token rejection, and role matching"
        ),
        "verification": "uv run pytest tests/test_security.py"
    },
    {
        "task_id": "CHALLENGE-TASK-03",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-06",
        "parent_issue_number": "1",
        "title": "[CHALLENGE-TASK-03] Challenge Database Model & PostgreSQL Constraints",
        "assignee": "NelsonConde",
        "labels": "task,sprint-2",
        "objective": "Implement the Challenge SQLAlchemy model in db_challenges with state enums, JSONB skills, semester check constraints, and Alembic migrations.",
        "specs": (
            "- Table: challenges in db_challenges\n"
            "- Columns:\n"
            "  * id: UUID (Primary Key, default gen_random_uuid())\n"
            "  * company_id: UUID (NOT NULL, indexed)\n"
            "  * title: VARCHAR(255) (NOT NULL)\n"
            "  * description: TEXT (NOT NULL)\n"
            "  * business_process: VARCHAR(255) (NOT NULL)\n"
            "  * status: VARCHAR(20) (NOT NULL, CHECK status IN ('DRAFT', 'OPEN', 'IN_PROGRESS', 'CLOSED', 'CANCELLED'), DEFAULT 'DRAFT')\n"
            "  * difficulty_level: VARCHAR(20) (NOT NULL, CHECK difficulty_level IN ('BEGINNER', 'INTERMEDIATE', 'ADVANCED'))\n"
            "  * modality: VARCHAR(20) (NOT NULL, CHECK modality IN ('REMOTE', 'HYBRID', 'ON_SITE'))\n"
            "  * min_semester: INTEGER (NOT NULL, CHECK min_semester BETWEEN 6 AND 10, DEFAULT 6)\n"
            "  * economic_sector: VARCHAR(100) (NOT NULL)\n"
            "  * required_skills: JSONB (NOT NULL, DEFAULT '[]')\n"
            "  * knowledge_areas: JSONB (NOT NULL, DEFAULT '[]')\n"
            "  * created_at: TIMESTAMPTZ (NOT NULL, DEFAULT CURRENT_TIMESTAMP)\n"
            "  * updated_at: TIMESTAMPTZ (NOT NULL, DEFAULT CURRENT_TIMESTAMP)\n"
            "- Target Files: src/models/challenge.py, alembic/versions/001_create_challenges_table.py"
        ),
        "deliverables": (
            "- [ ] Declarative SQLAlchemy model for Challenge with all column types and CHECK constraints\n"
            "- [ ] Configure Alembic environment reading models\n"
            "- [ ] Initial migration generated and applied cleanly against PostgreSQL\n"
            "- [ ] Model unit tests verifying constraints, defaults, and enums"
        ),
        "verification": "uv run alembic upgrade head"
    },
    {
        "task_id": "CHALLENGE-TASK-04",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-06",
        "parent_issue_number": "1",
        "title": "[CHALLENGE-TASK-04] Challenge Pydantic v2 Schemas & Repository",
        "assignee": "NelsonConde",
        "labels": "task,sprint-2",
        "objective": "Create Pydantic v2 schemas for challenge creation, update, and inspection, and implement the ChallengeRepository for asynchronous database persistence.",
        "specs": (
            "- Schemas:\n"
            "  * ChallengeCreate: title, description, business_process, difficulty_level, modality, min_semester (6-10), economic_sector, required_skills, knowledge_areas, optional status ('DRAFT' or 'OPEN')\n"
            "  * ChallengeUpdate: optional fields, status changes restricted\n"
            "  * ChallengeResponse: full company view with id, company_id, status, created_at, updated_at\n"
            "- Repository: ChallengeRepository\n"
            "  * create(db, challenge_in: ChallengeCreate, company_id: UUID) -> Challenge\n"
            "  * get_by_id(db, challenge_id: UUID) -> Challenge | None\n"
            "  * update(db, db_obj: Challenge, obj_in: ChallengeUpdate) -> Challenge\n"
            "  * list_by_company(db, company_id: UUID, skip: int, limit: int) -> list[Challenge]\n"
            "- Target Files: src/schemas/challenge.py, src/repositories/challenge_repository.py"
        ),
        "deliverables": (
            "- [ ] Pydantic v2 schemas with strict field and semester boundary validation\n"
            "- [ ] ChallengeRepository with async SQLAlchemy select and commit operations\n"
            "- [ ] Unit tests for schema serialization and repository CRUD methods"
        ),
        "verification": "uv run pytest tests/test_challenge_repository.py"
    },
    {
        "task_id": "CHALLENGE-TASK-05",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-06",
        "parent_issue_number": "1",
        "title": "[CHALLENGE-TASK-05] Challenge Publication & Ownership Protection Endpoint",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-2",
        "objective": "Expose challenge creation and edition endpoints, enforcing strict company ownership (RB-06 / RF15) and limiting modifications to Draft or Open states.",
        "specs": (
            "- Endpoints:\n"
            "  * POST /api/v1/challenges/: Create challenge for authenticated COMPANY (201 Created)\n"
            "  * GET /api/v1/challenges/{id}: Private full challenge details for owner\n"
            "  * PATCH /api/v1/challenges/{id}: Update challenge details\n"
            "- Business Rules:\n"
            "  * Only users with role COMPANY can create challenges\n"
            "  * RB-06: Companies can only edit their own challenges (company_id == user.id), returning HTTP 403 Forbidden if another company attempts access\n"
            "  * RB-06: Modifications only permitted while challenge is in DRAFT or OPEN status (HTTP 422 Unprocessable Entity if IN_PROGRESS or CLOSED)\n"
            "- Target Files: src/routers/challenges.py, src/services/challenge_service.py"
        ),
        "deliverables": (
            "- [ ] POST /api/v1/challenges/ route with company role requirement\n"
            "- [ ] Ownership verification service logic protecting PATCH and GET routes\n"
            "- [ ] State mutability check blocking edits on closed or in-progress challenges\n"
            "- [ ] Integration tests verifying successful creation, 403 ownership rejection, and state locking"
        ),
        "verification": "uv run pytest tests/test_challenge_endpoints.py"
    },
    {
        "task_id": "FRONTEND-TASK-01",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-06",
        "parent_issue_number": "1",
        "title": "[FRONTEND-TASK-01] Challenge TypeScript Interfaces & useChallenges Composable",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-2",
        "objective": "Create TypeScript interfaces for challenges, attachments, and filters, and implement the reactive useChallenges composable for API communication.",
        "specs": (
            "- TypeScript Interfaces: app/types/challenge.ts (Challenge, ChallengeCreatePayload, ChallengeUpdatePayload, ChallengeStatus, Attachment, CatalogFilters, CatalogPagination)\n"
            "- Composable: app/composables/useChallenges.ts wrapping useApi()\n"
            "  * createChallenge(payload): POST /challenges/\n"
            "  * updateChallenge(id, payload): PATCH /challenges/{id}\n"
            "  * fetchCompanyChallenges(status?): GET /challenges/company/me\n"
            "  * fetchChallengeDetail(id): GET /challenges/{id}\n"
            "- Target Files: app/types/challenge.ts, app/composables/useChallenges.ts"
        ),
        "deliverables": (
            "- [ ] Define complete TypeScript models matching challenge microservice schemas\n"
            "- [ ] Implement useChallenges composable with error handling and reactive state\n"
            "- [ ] Token authentication header injection via useApi integration\n"
            "- [ ] Typecheck and lint pass without warnings"
        ),
        "verification": "cd frontend && pnpm lint"
    },
    {
        "task_id": "FRONTEND-TASK-02",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-06",
        "parent_issue_number": "1",
        "title": "[FRONTEND-TASK-02] Company Challenge Creation Form Page (/challenges/new)",
        "assignee": "NelsonConde",
        "labels": "task,sprint-2",
        "objective": "Build the challenge publishing page with multi-field forms, Tiptap rich-text problem description, tags selector, and company role guard.",
        "specs": (
            "- Route: app/pages/challenges/new.vue\n"
            "- Form Components: title, problem description (Tiptap markdown), business process, modality, difficulty level, min semester (6-10), economic sector, skills tag selector\n"
            "- Role Guard: Nuxt middleware redirecting non-company users with toast notification\n"
            "- Actions: 'Save as Draft' and 'Publish Challenge' triggers\n"
            "- Target Files: app/pages/challenges/new.vue, app/components/challenges/ChallengeForm.vue"
        ),
        "deliverables": (
            "- [ ] Nuxt page challenges/new.vue with auth/role protection\n"
            "- [ ] Form component with client-side validation for required fields\n"
            "- [ ] Interactive tag chips input for required technical skills\n"
            "- [ ] Successful submission redirecting to company challenge management"
        ),
        "verification": "cd frontend && pnpm lint"
    },
    {
        "task_id": "INFRA-TASK-01",
        "repo": "infra",
        "service": "infra",
        "parent_story": "HU-06",
        "parent_issue_number": "1",
        "title": "[INFRA-TASK-01] Cloud Run Terraform Provisioning for Challenge Service",
        "assignee": "NelsonConde",
        "labels": "task,sprint-2",
        "objective": "Define the Google Cloud Run v2 service resource for challenge in Terraform with Cloud SQL instance connection, VPC connector, environment variables, and autoscaling.",
        "specs": (
            "- Target File: infra/cloud_run.tf, infra/variables.tf\n"
            "- Resource: google_cloud_run_v2_service.challenge\n"
            "- Image: ${var.region}-docker.pkg.dev/${var.project_id}/conecta-nexus-repo/challenge:latest\n"
            "- Cloud SQL volume mount: db_challenges on instance google_sql_database_instance.postgres\n"
            "- Scaling: min_instance_count = 0, max_instance_count = 5, cpu = '1', memory = '512Mi'\n"
            "- IAM: roles/run.invoker for Gateway service account"
        ),
        "deliverables": (
            "- [ ] Add google_cloud_run_v2_service.challenge to infra/cloud_run.tf\n"
            "- [ ] Configure environment variables (DATABASE_URL, APP_ENV, JWT_PUBLIC_KEY_PATH)\n"
            "- [ ] Cloud SQL connection attachment\n"
            "- [ ] Terraform plan validation passes cleanly"
        ),
        "verification": "cd infra && terraform validate"
    },

    # =========================================================================
    # HU-07: Secure Technical Attachment Management (5 pts - Should Have)
    # =========================================================================
    {
        "task_id": "CHALLENGE-TASK-06",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-07",
        "parent_issue_number": "2",
        "title": "[CHALLENGE-TASK-06] Object Storage Client & Storage Service (MinIO/GCS)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-2",
        "objective": "Integrate MinIO/GCS object storage client into FastAPI to handle file uploads, byte streaming, and presigned/signed download URL generation.",
        "specs": (
            "- Provider: S3-compatible MinIO client (or Google Cloud Storage client) via aioboto3 or minio SDK\n"
            "- Bucket: challenge-attachments\n"
            "- Operations:\n"
            "  * upload_file(file_obj, destination_path: str, content_type: str) -> str\n"
            "  * generate_signed_url(storage_path: str, expires_in_seconds: int = 3600) -> str\n"
            "  * delete_file(storage_path: str) -> bool\n"
            "- Target Files: src/core/storage.py, src/services/storage_service.py"
        ),
        "deliverables": (
            "- [ ] Storage client initialization and connection pooling in src/core/storage.py\n"
            "- [ ] StorageService class with upload, signed URL, and delete methods\n"
            "- [ ] Local MinIO container / bucket auto-initialization hook\n"
            "- [ ] Unit tests with mock storage client validating file streaming and signed URL generation"
        ),
        "verification": "uv run pytest tests/test_storage_service.py"
    },
    {
        "task_id": "CHALLENGE-TASK-07",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-07",
        "parent_issue_number": "2",
        "title": "[CHALLENGE-TASK-07] Attachment Database Model & Storage Migrations",
        "assignee": "NelsonConde",
        "labels": "task,sprint-2",
        "objective": "Implement the ChallengeAttachment SQLAlchemy model representing technical support files, with size and MIME type constraints in db_challenges.",
        "specs": (
            "- Table: challenge_attachments in db_challenges\n"
            "- Columns:\n"
            "  * id: UUID (Primary Key, default gen_random_uuid())\n"
            "  * challenge_id: UUID (NOT NULL, FK challenges.id ON DELETE CASCADE, indexed)\n"
            "  * file_name: VARCHAR(255) (NOT NULL)\n"
            "  * file_size_bytes: BIGINT (NOT NULL, CHECK file_size_bytes <= 10485760 [10MB])\n"
            "  * mime_type: VARCHAR(100) (NOT NULL, CHECK mime_type IN ('application/pdf', 'image/png', 'image/jpeg', 'image/webp'))\n"
            "  * storage_path: VARCHAR(512) (NOT NULL)\n"
            "  * uploaded_by: UUID (NOT NULL)\n"
            "  * created_at: TIMESTAMPTZ (NOT NULL, DEFAULT CURRENT_TIMESTAMP)\n"
            "- Target Files: src/models/attachment.py, alembic/versions/002_create_attachments_table.py"
        ),
        "deliverables": (
            "- [ ] Declarative ChallengeAttachment model with CASCADE delete on parent challenge\n"
            "- [ ] PostgreSQL CHECK constraints for <= 10MB and allowed MIME types\n"
            "- [ ] Alembic migration generated and applied cleanly\n"
            "- [ ] Model tests verifying cascade deletion and constraint violation handling"
        ),
        "verification": "uv run alembic upgrade head"
    },
    {
        "task_id": "CHALLENGE-TASK-08",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-07",
        "parent_issue_number": "2",
        "title": "[CHALLENGE-TASK-08] Attachment Upload & Signed Download Endpoints",
        "assignee": "juandiegosb",
        "labels": "task,sprint-2",
        "objective": "Expose multipart upload endpoint enforcing size limits (<=10MB) and MIME checks, alongside signed download and deletion routes.",
        "specs": (
            "- Endpoints:\n"
            "  * POST /api/v1/challenges/{id}/attachments: multipart file upload, size <= 10MB, MIME verification\n"
            "  * GET /api/v1/challenges/{id}/attachments: list attachments with active signed download URLs\n"
            "  * DELETE /api/v1/challenges/{id}/attachments/{attachment_id}: delete attachment and storage object\n"
            "- Business Rules: RB-06 company ownership check; RB-07 size limit <= 10MB (HTTP 413) and PDF/Images only (HTTP 415)\n"
            "- Target Files: src/routers/attachments.py, src/services/attachment_service.py, src/schemas/attachment.py"
        ),
        "deliverables": (
            "- [ ] POST attachment endpoint with chunked streaming size validation\n"
            "- [ ] MIME verification inspecting magic bytes and content types\n"
            "- [ ] Ephemeral signed URL generation for attachment downloads\n"
            "- [ ] Integration tests testing valid upload, 413 oversized rejection, and 415 format rejection"
        ),
        "verification": "uv run pytest tests/test_attachment_upload.py"
    },
    {
        "task_id": "FRONTEND-TASK-03",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-07",
        "parent_issue_number": "2",
        "title": "[FRONTEND-TASK-03] Drag-and-Drop Attachment Uploader Component with Size/MIME Validation",
        "assignee": "juandiegosb",
        "labels": "task,sprint-2",
        "objective": "Implement reusable attachment uploader component with client-side 10MB limit enforcement, format restrictions, and upload progress indicator.",
        "specs": (
            "- Component: app/components/challenges/AttachmentUploader.vue\n"
            "- Props: challengeId: string, readonly?: boolean\n"
            "- Client Validation: Reject files > 10MB with toast alert; permit only PDF (.pdf) and images (.png, .jpg, .jpeg, .webp)\n"
            "- Progress Handling: Chunked upload animation with upload progress bar\n"
            "- Target Files: app/components/challenges/AttachmentUploader.vue, app/composables/useChallenges.ts"
        ),
        "deliverables": (
            "- [ ] Drag-and-drop file upload component with file picker button\n"
            "- [ ] Client-side pre-validation for 10MB boundary and MIME types\n"
            "- [ ] Upload progress state and error display\n"
            "- [ ] Emits uploaded event with updated attachment metadata"
        ),
        "verification": "cd frontend && pnpm lint"
    },
    {
        "task_id": "FRONTEND-TASK-04",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-07",
        "parent_issue_number": "2",
        "title": "[FRONTEND-TASK-04] Attachment Download & Ephemeral Link Preview Component",
        "assignee": "juandiegosb",
        "labels": "task,sprint-2",
        "objective": "Build the attachment list view component displaying file badges, human-readable file sizes, download triggers, and owner delete actions.",
        "specs": (
            "- Component: app/components/challenges/AttachmentList.vue\n"
            "- Props: attachments: Attachment[], canDelete: boolean\n"
            "- Features: File icon according to MIME type, human-readable size (e.g. 2.4 MB), direct download link opening signed URL in new tab, delete button with confirmation dialog\n"
            "- Target Files: app/components/challenges/AttachmentList.vue"
        ),
        "deliverables": (
            "- [ ] Attachment list cards with file icon, name, and size badges\n"
            "- [ ] Download button triggering secure signed URL access\n"
            "- [ ] Delete button with confirmation modal calling useChallenges().deleteAttachment\n"
            "- [ ] Reactive state updating immediately upon file removal"
        ),
        "verification": "cd frontend && pnpm lint"
    },
    {
        "task_id": "INFRA-TASK-02",
        "repo": "infra",
        "service": "infra",
        "parent_story": "HU-07",
        "parent_issue_number": "2",
        "title": "[INFRA-TASK-02] Cloud Storage Bucket & IAM Binding for Technical Attachments",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-2",
        "objective": "Provision Google Cloud Storage bucket in Terraform for challenge attachments with CORS rules, lifecycle management, and service account access.",
        "specs": (
            "- Target File: infra/storage.tf\n"
            "- Resource: google_storage_bucket.challenge_attachments\n"
            "- Bucket Name: conecta-nexus-${var.environment}-challenge-attachments\n"
            "- Location: var.region (Standard storage class, uniform bucket-level access)\n"
            "- CORS: Allow origins (var.cors_allowed_origins), methods (GET, PUT, POST, HEAD), max age 3600\n"
            "- IAM: google_storage_bucket_iam_member granting roles/storage.objectAdmin to challenge Cloud Run service account"
        ),
        "deliverables": (
            "- [ ] Create infra/storage.tf with google_storage_bucket resource\n"
            "- [ ] Configure CORS block for frontend signed URL uploads/downloads\n"
            "- [ ] Attach IAM policy binding for challenge service account\n"
            "- [ ] Output bucket name in infra/outputs.tf"
        ),
        "verification": "cd infra && terraform validate"
    },
    {
        "task_id": "INFRA-TASK-03",
        "repo": "infra",
        "service": "infra",
        "parent_story": "HU-07",
        "parent_issue_number": "2",
        "title": "[INFRA-TASK-03] MinIO Object Storage Setup for Local Containerized Environment",
        "assignee": "NelsonConde",
        "labels": "task,sprint-2",
        "objective": "Configure MinIO S3-compatible object storage container and auto-bucket creation in compose.yaml for local development of challenge attachments.",
        "specs": (
            "- Target Files: compose.yaml, challenge/.env.example\n"
            "- Service minio: image minio/minio:latest, ports 9000:9000 and 9001:9001 (console), volume minio_data:/data\n"
            "- Service minio-init: minio/mc container waiting for minio, creating bucket challenge-attachments, setting access policy\n"
            "- Dependencies: challenge service depends_on minio (healthy)"
        ),
        "deliverables": (
            "- [ ] Add minio and minio-init services to compose.yaml\n"
            "- [ ] Configure STORAGE_ENDPOINT and STORAGE_BUCKET in challenge/.env.example\n"
            "- [ ] Verify podman/docker compose config syntax\n"
            "- [ ] Test bucket creation on container startup"
        ),
        "verification": "podman compose config || docker compose config"
    },
    {
        "task_id": "GATEWAY-TASK-01",
        "repo": "gateway",
        "service": "gateway",
        "parent_story": "HU-07",
        "parent_issue_number": "2",
        "title": "[GATEWAY-TASK-01] Large Attachment Streaming & Proxy Buffering Optimization",
        "assignee": "NelsonConde",
        "labels": "task,sprint-2",
        "objective": "Optimize Nginx gateway configurations for multipart file uploads up to 10MB, disabling request buffering to stream directly to the challenge service.",
        "specs": (
            "- Target Files: gateway/conf.d/default.conf, gateway/templates/default.conf.template\n"
            "- Route: location ~ ^/api/v1/challenge(s)?(/.*)?$\n"
            "- Directives:\n"
            "  * client_max_body_size 25M;\n"
            "  * proxy_request_buffering off; (real-time stream upload without disk buffering)\n"
            "  * proxy_read_timeout 120s;\n"
            "  * proxy_send_timeout 120s;\n"
            "  * Access-Control-Expose-Headers: Content-Disposition, Content-Length, ETag"
        ),
        "deliverables": (
            "- [ ] Update default.conf and default.conf.template with streaming proxy directives\n"
            "- [ ] Configure extended timeout limits for 10MB attachment uploads\n"
            "- [ ] Ensure Content-Disposition is exposed in CORS headers\n"
            "- [ ] Validate Nginx configuration syntax"
        ),
        "verification": "docker run --rm -v $(pwd)/gateway/conf.d:/etc/nginx/conf.d:ro nginx:alpine nginx -t 2>/dev/null || true"
    },

    # =========================================================================
    # HU-08: Own Challenge Administration and Voluntary Closure (5 pts) - Should Have
    # =========================================================================
    {
        "task_id": "CHALLENGE-TASK-09",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-08",
        "parent_issue_number": "3",
        "title": "[CHALLENGE-TASK-09] Challenge Lifecycle State Machine & Justification Model",
        "assignee": "juandiegosb",
        "labels": "task,sprint-2",
        "objective": "Implement challenge status transition rules and the ChallengeClosureLog database model to audit voluntary closures with mandatory justifications.",
        "specs": (
            "- Table: challenge_closure_logs in db_challenges (id, challenge_id, closed_by, previous_status, target_status, closure_reason, created_at)\n"
            "- State Machine: DRAFT -> OPEN (publish); OPEN -> CLOSED or CANCELLED (requires justification >= 15 chars); illegal transitions blocked\n"
            "- Target Files: src/models/closure.py, src/services/lifecycle_service.py, alembic/versions/003_create_closure_logs_table.py"
        ),
        "deliverables": (
            "- [ ] ChallengeClosureLog SQLAlchemy model and Alembic migration\n"
            "- [ ] State machine transition validator in LifecycleService\n"
            "- [ ] Unit tests verifying valid and illegal state transitions"
        ),
        "verification": "uv run alembic upgrade head"
    },
    {
        "task_id": "CHALLENGE-TASK-10",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-08",
        "parent_issue_number": "3",
        "title": "[CHALLENGE-TASK-10] Voluntary Closure & Company Dashboard Endpoints",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-2",
        "objective": "Expose endpoints for voluntary challenge closure requiring mandatory reason, and private company challenge portfolio query.",
        "specs": (
            "- Endpoints:\n"
            "  * POST /api/v1/challenges/{id}/close: requires closure_reason (>= 15 chars), sets status to CLOSED\n"
            "  * POST /api/v1/challenges/{id}/publish: transitions DRAFT to OPEN\n"
            "  * GET /api/v1/challenges/company/me: paginated list of company's challenges with status filters and summary metrics\n"
            "- Target Files: src/routers/challenges.py, src/services/challenge_service.py, src/schemas/closure.py"
        ),
        "deliverables": (
            "- [ ] Closure endpoint verifying mandatory justification (>= 15 chars)\n"
            "- [ ] Publish endpoint transitioning DRAFT to OPEN\n"
            "- [ ] Company portfolio endpoint returning all owned challenges and status counts\n"
            "- [ ] Integration tests verifying closure audit and company data isolation"
        ),
        "verification": "uv run pytest tests/test_challenge_closure.py"
    },
    {
        "task_id": "FRONTEND-TASK-05",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-08",
        "parent_issue_number": "3",
        "title": "[FRONTEND-TASK-05] Company Challenge Management Dashboard Page (/challenges/manage)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-2",
        "objective": "Build the company challenges portfolio dashboard with status tabs, metrics counters, quick action buttons, and publication toggles.",
        "specs": (
            "- Route: app/pages/challenges/manage.vue\n"
            "- Role Guard: Restrict to COMPANY role\n"
            "- Dashboard Features: Summary metric cards (Draft, Open, In Progress, Closed); status filter tabs; challenges table with dates, applications count, and status badges; action dropdowns ('Edit', 'Publish', 'Manage Files', 'Close')\n"
            "- Target Files: app/pages/challenges/manage.vue, app/components/challenges/CompanyChallengeTable.vue"
        ),
        "deliverables": (
            "- [ ] Nuxt management page with data fetching via useChallenges().fetchCompanyChallenges()\n"
            "- [ ] Metrics overview cards displaying state counts\n"
            "- [ ] Interactive table with action handlers and status badges\n"
            "- [ ] Toast alerts confirming status changes"
        ),
        "verification": "cd frontend && pnpm lint"
    },
    {
        "task_id": "FRONTEND-TASK-06",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-08",
        "parent_issue_number": "3",
        "title": "[FRONTEND-TASK-06] Voluntary Closure Modal with Mandatory Justification Validation",
        "assignee": "juandiegosb",
        "labels": "task,sprint-2",
        "objective": "Implement the modal dialog for voluntary challenge closure, enforcing client-side validation of mandatory justification (>=15 chars).",
        "specs": (
            "- Component: app/components/challenges/ChallengeClosureModal.vue\n"
            "- Props: challenge: Challenge | null, isOpen: boolean\n"
            "- Validation: Textarea with live character counter; 'Confirm Closure' button disabled if reason length < 15 chars\n"
            "- Action: Calls useChallenges().closeChallenge(id, { closure_reason, status: 'CLOSED' })\n"
            "- Target Files: app/components/challenges/ChallengeClosureModal.vue"
        ),
        "deliverables": (
            "- [ ] Modal component with UModal, UTextarea, and live character counter\n"
            "- [ ] Validation preventing submission without meaningful justification\n"
            "- [ ] Async mutation call updating challenge state\n"
            "- [ ] Emits closed event to refresh parent table"
        ),
        "verification": "cd frontend && pnpm lint"
    },

    # =========================================================================
    # HU-09: Open Opportunity Catalog Exploration (8 pts - Must Have)
    # =========================================================================
    {
        "task_id": "CHALLENGE-TASK-11",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-09",
        "parent_issue_number": "4",
        "title": "[CHALLENGE-TASK-11] Public Catalog Query Service & Data Masking Serializers",
        "assignee": "juandiegosb",
        "labels": "task,sprint-2",
        "objective": "Implement the public catalog projection service and Pydantic serializers, enforcing privacy data masking by hiding direct company contact details.",
        "specs": (
            "- Rule RB-05 / RF08 / RF19: Hide direct email/phone from catalog and public detail responses\n"
            "- Serializers: ChallengeCatalogItemResponse, ChallengeCatalogDetailResponse\n"
            "- Target Files: src/schemas/catalog.py, src/services/catalog_service.py"
        ),
        "deliverables": (
            "- [ ] Public catalog Pydantic schemas omitting all private contact fields\n"
            "- [ ] Description snippet truncation helper for discovery cards\n"
            "- [ ] Unit tests verifying direct email/phone are never serialized in public responses"
        ),
        "verification": "uv run pytest tests/test_catalog_schemas.py"
    },
    {
        "task_id": "CHALLENGE-TASK-12",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-09",
        "parent_issue_number": "4",
        "title": "[CHALLENGE-TASK-12] Public Catalog Exploration & Detail View Endpoints",
        "assignee": "juandiegosb",
        "labels": "task,sprint-2",
        "objective": "Expose public catalog exploration endpoint with pagination metadata, and public challenge detail route for eligible students.",
        "specs": (
            "- Endpoints:\n"
            "  * GET /api/v1/challenges/catalog: paginated open challenges (status == 'OPEN')\n"
            "  * GET /api/v1/challenges/catalog/{id}: full problem requirements and read-only attachments\n"
            "- Target Files: src/routers/catalog.py, src/repositories/catalog_repository.py"
        ),
        "deliverables": (
            "- [ ] GET /api/v1/challenges/catalog endpoint with pagination metadata\n"
            "- [ ] GET /api/v1/challenges/catalog/{id} detail route with read-only attachment URLs\n"
            "- [ ] Unit tests verifying that only OPEN challenges are returned and draft/closed challenges return 404"
        ),
        "verification": "uv run pytest tests/test_catalog_endpoint.py"
    },
    {
        "task_id": "FRONTEND-TASK-07",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-09",
        "parent_issue_number": "4",
        "title": "[FRONTEND-TASK-07] Opportunity Catalog Grid & Discovery Cards (/challenges)",
        "assignee": "NelsonConde",
        "labels": "task,sprint-2",
        "objective": "Build the main opportunity catalog exploration page with responsive card grid, pagination controls, and discovery summary cards.",
        "specs": (
            "- Route: app/pages/challenges/index.vue\n"
            "- Card Component: app/components/challenges/ChallengeCard.vue (title, truncated description, company name, sector, difficulty badge, modality, semester tag, skills pills)\n"
            "- Pagination: UPagination controls synchronized with page/size query params\n"
            "- Target Files: app/pages/challenges/index.vue, app/components/challenges/ChallengeCard.vue"
        ),
        "deliverables": (
            "- [ ] Main catalog page fetching open opportunities via useChallenges().fetchCatalog()\n"
            "- [ ] Responsive grid card component conforming to design guidelines\n"
            "- [ ] Pagination component with page and size controls\n"
            "- [ ] Privacy check verifying direct company email/phone are never rendered"
        ),
        "verification": "cd frontend && pnpm lint"
    },
    {
        "task_id": "FRONTEND-TASK-08",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-09",
        "parent_issue_number": "4",
        "title": "[FRONTEND-TASK-08] Public Challenge Detail Page with Masked Contacts (/challenges/[id])",
        "assignee": "juandiegosb",
        "labels": "task,sprint-2",
        "objective": "Implement public challenge detail page presenting full technical problem, requirements, downloadable support files, and application CTA.",
        "specs": (
            "- Route: app/pages/challenges/[id].vue\n"
            "- Detail Layout: company name, sector, date, modality, difficulty; formatted problem statement & business process; required skills chips; technical attachments with AttachmentList.vue; Apply to Challenge CTA button\n"
            "- Privacy Masking: strictly masks corporate contact channels (RB-05)\n"
            "- Target Files: app/pages/challenges/[id].vue"
        ),
        "deliverables": (
            "- [ ] Dynamic route page with async data loading and 404 fallback\n"
            "- [ ] Full specification layout with structured technical sections\n"
            "- [ ] Attachment download integration\n"
            "- [ ] Student role verification on 'Apply' action button"
        ),
        "verification": "cd frontend && pnpm lint"
    },
    {
        "task_id": "GATEWAY-TASK-02",
        "repo": "gateway",
        "service": "gateway",
        "parent_story": "HU-09",
        "parent_issue_number": "4",
        "title": "[GATEWAY-TASK-02] Catalog Micro-Caching & Public Route Rate Limiting",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-2",
        "objective": "Configure rate limiting and short-lived proxy caching for public catalog exploration endpoints to safeguard downstream services against high traffic.",
        "specs": (
            "- Target Files: gateway/conf.d/default.conf, gateway/templates/default.conf.template\n"
            "- Rate Limiting Zone: limit_req_zone $binary_remote_addr zone=catalog_limit:10m rate=30r/s;\n"
            "- Proxy Caching: proxy_cache_valid 200 15s; for anonymous GET /api/v1/challenges/catalog\n"
            "- Cache Bypass: proxy_cache_bypass $http_authorization"
        ),
        "deliverables": (
            "- [ ] Define catalog rate limiting zone in Nginx configuration\n"
            "- [ ] Implement 15-second micro-cache for public anonymous catalog queries\n"
            "- [ ] Configure cache bypass for authenticated user requests\n"
            "- [ ] Test gateway routing with caching headers"
        ),
        "verification": "docker run --rm -v $(pwd)/gateway/conf.d:/etc/nginx/conf.d:ro nginx:alpine nginx -t 2>/dev/null || true"
    },

    # =========================================================================
    # HU-10: Reactive Multi-Criteria Filtering (7 pts) - Should Have
    # =========================================================================
    {
        "task_id": "CHALLENGE-TASK-13",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-10",
        "parent_issue_number": "5",
        "title": "[CHALLENGE-TASK-13] GIN Indexes & Multi-Criteria SQL Query Repository",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-2",
        "objective": "Implement PostgreSQL GIN indexes for JSONB arrays and the dynamic multi-attribute query builder for reactive challenge filtering.",
        "specs": (
            "- Indexes in db_challenges: GIN on required_skills and knowledge_areas, B-Tree on status, created_at and sector, modality, difficulty\n"
            "- Repository Query Builder: filter by knowledge areas, skills, sector, modality, difficulty, min_semester, keyword search\n"
            "- Target Files: src/repositories/catalog_repository.py, alembic/versions/004_create_catalog_indexes.py"
        ),
        "deliverables": (
            "- [ ] Alembic migration creating GIN and B-Tree indexes\n"
            "- [ ] Dynamic SQLAlchemy async query builder in CatalogRepository\n"
            "- [ ] Unit tests verifying SQL query generation and index execution plans"
        ),
        "verification": "uv run alembic upgrade head"
    },
    {
        "task_id": "CHALLENGE-TASK-14",
        "repo": "challenge",
        "service": "challenge",
        "parent_story": "HU-10",
        "parent_issue_number": "5",
        "title": "[CHALLENGE-TASK-14] Reactive Filtering Endpoint & Empty-State Metadata",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-2",
        "objective": "Add multi-criteria query parameters to the catalog endpoint and return structured metadata with explicit empty-state messaging when zero matches occur.",
        "specs": (
            "- Endpoint: GET /api/v1/challenges/catalog with query params (knowledge_area, skill, sector, modality, difficulty, max_semester, q)\n"
            "- Empty State Metadata: returns structured metadata with active_filters and code NO_MATCHING_CHALLENGES\n"
            "- Target Files: src/routers/catalog.py, src/schemas/catalog.py"
        ),
        "deliverables": (
            "- [ ] Query parameter parsing and validation in catalog router\n"
            "- [ ] Empty-state metadata serializer\n"
            "- [ ] Integration tests testing multi-filter combinations and empty-state response structure"
        ),
        "verification": "uv run pytest tests/test_catalog_filtering.py"
    },
    {
        "task_id": "FRONTEND-TASK-09",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-10",
        "parent_issue_number": "5",
        "title": "[FRONTEND-TASK-09] Reactive Filter Bar Component & URL Query Sync",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-2",
        "objective": "Build the reactive multi-criteria filter component with debounced search, dropdown selectors, and bidirectional URL query synchronization.",
        "specs": (
            "- Component: app/components/challenges/CatalogFilterBar.vue\n"
            "- Filter Controls: keyword search with 300ms debounce, knowledge area multi-select, skills tag chips, economic sector select, modality toggle, difficulty selector\n"
            "- Synchronization: updates Nuxt router query parameters without page reload\n"
            "- Target Files: app/components/challenges/CatalogFilterBar.vue, app/pages/challenges/index.vue"
        ),
        "deliverables": (
            "- [ ] Responsive filter bar component with expandable mobile drawer\n"
            "- [ ] Debounced text search and multi-select filters\n"
            "- [ ] Nuxt router query synchronization logic\n"
            "- [ ] Active filter count badge and individual filter chip dismissals"
        ),
        "verification": "cd frontend && pnpm lint"
    },
    {
        "task_id": "FRONTEND-TASK-10",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-10",
        "parent_issue_number": "5",
        "title": "[FRONTEND-TASK-10] Filter Empty-State View & Reset Action Component",
        "assignee": "NelsonConde",
        "labels": "task,sprint-2",
        "objective": "Implement dedicated empty-state feedback card when no challenges match applied filters, providing one-click filter reset actions.",
        "specs": (
            "- Component: app/components/challenges/CatalogEmptyState.vue\n"
            "- Elements: Empty state illustration, informative message ('No matching challenges found'), list of active filters causing zero results, primary action button 'Reset All Filters'\n"
            "- Target Files: app/components/challenges/CatalogEmptyState.vue, app/pages/challenges/index.vue"
        ),
        "deliverables": (
            "- [ ] Empty-state UI component integrated into catalog page\n"
            "- [ ] One-click filter reset handler\n"
            "- [ ] Unit/component tests verifying render condition when items.length === 0"
        ),
        "verification": "cd frontend && pnpm lint"
    },
    {
        "task_id": "INFRA-TASK-04",
        "repo": "infra",
        "service": "infra",
        "parent_story": "HU-10",
        "parent_issue_number": "5",
        "title": "[INFRA-TASK-04] Cloud SQL Database & Performance Optimization for db_challenges",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-2",
        "objective": "Verify and apply Cloud SQL flags, connection pooling limits, and resource allocations for db_challenges on PostgreSQL 16.",
        "specs": (
            "- Target Files: infra/cloud_sql.tf\n"
            "- Database: db_challenges on Cloud SQL instance google_sql_database_instance.postgres\n"
            "- Database Flags: max_connections = 100, shared_buffers = '128MB', work_mem = '16MB'\n"
            "- IAM User: grant permissions to Cloud Run challenge service account"
        ),
        "deliverables": (
            "- [ ] Add database resource db_challenges to infra/cloud_sql.tf\n"
            "- [ ] Configure memory and connection optimization flags for JSONB indexing\n"
            "- [ ] Verify service account database access credentials\n"
            "- [ ] Terraform validation passes cleanly"
        ),
        "verification": "cd infra && terraform validate"
    }
]


def build_markdown_body(task: dict) -> str:
    """Builds the standardized markdown body following .github/ISSUE_TEMPLATE/task.md"""
    parent_issue = task["parent_issue_number"]
    return (
        f"### 1. Task Metadata & Traceability\n"
        f"- **Module / Microservice:** `{task['service']}`\n"
        f"- **Parent User Story:** {task['parent_story']} (Closes part of conecta-nexus/challenge#{parent_issue})\n"
        f"- **Assigned Developer:** @{task['assignee']}\n"
        f"- **Sprint:** Sprint 2 (23 Oct – 11 Nov 2026)\n"
        f"- **Labels:** `task`, `sprint-2`\n\n"
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
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conecta_nexus_sprint_2_tasks.csv")
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
