#!/usr/bin/env python3
"""
Conecta Nexus - Sprint 3 Full Technical Tasks Generator
Decomposes Sprint 3 User Stories (HU-11 to HU-14) and Reopened Sprint 2 Frontend tasks
into 39 granular engineering tasks across the microservice ecosystem:
- 10 Reopened Frontend tasks from Sprint 2 (hardened with explicit visual/interaction acceptance criteria)
- 8 Application backend tasks ('application')
- 5 Notification backend tasks ('notification')
- 5 Moderation backend tasks ('moderation')
- 6 New Frontend tasks ('frontend')
- 2 Gateway tasks ('gateway')
- 3 Infrastructure tasks ('infra')

Equitably distributed (exactly 13 tasks each) among the 3 developers:
@juandiegosb, @NelsonConde, and @AnorakTeam.
"""

import os
import csv

TASKS = [
    # =========================================================================
    # REOPENED SPRINT 2 FRONTEND TASKS (10 Tasks - Quality Hardening)
    # =========================================================================
    {
        "task_id": "FRONTEND-TASK-01-R",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-06",
        "parent_issue_number": "1",
        "title": "[FRONTEND-TASK-01-R] Reopen: Harden Challenge TypeScript Interfaces & useChallenges Composable",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,reopened,frontend",
        "objective": "Reopen and harden the core TypeScript domain models and the reactive useChallenges composable to support robust state management, query caching, attachment metadata, and optimistic updates.",
        "specs": (
            "- Framework: Nuxt 4 (Vue 3 Composition API, TypeScript 5.x)\n"
            "- Target Files:\n"
            "  * app/types/challenge.ts\n"
            "  * app/composables/useChallenges.ts\n"
            "- Interfaces to strictly enforce:\n"
            "  * Challenge (id, title, description, business_process, status, difficulty_level, modality, min_semester, attachments)\n"
            "  * ChallengeCreateInput, ChallengeUpdateInput, ChallengeFilterParams\n"
            "  * AttachmentMetadata (id, file_name, file_size_bytes, mime_type, download_url)\n"
            "- Composable API: fetchCatalog(), fetchChallengeById(), createChallenge(), publishChallenge(), closeChallenge(), uploadAttachment(), deleteAttachment()"
        ),
        "acceptance_criteria": (
            "- **Type Safety & Strict Validation:** All API request payloads and response envelopes must be strictly typed without any `any` or loose casts.\n"
            "- **Optimistic Updates & Cache Invalidation:** Calling `publishChallenge` or `closeChallenge` must reactively update local component state and invalidate cached catalog queries without requiring a full page reload.\n"
            "- **Error Normalization:** Composable must parse 400/403/404/409/422 responses from FastAPI/Nginx and return user-friendly localized error strings (e.g. extracting `detail` from JSON envelope).\n"
            "- **Loading & Error Reactivity:** Every asynchronous action exposes reactive `pending: Ref<boolean>` and `error: Ref<Error | null>` states."
        ),
        "deliverables": (
            "- [ ] Refactor app/types/challenge.ts with complete domain models and attachment types\n"
            "- [ ] Harden app/composables/useChallenges.ts with error handling and reactive state\n"
            "- [ ] Add Vitest unit tests in tests/composables/useChallenges.spec.ts\n"
            "- [ ] Code passes pnpm lint and vue-tsc type checking"
        ),
        "verification": "cd frontend && pnpm test tests/composables/useChallenges.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-02-R",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-06",
        "parent_issue_number": "1",
        "title": "[FRONTEND-TASK-02-R] Reopen: Redesign Company Challenge Creation Page (/challenges/new)",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,reopened,frontend",
        "objective": "Reopen and completely overhaul the Challenge Creation Page (/challenges/new) with strict field validations, interactive chips, live character counters, and explicit error states.",
        "specs": (
            "- Route: /challenges/new\n"
            "- Role Guard: Restricted strictly to COMPANY role via client-side middleware\n"
            "- Component: app/pages/challenges/new.vue\n"
            "- Form Fields: Title (min 10 chars), Business Process (min 5 chars), Description (markdown/rich-text, min 30 chars), Difficulty Level (BEGINNER, INTERMEDIATE, ADVANCED), Modality (REMOTE, PRESENTIAL, HYBRID), Minimum Semester (6 to 10 slider/select), Knowledge Areas (chips), Required Skills (chips)\n"
            "- Actions: 'Save Draft' (POST /api/v1/challenges/) and 'Publish Immediately' (POST + POST /publish)"
        ),
        "acceptance_criteria": (
            "- **Visual Layout & Hierarchy:** Clean 2-column desktop layout (left: main fields & description, right: requirements card & action panel). Mobile renders as a single stacked column with sticky bottom action bar.\n"
            "- **Real-time Field Validation:** Dirty fields must display instant visual red border (`border-red-500`) and inline explanatory error text beneath the input upon blur.\n"
            "- **Live Character Counter:** Description textarea must show a dynamic counter (`Current: X / 30 min characters`) turning green when requirement is satisfied.\n"
            "- **Tag Chips Input:** Skills and knowledge areas must support typing a term, pressing 'Enter' or ',' to convert to a removable pill chip, with duplicate tag prevention.\n"
            "- **Button States:** 'Publish Challenge' button is disabled with an explanatory tooltip until all required fields pass validation. On submit, shows an animated loading spinner."
        ),
        "deliverables": (
            "- [ ] Overhaul app/pages/challenges/new.vue with complete UI and validation state\n"
            "- [ ] Implement skills/knowledge tag chips input with removal icons\n"
            "- [ ] Add visual validation feedback and disabled button logic\n"
            "- [ ] Add Vitest unit test in tests/pages/challenges/new.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/pages/challenges/new.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-03-R",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-07",
        "parent_issue_number": "2",
        "title": "[FRONTEND-TASK-03-R] Reopen: Redesign Drag-and-Drop Attachment Uploader (AttachmentUploader.vue)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,reopened,frontend",
        "objective": "Reopen and rebuild the AttachmentUploader component with an interactive drag-and-drop zone, client-side MIME & 10MB limit enforcement, animated progress indicators, and visual error banners.",
        "specs": (
            "- Component: app/components/challenges/AttachmentUploader.vue\n"
            "- Allowed Formats: application/pdf, image/png, image/jpeg\n"
            "- Size Limit: Maximum 10MB (10,485,760 bytes)\n"
            "- Props: challengeId (UUID), disabled (boolean)\n"
            "- Events: @uploaded(attachment), @error(message)"
        ),
        "acceptance_criteria": (
            "- **Visual Drop Zone:** Dashed border box with upload cloud icon. When a file is dragged over the component, the background changes to primary light tone (`bg-primary-50`) with an animated pulsing border.\n"
            "- **Client-Side Validation Feedback:** Attempting to drop a file > 10MB or an invalid extension (.exe, .zip) must immediately trigger a prominent warning banner with an error icon, blocking the upload before any network request.\n"
            "- **Individual Progress Bar:** While uploading, the selected file is displayed in a preview card with filename, size in MB, and a smooth percentage progress bar (0% -> 100%).\n"
            "- **Success & Reset State:** Upon HTTP 201 response, a green checkmark appears with a 'File uploaded successfully' toast, and the drop zone resets to idle state."
        ),
        "deliverables": (
            "- [ ] Rebuild app/components/challenges/AttachmentUploader.vue with drag-and-drop\n"
            "- [ ] Implement client-side size and MIME type guards with visual error alerts\n"
            "- [ ] Add smooth progress bar animation and success reset\n"
            "- [ ] Vitest unit tests in tests/components/challenges/AttachmentUploader.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/components/challenges/AttachmentUploader.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-04-R",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-07",
        "parent_issue_number": "2",
        "title": "[FRONTEND-TASK-04-R] Reopen: Redesign Attachment List & Ephemeral Preview (AttachmentList.vue)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,reopened,frontend",
        "objective": "Reopen and refine AttachmentList.vue to render file format badges, human-readable file sizes, signed download openers, and owner deletion confirmations.",
        "specs": (
            "- Component: app/components/challenges/AttachmentList.vue\n"
            "- Props: attachments (AttachmentMetadata[]), isOwner (boolean), challengeId (UUID)\n"
            "- Target Icons: PDF (red document icon), Images (blue picture icon), Generic (gray file icon)\n"
            "- Actions: Download (opens signed URL in new tab), Delete (owner only, calls DELETE endpoint)"
        ),
        "acceptance_criteria": (
            "- **Visual Format Badges:** Each attachment item card displays an explicit icon/badge: red for PDF, blue for PNG/JPEG, alongside the truncated file name and human-formatted size (e.g., '3.2 MB').\n"
            "- **Download Experience:** Clicking the download button triggers a browser download or opens the signed MinIO/GCS URL in a new tab without altering the current route.\n"
            "- **Deletion Confirmation Dialog:** Clicking the trash icon opens a confirmation popover ('Are you sure you want to delete this file? This action cannot be undone') before emitting or calling the delete API.\n"
            "- **Empty State:** When attachments array is empty, renders a clean muted placeholder ('No technical attachments uploaded yet')."
        ),
        "deliverables": (
            "- [ ] Refactor app/components/challenges/AttachmentList.vue with icons and format pills\n"
            "- [ ] Implement deletion confirmation dialog popover\n"
            "- [ ] Handle signed URL download trigger without page disruption\n"
            "- [ ] Vitest test suite in tests/components/challenges/AttachmentList.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/components/challenges/AttachmentList.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-05-R",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-08",
        "parent_issue_number": "3",
        "title": "[FRONTEND-TASK-05-R] Reopen: Overhaul Company Challenge Management Dashboard (/challenges/manage)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,reopened,frontend",
        "objective": "Reopen and redesign the Company Challenge Management Portfolio (/challenges/manage) with status filter tabs, metric cards, action menus, and empty state CTA.",
        "specs": (
            "- Route: /challenges/manage\n"
            "- Role Guard: COMPANY only\n"
            "- Metric Counters: Total Challenges, Active/Open, In Progress, Closed\n"
            "- Status Tabs: All, Open, Draft, In Progress, Closed\n"
            "- Actions per row: View Details, Edit (if Draft/Open), Publish (if Draft), Voluntary Close (if Open)"
        ),
        "acceptance_criteria": (
            "- **Overview Metric Cards:** Top grid featuring 4 stat cards with icons, total counts, and subtle background accent colors.\n"
            "- **Status Tabs with Badges:** Tab bar allowing instant client-side switching between statuses. Each tab displays a numeric badge counter (e.g. 'Open (4)').\n"
            "- **Responsive Table:** Clean table on desktop displaying Title, Created Date, Semester Requirement, Applications Count, and Status Pill (Green for Open, Yellow for Draft, Blue for In Progress, Gray for Closed). Mobile view collapses rows into cards.\n"
            "- **Row Action Menu:** Three-dot dropdown menu providing contextual actions based on status (e.g. 'Publish' only visible for Draft; 'Close Challenge' only for Open).\n"
            "- **Zero-State CTA:** When the selected tab contains zero challenges, displays an empty state banner with a direct 'Create Your First Challenge' primary button."
        ),
        "deliverables": (
            "- [ ] Overhaul app/pages/challenges/manage.vue with tabbed navigation and stat cards\n"
            "- [ ] Implement CompanyChallengeTable.vue with contextual action dropdowns\n"
            "- [ ] Add responsive mobile card view alternative\n"
            "- [ ] Vitest test suite in tests/pages/challenges/manage.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/pages/challenges/manage.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-06-R",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-08",
        "parent_issue_number": "3",
        "title": "[FRONTEND-TASK-06-R] Reopen: Redesign Voluntary Closure Modal with Strict Guard (ChallengeClosureModal.vue)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,reopened,frontend",
        "objective": "Reopen and harden ChallengeClosureModal.vue with accessible dialog trapping, prominent warning banner, dynamic 15-character counter, and disabled confirm button.",
        "specs": (
            "- Component: app/components/challenges/ChallengeClosureModal.vue\n"
            "- Props: isOpen (boolean), challengeId (UUID), challengeTitle (string)\n"
            "- Business Rule: Closure reason mandatory with at least 15 characters (HU-08)\n"
            "- Target Endpoint: POST /api/v1/challenges/{id}/close"
        ),
        "acceptance_criteria": (
            "- **Visual Warning Banner:** Prominent yellow/amber warning box inside the modal explaining: 'Voluntary closure will immediately remove this challenge from the public catalog and freeze active applications.'\n"
            "- **Interactive Character Counter:** Textarea displays a live counter at the bottom-right corner: `X / 15 characters minimum`. Numbers turn red when X < 15 and green when X >= 15.\n"
            "- **Strict Button Guard:** 'Confirm Voluntary Closure' button is disabled (opacity 50%, cursor not-allowed) as long as input length < 15 characters.\n"
            "- **Submission Feedback:** On click, button displays a loading spinner. Upon successful close, modal dismisses, emits `@closed`, and triggers a success toast notification."
        ),
        "deliverables": (
            "- [ ] Harden app/components/challenges/ChallengeClosureModal.vue with character counter\n"
            "- [ ] Enforce strict 15-character disabling guard on confirm button\n"
            "- [ ] Integrate warning banner and loading state\n"
            "- [ ] Vitest unit test in tests/components/challenges/ChallengeClosureModal.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/components/challenges/ChallengeClosureModal.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-07-R",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-09",
        "parent_issue_number": "4",
        "title": "[FRONTEND-TASK-07-R] Reopen: Redesign Opportunity Catalog Grid & Discovery Cards (/challenges)",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,reopened,frontend",
        "objective": "Reopen and modernize the Opportunity Catalog Grid (/challenges) and ChallengeCard component with skeleton loading states, badges, hover lift effects, and pagination.",
        "specs": (
            "- Route: /challenges\n"
            "- Components:\n"
            "  * app/pages/challenges/index.vue\n"
            "  * app/components/challenges/ChallengeCard.vue\n"
            "- Card Metadata: Title, Company Name, Modality (Badge), Difficulty (Badge), Semester (Pill: 'Sem. 6+'), Skills (Chips), Description Snippet (clamped to 3 lines)\n"
            "- Responsive Grid: 1 column on mobile (< 640px), 2 columns on tablet (640-1024px), 3 columns on desktop (> 1024px)"
        ),
        "acceptance_criteria": (
            "- **Skeleton Loading State:** While fetching catalog items, renders 6 animated skeleton cards with shimmering gray placeholders matching the card layout.\n"
            "- **Visual Discovery Cards:** Clean white card with subtle border and shadow. On hover, smooth lift transition (`translate-y--1` and shadow enlargement).\n"
            "- **Badge Indicators:** Color-coded badges for Modality (Blue: Remote, Purple: Hybrid, Orange: Presential) and Difficulty (Green: Beginner, Amber: Intermediate, Red: Advanced).\n"
            "- **Pagination Bar:** Centered pagination controls at the bottom displaying active page, total pages, and next/prev arrows with automatic smooth scroll to top on page change."
        ),
        "deliverables": (
            "- [ ] Redesign app/components/challenges/ChallengeCard.vue with badges and hover lift\n"
            "- [ ] Implement skeleton card loading states in app/pages/challenges/index.vue\n"
            "- [ ] Add responsive grid layout and bottom pagination bar\n"
            "- [ ] Vitest unit tests in tests/pages/challenges/index.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/pages/challenges/index.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-08-R",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-09",
        "parent_issue_number": "4",
        "title": "[FRONTEND-TASK-08-R] Reopen: Redesign Public Challenge Detail Page with Masked Contacts (/challenges/[id])",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,reopened,frontend",
        "objective": "Reopen and elevate the Public Challenge Detail View (/challenges/[id]) with hero header, masked contact notice, technical attachments section, and sticky application CTA.",
        "specs": (
            "- Route: /challenges/[id]\n"
            "- Component: app/pages/challenges/[id].vue\n"
            "- Sections:\n"
            "  1. Hero Header (Title, Economic Sector, Status Badge, Published Date)\n"
            "  2. Problem Statement (Formatted rich text / markdown)\n"
            "  3. Requirements Sidebar (Min Semester, Modality, Required Skills Chips)\n"
            "  4. Technical Attachments (Downloadable files via AttachmentList.vue)\n"
            "  5. Contact Privacy Card (Explicit notice: corporate contacts revealed upon application acceptance)\n"
            "  6. Application CTA button"
        ),
        "acceptance_criteria": (
            "- **Hero & Sidebar Layout:** Two-column desktop layout (70% content left, 30% sticky metadata sidebar right). On mobile, collapses to single column with sticky bottom 'Apply' button.\n"
            "- **Contact Masking Notice:** A distinct info card displaying a lock icon and explanatory text: 'Corporate contact details are protected under Law 1581 and will be revealed mutually once the company accepts your academic application.'\n"
            "- **Role-Aware Application CTA:** For authenticated students (Semesters 6-10), 'Apply to Challenge' is prominent primary button. For unauthenticated visitors, redirects to login. For companies, button is disabled with tooltip: 'Only students can apply to challenges.'\n"
            "- **404 / Non-Open Handling:** If challenge does not exist or status is not OPEN, page renders a clean 'Opportunity Not Available' card with link back to catalog."
        ),
        "deliverables": (
            "- [ ] Overhaul app/pages/challenges/[id].vue with hero header and 2-column layout\n"
            "- [ ] Integrate privacy-masked contact notice and AttachmentList.vue\n"
            "- [ ] Add role-aware 'Apply' CTA button triggering application flow\n"
            "- [ ] Vitest test suite in tests/pages/challenges/detail.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/pages/challenges/detail.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-09-R",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-10",
        "parent_issue_number": "5",
        "title": "[FRONTEND-TASK-09-R] Reopen: Polish Reactive Catalog Filter Bar with URL Sync (CatalogFilterBar.vue)",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,reopened,frontend",
        "objective": "Reopen and enhance CatalogFilterBar.vue with debounced search input, multi-select dropdowns, active filter pill badges, and bidirectional URL query synchronization.",
        "specs": (
            "- Component: app/components/challenges/CatalogFilterBar.vue\n"
            "- Filters Supported: Keyword search (q), Modality (REMOTE, PRESENTIAL, HYBRID), Difficulty Level, Economic Sector, Minimum Semester\n"
            "- Query Sync: Bi-directional synchronization with `useRoute().query` and `router.push()`\n"
            "- Debounce: 300ms on text search input to prevent query hammering"
        ),
        "acceptance_criteria": (
            "- **Visual Filter Bar:** Top horizontal bar containing search input with search icon on the left and clear 'x' icon on the right when text is present, followed by select dropdowns.\n"
            "- **Active Filter Pills:** When filters are active, a secondary row renders pill chips showing active selections (e.g., `Modality: Remote ×`) with one-click individual removal.\n"
            "- **Bidirectional URL Query Sync:** Selecting a filter instantly updates browser URL (e.g. `?modality=REMOTE&q=data`) without reloading the page, enabling bookmarking and browser back/forward navigation.\n"
            "- **Debounce Behavior:** Typing in the search input waits 300ms of user inactivity before emitting query update or modifying URL."
        ),
        "deliverables": (
            "- [ ] Refactor app/components/challenges/CatalogFilterBar.vue with debounced search and URL sync\n"
            "- [ ] Add active filter pill chips with single-click removal icons\n"
            "- [ ] Ensure responsive mobile drawer/collapsible filter layout\n"
            "- [ ] Vitest test suite in tests/components/challenges/CatalogFilterBar.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/components/challenges/CatalogFilterBar.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-10-R",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-10",
        "parent_issue_number": "5",
        "title": "[FRONTEND-TASK-10-R] Reopen: Enhance Catalog Empty-State View & Reset Action (CatalogEmptyState.vue)",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,reopened,frontend",
        "objective": "Reopen and upgrade CatalogEmptyState.vue to render an engaging zero-results illustration, contextual guidance based on active filters, and a single-click reset action.",
        "specs": (
            "- Component: app/components/challenges/CatalogEmptyState.vue\n"
            "- Props: activeFilters (Record<string, any>), totalActiveCount (number)\n"
            "- Events: @reset\n"
            "- Business Rule: HU-10 structured empty state feedback"
        ),
        "acceptance_criteria": (
            "- **Visual Empty State Illustration:** Centered clean SVG illustration or magnifying glass icon with subtle muted colors, heading: 'No challenges match your search criteria'.\n"
            "- **Contextual Feedback:** Explanatory copy dynamically listing active filters (e.g. 'We could not find opportunities matching Sector: Software and Modality: Presential').\n"
            "- **Single-Click Reset Action:** Prominent primary button: 'Clear All Filters' that resets all query params and reloads the full catalog.\n"
            "- **Secondary Action Link:** Secondary outline button or link: 'Explore all open opportunities' that clears filters and focuses on page 1."
        ),
        "deliverables": (
            "- [ ] Upgrade app/components/challenges/CatalogEmptyState.vue with graphic and dynamic feedback\n"
            "- [ ] Add 'Clear All Filters' action resetting URL query params\n"
            "- [ ] Vitest test suite in tests/components/challenges/CatalogEmptyState.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/components/challenges/CatalogEmptyState.spec.ts"
    },

    # =========================================================================
    # HU-11: Submit Contact Application with Motivation Letter (8 pts - Must Have)
    # =========================================================================
    {
        "task_id": "APPLICATION-TASK-01",
        "repo": "application",
        "service": "application",
        "parent_story": "HU-11",
        "parent_issue_number": "6",
        "title": "[APPLICATION-TASK-01] Application Database Model, PostgreSQL Constraints & Migrations",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,application",
        "objective": "Implement the core Application Django ORM model in db_applications with unique compound constraint (student_id, challenge_id) enforcing RB-03, status enum, and motivation letter.",
        "specs": (
            "- Database: PostgreSQL 16 (db_applications)\n"
            "- Model: Application (apps/applications/models.py)\n"
            "- Fields: id (UUID PK), student_id (UUID), challenge_id (UUID), motivation_letter (TextField, min 20 chars), status (PENDING, ACCEPTED, REJECTED, CANCELLED), feedback_reason (TextField nullable), created_at, updated_at\n"
            "- Constraints: UniqueConstraint(fields=['student_id', 'challenge_id'], name='unique_student_challenge_application') enforcing RB-03"
        ),
        "acceptance_criteria": (
            "- **Database Migration:** Django migration runs cleanly on PostgreSQL creating `applications_application` table.\n"
            "- **RB-03 Non-Duplicity Guarantee:** Attempting to insert a record with identical `(student_id, challenge_id)` raises IntegrityError at database level.\n"
            "- **Default Status:** New applications default strictly to 'PENDING'.\n"
            "- **Indexes:** B-Tree indexes on `student_id`, `challenge_id`, and `status` for fast lookup."
        ),
        "deliverables": (
            "- [ ] Create Application model in apps/applications/models.py\n"
            "- [ ] Generate and execute Django migrations\n"
            "- [ ] Unit tests verifying table creation and unique constraint"
        ),
        "verification": "podman exec conecta-application python manage.py migrate"
    },
    {
        "task_id": "APPLICATION-TASK-02",
        "repo": "application",
        "service": "application",
        "parent_story": "HU-11",
        "parent_issue_number": "6",
        "title": "[APPLICATION-TASK-02] Inter-Service Synchronous Verification Clients (Profile & Challenge)",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,application",
        "objective": "Build and verify robust synchronous HTTP clients in Application service to validate student eligibility & consent against Profile service, and open status against Challenge public catalog.",
        "specs": (
            "- Target Files:\n"
            "  * apps/applications/clients/profile_client.py\n"
            "  * apps/applications/clients/challenge_client.py\n"
            "- Profile Client: GET /api/v1/profiles/internal/{user_id}/eligibility (validates is_eligible, current_semester >= 6, has_consent=True)\n"
            "- Challenge Client: GET /api/v1/challenges/catalog/{challenge_id} (validates existence and status == 'OPEN')\n"
            "- Timeout & Retries: 3.0s timeout with connection pool limits"
        ),
        "acceptance_criteria": (
            "- **Challenge Validation:** Validates challenge is strictly OPEN via catalog endpoint; translates 404 to ChallengeNotFoundError and non-open status to ChallengeNotOpenError.\n"
            "- **Profile Eligibility Validation:** Confirms semester between 6 and 10 (RB-02) and Habeas Data consent (RB-02); raises StudentNotEligibleError or ConsentMissingError on violation.\n"
            "- **Fault Tolerance:** Catches httpx.ConnectError / ReadTimeout and cleanly raises ChallengeServiceUnavailableError / ProfileServiceUnavailableError mapping to HTTP 502."
        ),
        "deliverables": (
            "- [ ] Implement and harden ChallengeServiceClient in apps/applications/clients/challenge_client.py\n"
            "- [ ] Implement and harden ProfileServiceClient in apps/applications/clients/profile_client.py\n"
            "- [ ] Pytest integration suite with respx mocks in apps/applications/tests/test_challenge_client.py & test_profile_client.py"
        ),
        "verification": "podman exec conecta-application uv run pytest apps/applications/tests/test_challenge_client.py apps/applications/tests/test_profile_client.py"
    },
    {
        "task_id": "APPLICATION-TASK-03",
        "repo": "application",
        "service": "application",
        "parent_story": "HU-11",
        "parent_issue_number": "6",
        "title": "[APPLICATION-TASK-03] Student Application Submission REST Endpoint (POST /api/v1/applications/)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,application",
        "objective": "Expose and secure the application submission endpoint enforcing RBAC (STUDENT only), non-duplicity fast check, inter-service validations, and atomic persistence.",
        "specs": (
            "- Endpoint: POST /api/v1/applications/\n"
            "- Permissions: IsAuthenticated, require_role('STUDENT')\n"
            "- Request Body: { challenge_id: UUID, motivation_letter: string (20-2000 chars) }\n"
            "- Response: HTTP 201 Created with Application details\n"
            "- Errors: 400 Bad Request (ineligible / no consent), 404 Not Found (challenge missing), 409 Conflict (duplicate application RB-03), 422 Unprocessable (challenge not open), 502 Bad Gateway (upstream failure)"
        ),
        "acceptance_criteria": (
            "- **RBAC Authorization:** Only authenticated users with role STUDENT can submit; COMPANY role returns HTTP 403 Forbidden.\n"
            "- **Duplicate Rejection (RB-03):** Immediate 409 Conflict if application exists for student + challenge.\n"
            "- **Validation Pipeline:** Sequentially checks duplicity -> challenge open status -> profile semester & consent -> persists application in db.\n"
            "- **HTTP Response:** Returns 201 Created with application UUID, initial status 'PENDING', and timestamps."
        ),
        "deliverables": (
            "- [ ] Implement ApplicationCreateView in apps/applications/views.py\n"
            "- [ ] Register URL routing in apps/applications/urls.py\n"
            "- [ ] Pytest test cases in apps/applications/tests/test_views.py"
        ),
        "verification": "podman exec conecta-application uv run pytest apps/applications/tests/test_views.py"
    },
    {
        "task_id": "APPLICATION-TASK-04",
        "repo": "application",
        "service": "application",
        "parent_story": "HU-11",
        "parent_issue_number": "6",
        "title": "[APPLICATION-TASK-04] Student Applications Consultation Endpoints (GET /me/ & GET /{id}/)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,application",
        "objective": "Create endpoints allowing students to inspect their own application history, view status updates (Pending, Accepted, Rejected), and read company feedback.",
        "specs": (
            "- Endpoints:\n"
            "  * GET /api/v1/applications/me/ (paginated list of owned applications)\n"
            "  * GET /api/v1/applications/{id}/ (detailed view with feedback or revealed company contacts if accepted)\n"
            "- Permissions: IsAuthenticated, Student owner guard"
        ),
        "acceptance_criteria": (
            "- **Student Portfolio Query:** Returns only applications where `student_id == request.user.id` ordered by `created_at DESC`.\n"
            "- **Owner Verification:** Querying an application ID owned by another student returns HTTP 404/403.\n"
            "- **Conditional Field Projection:** If status is 'ACCEPTED', includes company contact details; if status is 'REJECTED', includes `feedback_reason`."
        ),
        "deliverables": (
            "- [ ] Implement StudentApplicationListView and StudentApplicationDetailView\n"
            "- [ ] Add serializer projecting conditional feedback and contact fields\n"
            "- [ ] Pytest unit tests verifying student isolation and data projection"
        ),
        "verification": "podman exec conecta-application uv run pytest -k 'student_applications'"
    },
    {
        "task_id": "FRONTEND-TASK-11",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-11",
        "parent_issue_number": "6",
        "title": "[FRONTEND-TASK-11] Student Application Submission Modal & Motivation Letter Form",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,frontend",
        "objective": "Develop the ApplicationSubmissionModal component enabling eligible students to compose and submit their motivation letter with character limits and confirmation.",
        "specs": (
            "- Component: app/components/applications/ApplicationSubmissionModal.vue\n"
            "- Props: isOpen (boolean), challenge (Challenge)\n"
            "- Form Input: motivationLetter (textarea, 20 to 2000 characters)\n"
            "- API: POST /api/v1/applications/"
        ),
        "acceptance_criteria": (
            "- **Visual Layout & Dialog:** Accessible modal with clear header: 'Apply to [Challenge Title]'. Displays student academic reminder badge ('Applying as Semester X Student').\n"
            "- **Dynamic Character Counter:** Textarea shows live character counter (`X / 20 min characters`). Warning border appears if under 20 chars.\n"
            "- **Submit Action & Spinner:** 'Submit Academic Proposal' button disabled until letter >= 20 chars. Shows spinner while submitting.\n"
            "- **Success Experience:** On HTTP 201, closes modal, shows green celebration toast, and marks challenge page with an 'Applied' badge."
        ),
        "deliverables": (
            "- [ ] Build app/components/applications/ApplicationSubmissionModal.vue\n"
            "- [ ] Add motivation letter validation and character counter\n"
            "- [ ] Vitest unit tests in tests/components/applications/ApplicationSubmissionModal.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/components/applications/ApplicationSubmissionModal.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-12",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-11",
        "parent_issue_number": "6",
        "title": "[FRONTEND-TASK-12] Student Applications Portfolio Page (/applications)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,frontend",
        "objective": "Create the Student Applications Management Page (/applications) allowing students to track active and past applications, check match statuses, and view feedback.",
        "specs": (
            "- Route: /applications\n"
            "- Role Guard: STUDENT only\n"
            "- Filter Tabs: All, Pending, Accepted, Rejected\n"
            "- Card Elements: Challenge Title, Company Name, Applied Date, Status Badge, Feedback Expander"
        ),
        "acceptance_criteria": (
            "- **Visual Application Cards:** Grid of cards featuring status pills (Yellow: Pending, Green: Accepted, Red: Rejected).\n"
            "- **Accepted Match Card:** For accepted applications, displays an highlighted green card showing company contacts (email, phone, contact person) with click-to-email and click-to-call actions.\n"
            "- **Rejection Feedback Card:** For rejected applications, displays an expandable feedback alert detailing the company's reason.\n"
            "- **Empty State:** If student has 0 applications in the selected tab, renders a friendly illustration with a 'Browse Open Opportunities' CTA button."
        ),
        "deliverables": (
            "- [ ] Create app/pages/applications/index.vue\n"
            "- [ ] Implement status tabs and responsive card grid\n"
            "- [ ] Add accepted contact cards and rejection reason expander\n"
            "- [ ] Vitest unit tests in tests/pages/applications/index.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/pages/applications/index.spec.ts"
    },

    # =========================================================================
    # HU-12: Company Evaluation and Atomic State Transition (10 pts - Must Have)
    # =========================================================================
    {
        "task_id": "APPLICATION-TASK-05",
        "repo": "application",
        "service": "application",
        "parent_story": "HU-12",
        "parent_issue_number": "7",
        "title": "[APPLICATION-TASK-05] Company Challenge Applications Listing & Detail Endpoints (GET /challenge/{id}/)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,application",
        "objective": "Expose endpoints for companies to list and review all student applications submitted to their owned challenges, integrating public student academic profiles.",
        "specs": (
            "- Endpoints:\n"
            "  * GET /api/v1/applications/challenge/{challenge_id}/ (lists applications for a challenge)\n"
            "  * GET /api/v1/applications/{id}/review/ (detailed view for company)\n"
            "- Permissions: COMPANY role with challenge ownership verification"
        ),
        "acceptance_criteria": (
            "- **Company Ownership Verification:** Endpoint verifies that `request.user.id` is the owner of the challenge before returning candidates.\n"
            "- **Candidate Profile Projection:** Returns candidate's current semester, knowledge areas, skills, and motivation letter without private phone/email until accepted.\n"
            "- **Sorting & Status Filtering:** Allows filtering by status (PENDING, ACCEPTED, REJECTED) with default sort by `created_at ASC`."
        ),
        "deliverables": (
            "- [ ] Implement CompanyApplicationListView in apps/applications/views.py\n"
            "- [ ] Integrate Profile service public student profile lookup\n"
            "- [ ] Pytest integration tests verifying ownership checks"
        ),
        "verification": "podman exec conecta-application uv run pytest -k 'company_applications'"
    },
    {
        "task_id": "APPLICATION-TASK-06",
        "repo": "application",
        "service": "application",
        "parent_story": "HU-12",
        "parent_issue_number": "7",
        "title": "[APPLICATION-TASK-06] Atomic Application Acceptance & Challenge Locking State Machine (RB-04, RB-05)",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,application",
        "objective": "Implement the atomic match transaction in Application service: accepting an application transitions status to ACCEPTED, locks the parent challenge to IN_PROGRESS (RB-04), and reveals reciprocal contacts (RB-05).",
        "specs": (
            "- Endpoint: POST /api/v1/applications/{id}/accept/\n"
            "- Permissions: COMPANY role, Challenge Owner\n"
            "- Business Rules:\n"
            "  * RB-04: Atomic lock - challenge status switches to IN_PROGRESS; blocks any other applications.\n"
            "  * RB-05: Reciprocal contact reveal - both parties receive unmasked contact information.\n"
            "- Inter-service: PATCH /api/v1/challenges/{id} with status='IN_PROGRESS'"
        ),
        "acceptance_criteria": (
            "- **Atomic Database Transaction:** Status change of the accepted application and rejection/freezing of competing candidates executes within `transaction.atomic()`.\n"
            "- **Inter-Service Challenge Locking (RB-04):** Calls Challenge service to set status='IN_PROGRESS'. If challenge service fails, transaction rolls back cleanly.\n"
            "- **Contact Exchange (RB-05):** Returns student contact info (email, phone) in response and makes company contact info available to student.\n"
            "- **Concurrency Guard:** Handles race conditions where two simultaneous accept requests hit the same challenge using `select_for_update()`."
        ),
        "deliverables": (
            "- [ ] Implement ApplicationAcceptView with select_for_update() and transaction.atomic()\n"
            "- [ ] Add Challenge service state transition sync client\n"
            "- [ ] Pytest test cases covering atomic lock, rollback, and concurrency"
        ),
        "verification": "podman exec conecta-application uv run pytest -k 'test_accept_application'"
    },
    {
        "task_id": "APPLICATION-TASK-07",
        "repo": "application",
        "service": "application",
        "parent_story": "HU-12",
        "parent_issue_number": "7",
        "title": "[APPLICATION-TASK-07] Application Rejection with Mandatory Explanation Endpoint (POST /{id}/reject/)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,application",
        "objective": "Implement application rejection endpoint requiring a mandatory explanatory reason (min 15 chars) while preserving the challenge in OPEN status.",
        "specs": (
            "- Endpoint: POST /api/v1/applications/{id}/reject/\n"
            "- Permissions: COMPANY role, Challenge Owner\n"
            "- Request Body: { feedback_reason: string (min 15 chars) }\n"
            "- Response: HTTP 200 OK with updated application status='REJECTED'"
        ),
        "acceptance_criteria": (
            "- **Mandatory Feedback:** Empty or short feedback (< 15 characters) returns HTTP 400 Bad Request with validation error.\n"
            "- **Challenge State Unchanged:** Challenge status remains strictly 'OPEN' so other students can continue applying.\n"
            "- **Audit Trail:** Feedback is saved in `feedback_reason` column with `updated_at` timestamp."
        ),
        "deliverables": (
            "- [ ] Implement ApplicationRejectView with feedback validation serializer\n"
            "- [ ] Pytest unit tests for valid rejection and rejection without feedback"
        ),
        "verification": "podman exec conecta-application uv run pytest -k 'test_reject_application'"
    },
    {
        "task_id": "APPLICATION-TASK-08",
        "repo": "application",
        "service": "application",
        "parent_story": "HU-12",
        "parent_issue_number": "7",
        "title": "[APPLICATION-TASK-08] Complete Integration Test Suite for Application Service",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,application",
        "objective": "Consolidate and execute a comprehensive Pytest test suite covering full application lifecycle, business rules RB-02, RB-03, RB-04, RB-05, and error status codes.",
        "specs": (
            "- Test Runner: Pytest with django-pytest and respx\n"
            "- Coverage Target: >= 85% of apps/applications/\n"
            "- Scenarios: Happy path submission, duplicate submission (409), ineligible semester (400), missing consent (400), closed challenge (422), upstream downtime (502), atomic accept, rejection feedback validation"
        ),
        "acceptance_criteria": (
            "- **Complete Test Pass:** All tests pass without warnings or failures.\n"
            "- **Coverage:** Measures coverage >= 85% for views, models, clients, and exceptions."
        ),
        "deliverables": (
            "- [ ] Write comprehensive integration tests in apps/applications/tests/\n"
            "- [ ] Execute and verify test coverage report"
        ),
        "verification": "podman exec conecta-application uv run pytest --cov=apps/applications"
    },
    {
        "task_id": "FRONTEND-TASK-13",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-12",
        "parent_issue_number": "7",
        "title": "[FRONTEND-TASK-13] Company Application Review & Decision View (Accept / Reject Modal)",
        "assignee": "juandiegosb",
        "labels": "task,sprint-3,frontend",
        "objective": "Build the company candidate evaluation interface allowing review of student motivation letters, profile summaries, acceptance modal, and rejection reason form.",
        "specs": (
            "- Components:\n"
            "  * app/components/applications/CandidateReviewDrawer.vue\n"
            "  * app/components/applications/ApplicationRejectModal.vue\n"
            "- Actions: Accept Candidate (triggers match lock confirmation), Reject Candidate (opens modal for mandatory feedback)"
        ),
        "acceptance_criteria": (
            "- **Candidate Review Drawer:** Side slide-over drawer displaying student name, semester, skills tags, and full motivation letter formatted in readable typography.\n"
            "- **Acceptance Confirmation Alert:** Clicking 'Accept Candidate' opens an alert modal: 'Accepting this candidate will lock the challenge to IN PROGRESS and notify the student. Do you wish to proceed?'\n"
            "- **Rejection Modal with Counter:** Rejection modal contains a textarea with live 15-character minimum counter. Confirm rejection button disabled until 15 characters are entered.\n"
            "- **Instant UI State Update:** On decision, candidate card updates status pill immediately without full page reload."
        ),
        "deliverables": (
            "- [ ] Create CandidateReviewDrawer.vue and ApplicationRejectModal.vue\n"
            "- [ ] Add character counter and validation to rejection modal\n"
            "- [ ] Vitest test suite in tests/components/applications/CandidateReviewDrawer.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/components/applications/CandidateReviewDrawer.spec.ts"
    },
    {
        "task_id": "FRONTEND-TASK-14",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-12",
        "parent_issue_number": "7",
        "title": "[FRONTEND-TASK-14] Reciprocal Contact Reveal Card & Match Celebration View",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,frontend",
        "objective": "Build the interactive Reciprocal Contact Card and Match Celebration Banner shown to both companies and students once an application is accepted.",
        "specs": (
            "- Component: app/components/applications/MatchContactCard.vue\n"
            "- Data: Contact person name, email (mailto: link), phone (tel: link), agreed start notes\n"
            "- Visuals: Confetti / celebration badge, copy-to-clipboard buttons"
        ),
        "acceptance_criteria": (
            "- **Visual Celebration Banner:** Green highlighted banner with party/check icon: 'Academic Match Successful! Contacts are now mutually revealed.'\n"
            "- **Interactive Contact Cards:** Clean contact cards with one-click 'Copy Email' and 'Copy Phone' buttons with tooltip feedback ('Copied!').\n"
            "- **Direct Communication Links:** `mailto:` and `tel:` links formatted for mobile dialing and desktop email clients.\n"
            "- **Privacy Watermark:** Subtle institutional footer: 'Contact data shared in accordance with Law 1581 for challenge execution only.'"
        ),
        "deliverables": (
            "- [ ] Build app/components/applications/MatchContactCard.vue\n"
            "- [ ] Implement copy-to-clipboard interactions with toast feedback\n"
            "- [ ] Vitest test suite in tests/components/applications/MatchContactCard.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/components/applications/MatchContactCard.spec.ts"
    },

    # =========================================================================
    # HU-13: Asynchronous Domain Alerts and SMTP Emailing (8 pts - Should Have)
    # =========================================================================
    {
        "task_id": "NOTIFICATION-TASK-01",
        "repo": "notification",
        "service": "notification",
        "parent_story": "HU-13",
        "parent_issue_number": "8",
        "title": "[NOTIFICATION-TASK-01] Notification Service FastEngine, Asyncpg & Event Dispatcher",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,notification",
        "objective": "Configure the core FastAPI engine, PostgreSQL connection with asyncpg for db_notifications, and event listener for transactional domain alerts.",
        "specs": (
            "- Service: notification (FastAPI + uv)\n"
            "- Database: PostgreSQL 16 (db_notifications)\n"
            "- Target Files: src/core/config.py, src/core/database.py, src/main.py\n"
            "- Events Supported: APPLICATION_CREATED, APPLICATION_ACCEPTED, APPLICATION_REJECTED, CHALLENGE_CLOSED"
        ),
        "acceptance_criteria": (
            "- **FastAPI Health & Startup:** Container starts cleanly with `/health` returning HTTP 200 and database connectivity status.\n"
            "- **Asyncpg Connection Pool:** Connection pool configured with pre-ping and environment variable overrides.\n"
            "- **Stateless RS256 Auth:** Implements JWT verification using public key for protected endpoints."
        ),
        "deliverables": (
            "- [ ] Configure FastAPI app and settings in src/core/config.py\n"
            "- [ ] Setup database engine and session factory in src/core/database.py\n"
            "- [ ] Unit tests verifying service startup and database ping"
        ),
        "verification": "podman exec conecta-notification uv run python -c 'import src.main; print(\"OK\")'"
    },
    {
        "task_id": "NOTIFICATION-TASK-02",
        "repo": "notification",
        "service": "notification",
        "parent_story": "HU-13",
        "parent_issue_number": "8",
        "title": "[NOTIFICATION-TASK-02] Transactional HTML Email Templates & Mailpit/SMTP Engine",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,notification",
        "objective": "Create responsive Jinja2 HTML email templates for all application events and implement the asynchronous SMTP sender connecting to Mailpit (local) and Cloud SMTP (prod).",
        "specs": (
            "- Templates (src/templates/):\n"
            "  * application_created.html (to company)\n"
            "  * application_accepted.html (to student & company with contacts)\n"
            "  * application_rejected.html (to student with feedback)\n"
            "- SMTP Engine: aiosmtplib with retry backoff and HTML/Plain-text alternative parts"
        ),
        "acceptance_criteria": (
            "- **Responsive HTML Design:** Templates render cleanly in desktop and mobile email clients with Conecta Nexus branding, logos, and action buttons.\n"
            "- **Mailpit Integration:** Emails dispatched locally land instantly in Mailpit web UI (`localhost:8025`).\n"
            "- **Fault Tolerance:** Temporary SMTP connection errors trigger exponential backoff retry (up to 3 attempts) before logging error."
        ),
        "deliverables": (
            "- [ ] Create 3 responsive HTML email templates in src/templates/\n"
            "- [ ] Implement EmailDispatcher service in src/services/email_service.py using aiosmtplib\n"
            "- [ ] Pytest unit tests mocking SMTP dispatch and verifying template variable rendering"
        ),
        "verification": "podman exec conecta-notification uv run pytest tests/test_email_service.py"
    },
    {
        "task_id": "NOTIFICATION-TASK-03",
        "repo": "notification",
        "service": "notification",
        "parent_story": "HU-13",
        "parent_issue_number": "8",
        "title": "[NOTIFICATION-TASK-03] In-App Notification Center Model & Storage",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,notification",
        "objective": "Implement the Notification database model in db_notifications for in-app alert tracking, read states, and user notification history.",
        "specs": (
            "- Model: Notification (src/models/notification.py)\n"
            "- Columns: id (UUID PK), user_id (UUID), event_type (VARCHAR), title (VARCHAR), message (TEXT), link_url (VARCHAR), is_read (BOOLEAN default False), created_at (TIMESTAMP)\n"
            "- Indexes: B-Tree index on (user_id, is_read, created_at)"
        ),
        "acceptance_criteria": (
            "- **Table Creation:** SQLAlchemy model and migrations create `notifications` table in `db_notifications`.\n"
            "- **Query Performance:** Compound index ensures sub-millisecond retrieval of unread notifications for a user.\n"
            "- **Read State:** New notifications default to `is_read = False`."
        ),
        "deliverables": (
            "- [ ] Create Notification model in src/models/notification.py\n"
            "- [ ] Setup Alembic migration in notification service\n"
            "- [ ] Unit tests for model persistence and indexing"
        ),
        "verification": "podman exec conecta-notification uv run alembic upgrade head"
    },
    {
        "task_id": "NOTIFICATION-TASK-04",
        "repo": "notification",
        "service": "notification",
        "parent_story": "HU-13",
        "parent_issue_number": "8",
        "title": "[NOTIFICATION-TASK-04] In-App Notification Query & Read State REST Endpoints",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,notification",
        "objective": "Expose REST endpoints for users to retrieve their in-app notifications, mark individual notifications as read, and bulk mark all as read.",
        "specs": (
            "- Endpoints:\n"
            "  * GET /api/v1/notifications/me (list user notifications with unread count)\n"
            "  * PATCH /api/v1/notifications/{id}/read (mark single notification as read)\n"
            "  * PATCH /api/v1/notifications/read-all (bulk mark as read)\n"
            "- Permissions: IsAuthenticated with JWT sub claim matching user_id"
        ),
        "acceptance_criteria": (
            "- **User Isolation:** Users can only view and update their own notifications.\n"
            "- **Unread Counter:** `GET /me` returns `{ items: [...], unread_count: int }` for navbar badge rendering.\n"
            "- **Mark as Read:** `PATCH /{id}/read` sets `is_read = True` and updates unread count."
        ),
        "deliverables": (
            "- [ ] Implement notification router in src/routers/notifications.py\n"
            "- [ ] Add Pydantic response and update schemas\n"
            "- [ ] Pytest integration tests covering query and read state updates"
        ),
        "verification": "podman exec conecta-notification uv run pytest tests/test_notification_router.py"
    },
    {
        "task_id": "NOTIFICATION-TASK-05",
        "repo": "notification",
        "service": "notification",
        "parent_story": "HU-13",
        "parent_issue_number": "8",
        "title": "[NOTIFICATION-TASK-05] Unit & Integration Test Suite for Notification Service",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,notification",
        "objective": "Develop comprehensive test suite verifying email templating, SMTP dispatching with mocks, in-app notification queries, and read-state transitions.",
        "specs": (
            "- Framework: Pytest, pytest-asyncio, httpx\n"
            "- Coverage: >= 80% across notification service"
        ),
        "acceptance_criteria": (
            "- **Full Test Suite Passing:** All unit and router tests pass cleanly.\n"
            "- **SMTP Mocking:** Tests verify that SMTP payload matches expected recipient and HTML body."
        ),
        "deliverables": (
            "- [ ] Test cases in tests/ for models, templates, and routers\n"
            "- [ ] Test coverage report verifying >= 80%"
        ),
        "verification": "podman exec conecta-notification uv run pytest -q"
    },
    {
        "task_id": "FRONTEND-TASK-15",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-13",
        "parent_issue_number": "8",
        "title": "[FRONTEND-TASK-15] In-App Notification Center Drawer & Toast Alert System",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,frontend",
        "objective": "Build the Notification Bell in the navigation bar with unread badge counter, slide-over notification drawer, and real-time toast alert popups.",
        "specs": (
            "- Components:\n"
            "  * app/components/notifications/NotificationBell.vue\n"
            "  * app/components/notifications/NotificationDrawer.vue\n"
            "- Composable: app/composables/useNotifications.ts (polling or SSE query, markAsRead, unreadCount)\n"
            "- Visuals: Nuxt UI slide-over, unread red badge pill"
        ),
        "acceptance_criteria": (
            "- **Navbar Bell Badge:** Bell icon in top navbar with a red badge showing unread count (e.g. '3'). Badge hides when unread count is 0.\n"
            "- **Slide-over Drawer:** Clicking bell opens smooth slide-over drawer displaying list of notifications with timestamp, icon by type, and 'Mark All as Read' button.\n"
            "- **Interactive Read State:** Clicking an unread notification marks it as read, decrements the badge counter, and navigates to the relevant entity (e.g. application detail).\n"
            "- **Real-time Toasts:** Incoming events display a bottom-right toast notification that auto-dismisses after 5 seconds."
        ),
        "deliverables": (
            "- [ ] Create NotificationBell.vue and NotificationDrawer.vue\n"
            "- [ ] Implement useNotifications.ts composable\n"
            "- [ ] Vitest test suite in tests/components/notifications/NotificationDrawer.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/components/notifications/NotificationDrawer.spec.ts"
    },

    # =========================================================================
    # HU-14: Platform Governance and Institutional Audit Log (8 pts - Should Have)
    # =========================================================================
    {
        "task_id": "MODERATION-TASK-01",
        "repo": "moderation",
        "service": "moderation",
        "parent_story": "HU-14",
        "parent_issue_number": "9",
        "title": "[MODERATION-TASK-01] Moderation Database Model & Append-Only Audit Log Engine",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,moderation",
        "objective": "Implement the AuditLog model in db_moderation with strict append-only constraints, recording all administrative governance actions, entity suspensions, and user audit trails.",
        "specs": (
            "- Service: moderation (Django + DRF)\n"
            "- Database: PostgreSQL 16 (db_moderation)\n"
            "- Model: AuditLog (apps/moderation/models.py)\n"
            "- Fields: id (UUID PK), actor_id (UUID), actor_email (VARCHAR), actor_role (ADMIN), action_type (CHALLENGE_SUSPEND, USER_SUSPEND, CONTENT_FLAG), target_id (UUID), target_type (CHALLENGE, USER), justification (TEXT), ip_address (GenericIPAddressField), created_at (TIMESTAMP)\n"
            "- Immutability Rule: No UPDATE or DELETE allowed; model overrides save() and delete() to prevent mutation."
        ),
        "acceptance_criteria": (
            "- **Database Migration:** Creates `moderation_auditlog` table in `db_moderation`.\n"
            "- **Append-Only Immutability:** Attempting to call `.delete()` or update an existing `AuditLog` instance raises PermissionDenied / ImmutableLogException.\n"
            "- **Mandatory Justification:** Every action requires a non-empty `justification` string."
        ),
        "deliverables": (
            "- [ ] Create AuditLog model in apps/moderation/models.py with immutability guards\n"
            "- [ ] Generate and execute Django migrations\n"
            "- [ ] Unit tests verifying append-only behavior and immutability"
        ),
        "verification": "podman exec conecta-moderation python manage.py migrate"
    },
    {
        "task_id": "MODERATION-TASK-02",
        "repo": "moderation",
        "service": "moderation",
        "parent_story": "HU-14",
        "parent_issue_number": "9",
        "title": "[MODERATION-TASK-02] Django Admin Institutional Governance Dashboard",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,moderation",
        "objective": "Configure custom Django Admin interface in moderation service with read-only audit log views, search by actor and entity, date range filters, and institutional branding.",
        "specs": (
            "- Django Admin: apps/moderation/admin.py\n"
            "- Read-only Configuration: has_add_permission=False, has_change_permission=False, has_delete_permission=False for audit logs\n"
            "- Filters: action_type, target_type, created_at\n"
            "- Search: actor_email, target_id, justification"
        ),
        "acceptance_criteria": (
            "- **Read-Only Enforcement:** Admin UI prevents adding, editing, or deleting audit logs directly through the web interface.\n"
            "- **Search & Filters:** Administrators can instantly filter logs by action type (e.g. `CHALLENGE_SUSPEND`) and date range.\n"
            "- **Detail View:** Inspecting an individual log shows full actor details, IP address, timestamp, and justification."
        ),
        "deliverables": (
            "- [ ] Configure custom AuditLogAdmin in apps/moderation/admin.py\n"
            "- [ ] Customize Django admin headers with Conecta Nexus branding\n"
            "- [ ] Unit tests verifying read-only permissions in admin"
        ),
        "verification": "podman exec conecta-moderation python manage.py test apps.moderation.tests.test_admin"
    },
    {
        "task_id": "MODERATION-TASK-03",
        "repo": "moderation",
        "service": "moderation",
        "parent_story": "HU-14",
        "parent_issue_number": "9",
        "title": "[MODERATION-TASK-03] Inter-Service Suspension Webhook & Event Dispatcher",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,moderation",
        "objective": "Implement administrative endpoints in Moderation service to suspend challenges or users, notifying Challenge and Auth services synchronously and appending immutable audit entries.",
        "specs": (
            "- Endpoints:\n"
            "  * POST /api/v1/moderation/challenges/{id}/suspend/\n"
            "  * POST /api/v1/moderation/users/{id}/suspend/\n"
            "- Permissions: IsAuthenticated, require_role('ADMIN')\n"
            "- Body: { justification: string (min 15 chars) }\n"
            "- Inter-service calls: PATCH /api/v1/challenges/{id} with status='CANCELLED' and auth user deactivation"
        ),
        "acceptance_criteria": (
            "- **Role RBAC Guard:** Only ADMIN role can trigger suspensions; students and companies receive HTTP 403 Forbidden.\n"
            "- **Inter-Service Synchronization:** Suspending a challenge calls Challenge service to revoke publication from catalog; failure rolls back audit entry.\n"
            "- **Automatic Audit Recording:** Action automatically creates an immutable `AuditLog` record with administrator ID, IP address, and justification."
        ),
        "deliverables": (
            "- [ ] Implement challenge and user suspension views in apps/moderation/views.py\n"
            "- [ ] Build inter-service HTTP client for Challenge and Auth synchronization\n"
            "- [ ] Pytest unit tests for suspension actions and audit log creation"
        ),
        "verification": "podman exec conecta-moderation uv run pytest -k 'test_suspension'"
    },
    {
        "task_id": "MODERATION-TASK-04",
        "repo": "moderation",
        "service": "moderation",
        "parent_story": "HU-14",
        "parent_issue_number": "9",
        "title": "[MODERATION-TASK-04] Audit Log Consultation REST Endpoint with Admin RBAC",
        "assignee": "NelsonConde",
        "labels": "task,sprint-3,moderation",
        "objective": "Expose a paginated REST endpoint for frontend admin dashboards to query immutable audit logs with multi-parameter filtering and date ranges.",
        "specs": (
            "- Endpoint: GET /api/v1/moderation/audit-logs/\n"
            "- Query Params: page, page_size, action_type, actor_id, start_date, end_date\n"
            "- Permissions: IsAuthenticated, require_role('ADMIN')\n"
            "- Response: Paginated JSON list of audit entries"
        ),
        "acceptance_criteria": (
            "- **Strict Admin Access:** Anonymous users receive 401; non-admin authenticated users receive 403.\n"
            "- **Pagination & Ordering:** Results paginated (default 20 per page) and strictly ordered by `created_at DESC`.\n"
            "- **Date Range Filtering:** Supports filtering between ISO date strings `start_date` and `end_date`."
        ),
        "deliverables": (
            "- [ ] Implement AuditLogListView in apps/moderation/views.py\n"
            "- [ ] Create AuditLogSerializer with full audit details\n"
            "- [ ] Pytest tests covering pagination and filter params"
        ),
        "verification": "podman exec conecta-moderation uv run pytest -k 'test_audit_log_list'"
    },
    {
        "task_id": "MODERATION-TASK-05",
        "repo": "moderation",
        "service": "moderation",
        "parent_story": "HU-14",
        "parent_issue_number": "9",
        "title": "[MODERATION-TASK-05] Unit & Integration Test Suite for Moderation Service",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,moderation",
        "objective": "Consolidate complete Pytest test suite for Moderation service verifying audit log immutability, admin permissions, and suspension endpoints.",
        "specs": (
            "- Runner: Pytest with django-pytest and respx\n"
            "- Coverage Target: >= 85% of apps/moderation/"
        ),
        "acceptance_criteria": (
            "- **All Tests Pass:** 100% test pass rate on all moderation test suites.\n"
            "- **Audit Immutability Verification:** Test explicitly asserts that calling `.delete()` or `.update()` on an AuditLog raises an exception."
        ),
        "deliverables": (
            "- [ ] Pytest test cases in apps/moderation/tests/\n"
            "- [ ] Test coverage report verifying >= 85%"
        ),
        "verification": "podman exec conecta-moderation uv run pytest --cov=apps/moderation"
    },
    {
        "task_id": "FRONTEND-TASK-16",
        "repo": "frontend",
        "service": "frontend",
        "parent_story": "HU-14",
        "parent_issue_number": "9",
        "title": "[FRONTEND-TASK-16] Moderation & Audit Log Admin Dashboard View (/moderation)",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,frontend",
        "objective": "Build the institutional governance and moderation dashboard (/moderation) allowing administrators to audit activity logs, search actions, and view suspended entities.",
        "specs": (
            "- Route: /moderation\n"
            "- Role Guard: ADMIN only\n"
            "- Components: AuditLogTable.vue, SuspensionModal.vue\n"
            "- Table Columns: Timestamp, Admin Actor, Action Type Badge, Target Entity, Justification, IP Address"
        ),
        "acceptance_criteria": (
            "- **Admin Access Guard:** Non-admin users attempting to visit `/moderation` are redirected to `/` with an access denied toast.\n"
            "- **Visual Audit Log Table:** Clean tabular layout with color-coded action badges (Red for Suspensions, Blue for Flags, Gray for System Actions).\n"
            "- **Filter Controls:** Top filter bar with dropdown for action types and date range picker.\n"
            "- **Justification Popover:** Truncated justifications can be clicked to view complete audit explanation in an accessible popover."
        ),
        "deliverables": (
            "- [ ] Create app/pages/moderation/index.vue with admin middleware guard\n"
            "- [ ] Build AuditLogTable.vue with action type badges\n"
            "- [ ] Vitest test suite in tests/pages/moderation/index.spec.ts"
        ),
        "verification": "cd frontend && pnpm test tests/pages/moderation/index.spec.ts"
    },

    # =========================================================================
    # SPRINT 3 API GATEWAY & INFRASTRUCTURE TASKS (5 Tasks)
    # =========================================================================
    {
        "task_id": "GATEWAY-TASK-03",
        "repo": "gateway",
        "service": "gateway",
        "parent_story": "HU-13",
        "parent_issue_number": "8",
        "title": "[GATEWAY-TASK-03] Upstream Routing & WebSocket / SSE Configuration for Notifications & Moderation",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,gateway",
        "objective": "Configure upstream routing blocks in gateway/conf.d/default.conf for Notification and Moderation microservices, supporting long-lived connections for real-time alerts.",
        "specs": (
            "- Gateway: Nginx\n"
            "- Upstreams: notification_upstream (notification:8000), moderation_upstream (moderation:8000)\n"
            "- Routes: /api/v1/notifications/, /api/v1/moderation/\n"
            "- Headers: Standard CORS, JWT Claims forwarding (X-User-Id, X-User-Role), keepalive 65s"
        ),
        "acceptance_criteria": (
            "- **Route Mapping:** Requests to `/api/v1/notifications/*` and `/api/v1/moderation/*` proxy cleanly to their respective services.\n"
            "- **Header Forwarding:** Nginx forwards Authorization and user claims to upstreams.\n"
            "- **Error Mapping:** Upstream failures return standardized JSON 502/504 error envelopes."
        ),
        "deliverables": (
            "- [ ] Update gateway/conf.d/default.conf with notification and moderation upstreams\n"
            "- [ ] Test nginx syntax and reload service in container"
        ),
        "verification": "podman exec conecta-gateway nginx -t"
    },
    {
        "task_id": "GATEWAY-TASK-04",
        "repo": "gateway",
        "service": "gateway",
        "parent_story": "HU-11",
        "parent_issue_number": "6",
        "title": "[GATEWAY-TASK-04] Rate Limiting & Security Hardening for Application Submission & Admin Routes",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,gateway",
        "objective": "Implement specific rate-limiting zones in Nginx to protect application submissions from spamming and secure administrative moderation routes against brute-force attacks.",
        "specs": (
            "- Rate Limit Zones:\n"
            "  * application_limit_zone: 5 req/min per IP on `POST /api/v1/applications/`\n"
            "  * admin_limit_zone: 10 req/s on `/api/v1/moderation/`\n"
            "- Error Response: Standard 429 JSON response with Retry-After header"
        ),
        "acceptance_criteria": (
            "- **Submission Throttling:** Rapid consecutive application submissions (> 5 per minute) return HTTP 429 Too Many Requests.\n"
            "- **Standard Error JSON:** Returns team standard JSON `{ detail: 'Too Many Requests: Rate limit exceeded' }`.\n"
            "- **Nginx Configuration Validity:** `nginx -t` confirms zero syntax or memory zone errors."
        ),
        "deliverables": (
            "- [ ] Add limit_req_zone directives to gateway/conf.d/default.conf\n"
            "- [ ] Apply limit_req to application submission location block\n"
            "- [ ] Validate nginx configuration"
        ),
        "verification": "podman exec conecta-gateway nginx -t"
    },
    {
        "task_id": "INFRA-TASK-05",
        "repo": "infra",
        "service": "infra",
        "parent_story": "HU-11",
        "parent_issue_number": "6",
        "title": "[INFRA-TASK-05] Cloud Run & Cloud SQL Provisioning for Application Service",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,infra",
        "objective": "Provision google_cloud_run_v2_service.application and PostgreSQL database db_applications in Terraform with VPC connector, environment secrets, and Cloud SQL IAM bindings.",
        "specs": (
            "- Terraform Files: infra/cloud_run.tf, infra/cloud_sql.tf\n"
            "- Cloud Run: conecta-application service (us-central1, min 0 max 5 instances, 512Mi memory, 1 vCPU)\n"
            "- Database: db_applications on existing Cloud SQL instance with secure credentials via Secret Manager"
        ),
        "acceptance_criteria": (
            "- **Terraform Validation:** `terraform validate` executes cleanly with zero errors.\n"
            "- **Environment Secret Linking:** DATABASE_URL and JWT_PUBLIC_KEY mapped from Secret Manager references.\n"
            "- **VPC Access Connector:** Configured with Serverless VPC Connector for secure Cloud SQL private IP communication."
        ),
        "deliverables": (
            "- [ ] Add google_cloud_run_v2_service.application resource in infra/cloud_run.tf\n"
            "- [ ] Add db_applications database resource in infra/cloud_sql.tf\n"
            "- [ ] Execute terraform validate and plan"
        ),
        "verification": "cd infra && terraform validate"
    },
    {
        "task_id": "INFRA-TASK-06",
        "repo": "infra",
        "service": "infra",
        "parent_story": "HU-13",
        "parent_issue_number": "8",
        "title": "[INFRA-TASK-06] Cloud Run & Database Provisioning for Notification & Moderation Services",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,infra",
        "objective": "Provision Cloud Run services and databases for Notification (db_notifications) and Moderation (db_moderation) services in Terraform with IAM invoker permissions.",
        "specs": (
            "- Terraform Files: infra/cloud_run.tf, infra/cloud_sql.tf\n"
            "- Resources: google_cloud_run_v2_service.notification, google_cloud_run_v2_service.moderation\n"
            "- Databases: db_notifications, db_moderation on Cloud SQL\n"
            "- Invoker: Internal ingress or public with API Gateway authentication"
        ),
        "acceptance_criteria": (
            "- **Terraform Clean Validation:** Configuration passes `terraform validate`.\n"
            "- **Database Resource Declarations:** Both databases declared with UTF8 encoding and matching Secret Manager credentials."
        ),
        "deliverables": (
            "- [ ] Add Cloud Run resources for notification and moderation in infra/cloud_run.tf\n"
            "- [ ] Add database resources in infra/cloud_sql.tf\n"
            "- [ ] Verify terraform plan"
        ),
        "verification": "cd infra && terraform validate"
    },
    {
        "task_id": "INFRA-TASK-07",
        "repo": "infra",
        "service": "infra",
        "parent_story": "HU-13",
        "parent_issue_number": "8",
        "title": "[INFRA-TASK-07] Local Podman / Docker Compose Complete Stack Stabilization (Mailpit, Healthchecks)",
        "assignee": "AnorakTeam",
        "labels": "task,sprint-3,infra",
        "objective": "Stabilize and verify the complete 7-microservice local compose stack in compose.yaml, adding Mailpit SMTP mock container, volume persistency, and container healthchecks.",
        "specs": (
            "- Target File: compose.yaml\n"
            "- Services: postgres, auth, profile, challenge, application, notification, moderation, frontend, gateway, mailpit\n"
            "- Mailpit Ports: 1025 (SMTP), 8025 (Web UI)\n"
            "- Healthchecks: Configured on all microservice containers with 5s retries"
        ),
        "acceptance_criteria": (
            "- **Compose Validity:** `podman compose config` or `docker compose config` validates without syntax errors.\n"
            "- **Mailpit Availability:** Mailpit container runs and web dashboard is reachable at `http://localhost:8025`.\n"
            "- **Complete Stack Up:** All containers run concurrently in the local developer network without port collisions."
        ),
        "deliverables": (
            "- [ ] Add mailpit service definition to compose.yaml\n"
            "- [ ] Verify container dependencies and healthchecks across all 10 containers\n"
            "- [ ] Validate compose configuration"
        ),
        "verification": "podman compose config || docker compose config"
    }
]


def build_markdown_body(task: dict) -> str:
    """Builds the standardized markdown body following .github/ISSUE_TEMPLATE/task.md with explicit acceptance criteria."""
    parent_issue = task["parent_issue_number"]
    return (
        f"### 1. Task Metadata & Traceability\n"
        f"- **Module / Microservice:** `{task['service']}`\n"
        f"- **Parent User Story:** {task['parent_story']} (Closes part of conecta-nexus/{task['repo']}#{parent_issue})\n"
        f"- **Assigned Developer:** @{task['assignee']}\n"
        f"- **Sprint:** Sprint 3 (12 Nov – 02 Dec 2026)\n"
        f"- **Labels:** `{task['labels']}`\n\n"
        f"---\n\n"
        f"### 2. Objective & Description\n"
        f"{task['objective']}\n\n"
        f"---\n\n"
        f"### 3. Technical Specifications & Constraints\n"
        f"{task['specs']}\n\n"
        f"---\n\n"
        f"### 4. Explicit Acceptance Criteria & Visual/Functional Specifications\n"
        f"{task['acceptance_criteria']}\n\n"
        f"---\n\n"
        f"### 5. Deliverables & Checklist\n"
        f"{task['deliverables']}\n\n"
        f"---\n\n"
        f"### 6. Verification Command\n"
        f"```bash\n{task['verification']}\n```"
    )


def main():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conecta_nexus_sprint_3_tasks.csv")
    fieldnames = [
        "task_id", "repo", "service", "parent_story", "parent_issue_number",
        "title", "assignee", "labels", "objective", "specs", "acceptance_criteria",
        "deliverables", "verification", "body"
    ]
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for task in TASKS:
            row = dict(task)
            row["body"] = build_markdown_body(task)
            writer.writerow(row)
    print(f"✔ Successfully generated {len(TASKS)} Sprint 3 engineering tasks into '{filename}'.")

    # Developer count check
    counts = {}
    for task in TASKS:
        counts[task["assignee"]] = counts.get(task["assignee"], 0) + 1
    print("\n--- Developer Workload Distribution ---")
    for dev, count in counts.items():
        print(f"  @{dev}: {count} tasks")


if __name__ == "__main__":
    main()
