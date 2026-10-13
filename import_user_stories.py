#!/usr/bin/env python3
"""
Conecta Nexus - Importador Automatizado a GitHub Projects & Repositorios
Organización: conecta-nexus
Proyecto: Conecta Nexus Management (#2)
URL: https://github.com/orgs/conecta-nexus/projects/2
"""

import os
import sys
import csv
import time
import shutil
import subprocess

ORG = "conecta-nexus"
PROJECT_NUM = "2"
PROJECT_TITLE = "Conecta Nexus Management"
CSV_FILENAME = "conecta_nexus_user_stories.csv"

# Definición completa de las 14 Historias de Usuario oficiales (100 PH)
USER_STORIES = [
    {
        "id": "HU-01",
        "repo": "auth",
        "service": "auth",
        "title": "[AUTH] HU-01: User Registration and Multi-Role Assignment",
        "statement": "As a new user (Student or Company), I want to register with my institutional/corporate email and secure credentials, so that I have personalized access according to my role.",
        "rf": "RF01, RF03",
        "rb": "RB-01 (Role segregation and secure password policy)",
        "cu": "CU-01",
        "sprint": "Sprint 1",
        "points": 5,
        "priority": "Must Have",
        "assignees": "anorak,nelson",
        "acceptance_criteria": (
            "#### Scenario 1: Successful Registration\n"
            "- **Given** a new visitor with an unregistered email and valid password\n"
            "- **When** they select their role (Student or Company) and submit the registration form\n"
            "- **Then** the system creates the account in `db_auth` with hashed password and confirms registration.\n\n"
            "#### Scenario 2: Duplicate Email\n"
            "- **Given** an existing registered email in the system\n"
            "- **When** a user attempts to register with that email\n"
            "- **Then** the system rejects registration and displays a duplicate email error message."
        ),
        "checklist": (
            "- [ ] Create user schema and SQLAlchemy/Pydantic models in `auth`\n"
            "- [ ] Implement bcrypt password hashing\n"
            "- [ ] Create `/api/v1/auth/register` endpoint\n"
            "- [ ] Add unit tests with pytest covering valid registration and duplicate email"
        )
    },
    {
        "id": "HU-02",
        "repo": "auth",
        "service": "auth",
        "title": "[AUTH] HU-02: Secure Session Management and JWT Lifecycle",
        "statement": "As a registered user, I want to securely log in and obtain JWT access and refresh tokens, so that my authenticated session is protected and verified across microservices.",
        "rf": "RF02, RF05",
        "rb": "RB-01 (Secure session revocation and stateless token validation)",
        "cu": "CU-01",
        "sprint": "Sprint 1",
        "points": 5,
        "priority": "Must Have",
        "assignees": "anorak,nelson",
        "acceptance_criteria": (
            "#### Scenario 1: Successful Login\n"
            "- **Given** a registered user with valid credentials\n"
            "- **When** they submit the login form with email and password\n"
            "- **Then** the system returns JWT access/refresh tokens with user role and active status.\n\n"
            "#### Scenario 2: Invalid Credentials\n"
            "- **Given** an invalid password or non-existent user email\n"
            "- **When** authentication is attempted\n"
            "- **Then** the system responds with HTTP 401 Unauthorized.\n\n"
            "#### Scenario 3: Explicit Logout\n"
            "- **Given** an active authenticated session\n"
            "- **When** the user logs out\n"
            "- **Then** the token is revoked and private route access is invalidated."
        ),
        "checklist": (
            "- [ ] Implement JWT generation, signing, and verification in `auth`\n"
            "- [ ] Create `/api/v1/auth/login` and `/api/v1/auth/logout` endpoints\n"
            "- [ ] Create `/api/v1/auth/verify` endpoint for API Gateway\n"
            "- [ ] Write unit tests for login success, failure, and token expiration"
        )
    },
    {
        "id": "HU-03",
        "repo": "profile",
        "service": "profile",
        "title": "[PROFILE] HU-03: Habeas Data and Law 1581 Consent Registration",
        "statement": "As a platform user, I must provide explicit and traceable consent for personal data processing under Colombian Law 1581 of 2012, so that my account complies with data protection regulations.",
        "rf": "RF09",
        "rb": "RB-05 (Traceable data consent prior to profile activation)",
        "cu": "CU-02, CU-03",
        "sprint": "Sprint 1",
        "points": 5,
        "priority": "Must Have",
        "assignees": "anorak,juan",
        "acceptance_criteria": (
            "#### Scenario 1: Explicit Consent Accepted\n"
            "- **Given** a newly registered user who has not accepted Law 1581 terms\n"
            "- **When** they check the consent box and submit the form\n"
            "- **Then** the system stores the timestamp and version of the consent in `db_profiles`.\n\n"
            "#### Scenario 2: Access Blocked without Consent\n"
            "- **Given** a user attempting to access private profile features without consent\n"
            "- **When** any profile interaction is requested\n"
            "- **Then** the system prompts the mandatory consent modal and halts execution."
        ),
        "checklist": (
            "- [ ] Create `HabeasDataConsent` Django model in `profile`\n"
            "- [ ] Create endpoint `/api/v1/profiles/consent/`\n"
            "- [ ] Implement middleware/serializer check for consent validation\n"
            "- [ ] Unit tests for consent submission and audit log verification"
        )
    },
    {
        "id": "HU-04",
        "repo": "profile",
        "service": "profile",
        "title": "[PROFILE] HU-04: Student Academic Profile and Semester Validation",
        "statement": "As a student, I want to manage my academic profile (skills, active semester between 6th and 10th, and areas of interest) with immutable career code, so that companies can review my profile.",
        "rf": "RF06, RF08, RF10",
        "rb": "RB-02 (Semester 6-10 constraint) & RB-08 (Immutable career and student code)",
        "cu": "CU-02",
        "sprint": "Sprint 1",
        "points": 8,
        "priority": "Should Have",
        "assignees": "anorak,juan",
        "acceptance_criteria": (
            "#### Scenario 1: Valid Student Profile Update\n"
            "- **Given** an authenticated student in semester 6 to 10\n"
            "- **When** they update their technical skills, subjects, and interests\n"
            "- **Then** the profile updates successfully in `db_profiles`.\n\n"
            "#### Scenario 2: Immutable Student Code\n"
            "- **Given** a registered student profile with assigned student code\n"
            "- **When** a modification payload contains a different student code or career\n"
            "- **Then** the system rejects the modification under rule RB-08.\n\n"
            "#### Scenario 3: Semester Out of Range\n"
            "- **Given** an entered semester less than 6 or greater than 10\n"
            "- **When** the profile is saved\n"
            "- **Then** the system returns a validation error."
        ),
        "checklist": (
            "- [ ] Create `StudentProfile` Django model with validators in `profile`\n"
            "- [ ] Enforce immutability of `student_code` and `career` on update\n"
            "- [ ] Implement restricted public view serializer (excluding direct contact details)\n"
            "- [ ] Unit tests for semester boundary checks (semesters 1-5 rejected, 6-10 accepted)"
        )
    },
    {
        "id": "HU-05",
        "repo": "profile",
        "service": "profile",
        "title": "[PROFILE] HU-05: Company Corporate Profile and Tax ID Management",
        "statement": "As a company representative, I want to configure my corporate profile with business name, Tax ID (NIT), sector, and website, so that students can verify institutional credibility.",
        "rf": "RF07, RF08",
        "rb": "RB-05 (Restricted corporate view without private contacts until match)",
        "cu": "CU-03",
        "sprint": "Sprint 1",
        "points": 10,
        "priority": "Should Have",
        "assignees": "anorak,juan",
        "acceptance_criteria": (
            "#### Scenario 1: Corporate Profile Registration\n"
            "- **Given** an authenticated user with Company role\n"
            "- **When** they complete company name, NIT, economic sector, and website\n"
            "- **Then** the corporate profile is saved and marked verified.\n\n"
            "#### Scenario 2: Restricted Public Profile View\n"
            "- **Given** an unauthenticated visitor or student viewing the company profile\n"
            "- **When** the public profile endpoint is requested\n"
            "- **Then** company overview is displayed while direct emails and phones remain hidden."
        ),
        "checklist": (
            "- [ ] Create `CompanyProfile` model with NIT validation in `profile`\n"
            "- [ ] Implement DRF serializer with field-level masking for private contacts\n"
            "- [ ] Create `/api/v1/profiles/company/` CRUD endpoints\n"
            "- [ ] Unit tests for corporate profile creation and public projection"
        )
    },
    {
        "id": "HU-06",
        "repo": "challenge",
        "service": "challenge",
        "title": "[CHALLENGE] HU-06: Business Need and Challenge Publication",
        "statement": "As a verified company, I want to publish real operational challenges detailing problem description, affected business process, and required skills, so that interested students can discover them.",
        "rf": "RF11, RF14, RF15, RF16",
        "rb": "RB-06 (Strict ownership: companies can only edit own challenges in Draft or Open)",
        "cu": "CU-04",
        "sprint": "Sprint 2",
        "points": 8,
        "priority": "Must Have",
        "assignees": "anorak,nelson",
        "acceptance_criteria": (
            "#### Scenario 1: Successful Challenge Publication\n"
            "- **Given** an authenticated company with complete profile\n"
            "- **When** they fill title, problem statement, required skills, and set status to 'Open'\n"
            "- **Then** the challenge is saved in `db_challenges` and becomes visible in the catalog.\n\n"
            "#### Scenario 2: Editing Restrictions\n"
            "- **Given** a challenge belonging to Company A\n"
            "- **When** Company B attempts to update or delete it\n"
            "- **Then** the system returns HTTP 403 Forbidden under rule RF15."
        ),
        "checklist": (
            "- [ ] Create `Challenge` model with state enum (Draft, Open, In Progress, Closed, Cancelled) in `challenge`\n"
            "- [ ] Implement FastAPI route `/api/v1/challenges/` with Pydantic validation\n"
            "- [ ] Enforce ownership checks on update/delete\n"
            "- [ ] Unit tests for challenge creation, state changes, and permission boundary"
        )
    },
    {
        "id": "HU-07",
        "repo": "challenge",
        "service": "challenge",
        "title": "[CHALLENGE] HU-07: Secure Technical Attachment Management",
        "statement": "As a company, I want to attach PDF or image support documents (up to 10MB) to my challenge, so that students have accurate technical context.",
        "rf": "RF12, RF18",
        "rb": "RB-07 (Secure storage, authorized access, size <=10MB, PDF/Image only)",
        "cu": "CU-04",
        "sprint": "Sprint 2",
        "points": 5,
        "priority": "Should Have",
        "assignees": "anorak,nelson",
        "acceptance_criteria": (
            "#### Scenario 1: Valid File Upload\n"
            "- **Given** an open challenge owned by the company\n"
            "- **When** a valid PDF file under 10MB is uploaded\n"
            "- **Then** the file is streamed to Object Storage (MinIO/GCS) and linked via secure URI.\n\n"
            "#### Scenario 2: Oversized File Rejection\n"
            "- **Given** a file larger than 10MB\n"
            "- **When** upload is attempted\n"
            "- **Then** the system blocks the upload with HTTP 413 Payload Too Large.\n\n"
            "#### Scenario 3: Disallowed File Format\n"
            "- **Given** an executable or unsupported file extension\n"
            "- **When** upload is attempted\n"
            "- **Then** the system rejects the file with HTTP 415 Unsupported Media Type."
        ),
        "checklist": (
            "- [ ] Integrate MinIO/GCS client in FastAPI service `challenge`\n"
            "- [ ] Implement file size (<10MB) and MIME type validator\n"
            "- [ ] Create upload endpoint `/api/v1/challenges/{id}/attachments`\n"
            "- [ ] Unit tests for upload validation, signed URL generation, and size boundary"
        )
    },
    {
        "id": "HU-08",
        "repo": "challenge",
        "service": "challenge",
        "title": "[CHALLENGE] HU-08: Own Challenge Administration and Voluntary Closure",
        "statement": "As a company, I want to edit, close, or cancel my open challenges with mandatory justification, so that my organization's portfolio remains accurate.",
        "rf": "RF13, RF14, RF15, RF17",
        "rb": "RB-06 (Mandatory closure justification)",
        "cu": "CU-04",
        "sprint": "Sprint 2",
        "points": 5,
        "priority": "Should Have",
        "assignees": "anorak,nelson",
        "acceptance_criteria": (
            "#### Scenario 1: Voluntary Closure with Reason\n"
            "- **Given** an open challenge owned by the company\n"
            "- **When** the company selects 'Close' and provides a justification\n"
            "- **Then** state transitions to 'Closed' and justification is recorded.\n\n"
            "#### Scenario 2: Closure without Reason Blocked\n"
            "- **Given** an open challenge\n"
            "- **When** closure is submitted with an empty reason\n"
            "- **Then** the system rejects the action with a validation error."
        ),
        "checklist": (
            "- [ ] Create endpoint `/api/v1/challenges/{id}/close`\n"
            "- [ ] Validate mandatory closure justification\n"
            "- [ ] Emit event on state change\n"
            "- [ ] Unit tests for challenge closure workflow"
        )
    },
    {
        "id": "HU-09",
        "repo": "challenge",
        "service": "challenge",
        "title": "[CHALLENGE] HU-09: Open Opportunity Catalog Exploration",
        "statement": "As an authenticated student, I want to browse the catalog of open challenges and search by keywords, so that I can discover academic collaboration opportunities.",
        "rf": "RF19, RF21",
        "rb": "RB-05 (Hide direct contact details on catalog exploration)",
        "cu": "CU-05",
        "sprint": "Sprint 2",
        "points": 8,
        "priority": "Must Have",
        "assignees": "anorak,nelson",
        "acceptance_criteria": (
            "#### Scenario 1: Catalog Listing\n"
            "- **Given** an authenticated student viewing the catalog\n"
            "- **When** the catalog page loads\n"
            "- **Then** only challenges with status 'Open' are returned with summary cards.\n\n"
            "#### Scenario 2: Challenge Detail View\n"
            "- **Given** an open challenge in the catalog\n"
            "- **When** the student selects it\n"
            "- **Then** the full problem statement and requirements appear without company direct contact information."
        ),
        "checklist": (
            "- [ ] Create `/api/v1/challenges/catalog` endpoint with pagination in `challenge`\n"
            "- [ ] Implement detail view route `/api/v1/challenges/{id}/detail`\n"
            "- [ ] Ensure company private contacts are excluded from payload\n"
            "- [ ] Unit tests for catalog filtering by 'Open' status and pagination"
        )
    },
    {
        "id": "HU-10",
        "repo": "challenge",
        "service": "challenge",
        "title": "[CHALLENGE] HU-10: Reactive Multi-Criteria Filtering",
        "statement": "As an authenticated student, I want to filter challenges by knowledge area, skills, and industry sector, so that I can quickly pinpoint relevant challenges.",
        "rf": "RF20, RF22",
        "rb": "RB-05 (Explicit empty-state messaging when no matches occur)",
        "cu": "CU-05",
        "sprint": "Sprint 2",
        "points": 7,
        "priority": "Should Have",
        "assignees": "anorak,nelson",
        "acceptance_criteria": (
            "#### Scenario 1: Filter Matches\n"
            "- **Given** an active catalog with multiple challenges\n"
            "- **When** a student filters by 'Machine Learning' and 'Healthcare'\n"
            "- **Then** only matching open challenges are returned.\n\n"
            "#### Scenario 2: No Matching Challenges\n"
            "- **Given** search criteria yielding zero results\n"
            "- **When** query executes\n"
            "- **Then** the API returns an empty list with an explicit 'No matching challenges found' metadata."
        ),
        "checklist": (
            "- [ ] Add multi-param query filters (area, skills, sector) to catalog endpoint\n"
            "- [ ] Implement index-backed search queries in PostgreSQL\n"
            "- [ ] Unit tests for multi-filter combinations and empty-state responses"
        )
    },
    {
        "id": "HU-11",
        "repo": "application",
        "service": "application",
        "title": "[APPLICATION] HU-11: Submit Contact Application with Motivation Letter",
        "statement": "As an eligible student (semesters 6-10), I want to submit a contact application with a motivation letter to an open challenge, so that the company can evaluate my academic proposal.",
        "rf": "RF23, RF24, RF28",
        "rb": "RB-02 (Semester verification 6-10) & RB-03 (Single active application per challenge)",
        "cu": "CU-06",
        "sprint": "Sprint 3",
        "points": 8,
        "priority": "Must Have",
        "assignees": "anorak,juan",
        "acceptance_criteria": (
            "#### Scenario 1: Valid Application Submission\n"
            "- **Given** an eligible student in semester 6-10 with no active applications to this challenge\n"
            "- **When** they submit a motivation letter\n"
            "- **Then** the application is recorded in status 'Pending' in `db_applications`.\n\n"
            "#### Scenario 2: Duplicate Application Blocked\n"
            "- **Given** a student who already submitted an active application to a challenge\n"
            "- **When** they attempt to submit a second application to the same challenge\n"
            "- **Then** the system rejects it under rule RB-03.\n\n"
            "#### Scenario 3: Ineligible Student\n"
            "- **Given** a student in semester 1 to 5\n"
            "- **When** they attempt to submit an application\n"
            "- **Then** the system blocks the action citing semester ineligibility."
        ),
        "checklist": (
            "- [ ] Create `Application` Django model with unique constraint (student_id, challenge_id) in `application`\n"
            "- [ ] Add inter-service synchronous check to `profile` for semester validation\n"
            "- [ ] Create `/api/v1/applications/` endpoint\n"
            "- [ ] Emit `ApplicationCreated` event to event broker\n"
            "- [ ] Unit tests for submission, non-duplicity constraint, and semester validation"
        )
    },
    {
        "id": "HU-12",
        "repo": "application",
        "service": "application",
        "title": "[APPLICATION] HU-12: Company Evaluation and Atomic State Transition",
        "statement": "As a company, I want to review applications and accept (locking challenge to 'In Progress' and revealing contacts) or reject (requiring mandatory feedback), so that match decisions are formalized.",
        "rf": "RF25, RF26, RF27, RF31",
        "rb": "RB-04 (Atomic lock to 'In Progress') & RB-05 (Reciprocal contact reveal upon acceptance)",
        "cu": "CU-07",
        "sprint": "Sprint 3",
        "points": 10,
        "priority": "Must Have",
        "assignees": "anorak,juan",
        "acceptance_criteria": (
            "#### Scenario 1: Application Acceptance\n"
            "- **Given** an open challenge with pending applications\n"
            "- **When** the company accepts Student A's application\n"
            "- **Then** the challenge atomically transitions to 'In Progress', new applications are blocked, and direct contact details are revealed to both parties.\n\n"
            "#### Scenario 2: Application Rejection with Reason\n"
            "- **Given** a pending application\n"
            "- **When** the company rejects it with a mandatory explanation\n"
            "- **Then** status becomes 'Rejected', reason is saved, and challenge remains 'Open'.\n\n"
            "#### Scenario 3: Rejection without Reason Blocked\n"
            "- **Given** a rejection attempt without explanation text\n"
            "- **When** submitted\n"
            "- **Then** the action is rejected with validation error."
        ),
        "checklist": (
            "- [ ] Implement `accept` endpoint with atomic transaction and challenge lock in `application`\n"
            "- [ ] Implement `reject` endpoint requiring non-empty `feedback_reason`\n"
            "- [ ] Expose contact details conditionally only for accepted applications\n"
            "- [ ] Emit `ApplicationAccepted` and `ApplicationRejected` domain events\n"
            "- [ ] Unit tests covering race conditions, atomic lock, and mandatory rejection feedback"
        )
    },
    {
        "id": "HU-13",
        "repo": "notification",
        "service": "notification",
        "title": "[NOTIFICATION] HU-13: Asynchronous Domain Alerts and SMTP Emailing",
        "statement": "As a platform participant, I want to receive automated email notifications when applications are created or decided, so that I stay informed asynchronously.",
        "rf": "RF29, RF30",
        "rb": "RNF06 (SMTP fault tolerance and idempotent delivery)",
        "cu": "CU-08",
        "sprint": "Sprint 3",
        "points": 8,
        "priority": "Should Have",
        "assignees": "juan,nelson",
        "acceptance_criteria": (
            "#### Scenario 1: Application Created Notification\n"
            "- **Given** an `ApplicationCreated` event\n"
            "- **When** consumed by notification worker\n"
            "- **Then** a transactional email is dispatched to the company with application details.\n\n"
            "#### Scenario 2: Application Decision Notification\n"
            "- **Given** an `ApplicationAccepted` or `ApplicationRejected` event\n"
            "- **When** consumed\n"
            "- **Then** a notification is dispatched to the student with the outcome and feedback/contacts."
        ),
        "checklist": (
            "- [ ] Build event consumer in FastAPI/Worker service `notification`\n"
            "- [ ] Integrate Mailpit (local) / SMTP server with retry policy and idempotency\n"
            "- [ ] Create responsive HTML email templates for application events\n"
            "- [ ] Unit tests for event deserialization and email dispatch handling"
        )
    },
    {
        "id": "HU-14",
        "repo": "moderation",
        "service": "moderation",
        "title": "[MODERATION] HU-14: Platform Governance and Institutional Audit Log",
        "statement": "As an administrator, I want to supervise, suspend, or take down non-compliant challenges or accounts, and keep immutable audit logs, so that academic integrity is upheld.",
        "rf": "RF32",
        "rb": "RNF03 (Immutable audit logging)",
        "cu": "CU-09",
        "sprint": "Sprint 3",
        "points": 8,
        "priority": "Should Have",
        "assignees": "juan,nelson",
        "acceptance_criteria": (
            "#### Scenario 1: Challenge Suspension\n"
            "- **Given** a reported or non-compliant challenge\n"
            "- **When** the administrator suspends it via Django Admin\n"
            "- **Then** its status changes to 'Suspended', it is hidden from catalog, and an immutable log entry is generated.\n\n"
            "#### Scenario 2: Immutable Audit Log\n"
            "- **Given** any administrative action\n"
            "- **When** executed\n"
            "- **Then** user ID, target entity, timestamp, and justification are permanently recorded."
        ),
        "checklist": (
            "- [ ] Configure custom Django Admin interface in `moderation`\n"
            "- [ ] Create `AuditLog` model with append-only permissions\n"
            "- [ ] Implement inter-service suspension webhook/event to `challenge` and `auth`\n"
            "- [ ] Unit tests for admin action logging and suspension rules"
        )
    }
]


def build_markdown_body(us: dict) -> str:
    """Genera el cuerpo completo en Markdown estructurado para el issue."""
    assignees_formatted = " @" + " @".join(us["assignees"].split(","))
    return (
        f"### User Story Statement\n{us['statement']}\n\n"
        f"### Traceability\n"
        f"- **Service / Repo:** `{us['service']}`\n"
        f"- **Requirements:** {us['rf']}\n"
        f"- **Business Rules:** {us['rb']}\n"
        f"- **Use Case:** {us['cu']}\n"
        f"- **Sprint:** {us['sprint']}\n"
        f"- **Story Points:** {us['points']}\n"
        f"- **Priority:** {us['priority']}\n"
        f"- **Code Owners:** {assignees_formatted}\n\n"
        f"### Acceptance Criteria (Gherkin)\n{us['acceptance_criteria']}\n\n"
        f"### Technical Checklist\n{us['checklist']}"
    )


def ensure_csv_exists(filename: str):
    """Garantiza la existencia del CSV con todos los campos formateados."""
    if os.path.exists(filename):
        print(f"ℹ Archivo CSV detectado: '{filename}'")
        return

    print(f"📄 Generando '{filename}' con las 14 historias de usuario...")
    fieldnames = [
        "id", "repo", "service", "title", "statement", "rf", "rb", "cu",
        "sprint", "points", "priority", "assignees", "acceptance_criteria",
        "checklist", "body"
    ]
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for us in USER_STORIES:
            row = dict(us)
            row["body"] = build_markdown_body(us)
            writer.writerow(row)
    print(f"✔ '{filename}' generado exitosamente.")


def check_prerequisites():
    """Verifica que gh esté instalado y autenticado."""
    if not shutil.which("gh"):
        print("❌ Error: GitHub CLI ('gh') no está instalado en tu sistema.")
        print("   Instálalo desde: https://cli.github.com/")
        sys.exit(1)

    res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ Error: No has iniciado sesión en GitHub CLI.")
        print("   Ejecuta en tu terminal: gh auth login")
        sys.exit(1)


def ensure_label_exists(target_repo: str, label_name: str = "user-story"):
    """Crea la etiqueta en el repositorio de destino si aún no existe."""
    cmd_label = [
        "gh", "label", "create", label_name,
        "--repo", target_repo,
        "--color", "0E8A16",
        "--description", "User Story backlog item",
        "--force"
    ]
    subprocess.run(cmd_label, capture_output=True, text=True)


def main():
    check_prerequisites()

    csv_file = sys.argv[1] if len(sys.argv) > 1 else CSV_FILENAME
    ensure_csv_exists(csv_file)

    print("\n" + "=" * 80)
    print("🚀 IMPORTADOR DE HISTORIAS DE USUARIO A GITHUB PROJECTS")
    print(f"   Organización:       {ORG}")
    print(f"   Proyecto:           #{PROJECT_NUM} ({PROJECT_TITLE})")
    print(f"   URL del Proyecto:   https://github.com/orgs/{ORG}/projects/{PROJECT_NUM}")
    print(f"   Archivo Origen:     {csv_file}")
    print("=" * 80 + "\n")

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        stories = list(reader)

    total = len(stories)
    success = 0
    failed = 0

    for idx, row in enumerate(stories, start=1):
        hu_id = row.get("id", "")
        repo = row.get("repo", "")
        title = row.get("title", "")
        body = row.get("body", "")
        points = row.get("points", "")
        sprint = row.get("sprint", "")
        priority = row.get("priority", "")
        target_repo = f"{ORG}/{repo}"

        print(f"[{idx}/{total}] Procesando {hu_id} ➔ {target_repo}")
        print(f"    Título: {title}")
        print(f"    Estimación: {points} PH | {sprint} | {priority}")

        # 1. Asegurar que el label 'user-story' exista en el repositorio
        ensure_label_exists(target_repo, "user-story")

        # 2. Intentar crear el Issue con la etiqueta
        cmd_create = [
            "gh", "issue", "create",
            "--repo", target_repo,
            "--title", title,
            "--body", body,
            "--label", "user-story"
        ]

        res = subprocess.run(cmd_create, capture_output=True, text=True)

        # Fallback: Si falló específicamente por el label, reintentar sin el label
        if res.returncode != 0 and "label" in res.stderr.lower():
            cmd_create_fallback = [
                "gh", "issue", "create",
                "--repo", target_repo,
                "--title", title,
                "--body", body
            ]
            res = subprocess.run(cmd_create_fallback, capture_output=True, text=True)

        if res.returncode != 0:
            print(f"    ❌ Error al crear issue: {res.stderr.strip()}")
            failed += 1
            print("-" * 70)
            continue

        issue_url = res.stdout.strip()
        print(f"    ✔ Issue creado: {issue_url}")

        # 3. Asociar el issue directamente al proyecto organizacional #2
        cmd_link = [
            "gh", "project", "item-add", PROJECT_NUM,
            "--owner", ORG,
            "--url", issue_url
        ]

        res_link = subprocess.run(cmd_link, capture_output=True, text=True)
        if res_link.returncode == 0:
            print(f"    ✔ Enlazado exitosamente al Proyecto #{PROJECT_NUM}")
            success += 1
        else:
            print(f"    ⚠️ Aviso al enlazar con el proyecto: {res_link.stderr.strip()}")
            success += 1

        print("-" * 70)
        time.sleep(1)  # Pausa breve preventiva contra rate-limits de la API

    print("\n" + "=" * 80)
    print(f"🎉 Proceso finalizado: {success}/{total} historias registradas correctamente.")
    if failed > 0:
        print(f"⚠️ {failed} historias fallaron. Verifica la existencia de los repositorios.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
