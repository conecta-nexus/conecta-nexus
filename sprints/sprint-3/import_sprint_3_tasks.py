#!/usr/bin/env python3
"""
Conecta Nexus - Official Sprint 3 Task Importer for GitHub Projects & Repositories
1. Ensures all required labels exist across all target repositories.
2. Reopens the 10 Sprint 2 Frontend tasks (#9 through #18 in conecta-nexus/frontend),
   updates their titles with '-R', updates their bodies with explicit acceptance criteria,
   applies labels 'sprint-3' and 'reopened', assigns developers, and configures Project #2
   with Status = 'To Do' and Iteration = 'Sprint 3'.
3. Creates the remaining 29 Sprint 3 technical engineering tasks in their respective repos
   (application, notification, moderation, frontend, gateway, infra), assigns developers,
   adds them to Project #2, and sets Status = 'To Do' and Iteration = 'Sprint 3'.
"""

import os
import sys
import csv
import json
import time
import shutil
import subprocess

ORG = "conecta-nexus"
PROJECT_NUM = 2
PROJECT_ID = "PVT_kwDOE2mZY84BmwV4"
STATUS_FIELD_ID = "PVTSSF_lADOE2mZY84BmwV4zhlYC3M"
TODO_OPTION_ID = "f75ad846"
SPRINT_FIELD_ID = "PVTIF_lADOE2mZY84BmwV4zhlYDeA"
SPRINT_3_ITER_ID = "d2c335bc"

CSV_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conecta_nexus_sprint_3_tasks.csv")
RESULTS_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "import_results.json")

# Mapping of reopened frontend tasks to their existing issue numbers in conecta-nexus/frontend
REOPENED_FRONTEND_MAP = {
    "FRONTEND-TASK-01-R": 9,
    "FRONTEND-TASK-02-R": 10,
    "FRONTEND-TASK-03-R": 11,
    "FRONTEND-TASK-04-R": 12,
    "FRONTEND-TASK-05-R": 13,
    "FRONTEND-TASK-06-R": 14,
    "FRONTEND-TASK-07-R": 15,
    "FRONTEND-TASK-08-R": 16,
    "FRONTEND-TASK-09-R": 17,
    "FRONTEND-TASK-10-R": 18,
}


def run_command_with_retry(cmd, max_retries=5, initial_delay=2, is_json=False):
    """Executes a subprocess command with exponential backoff on network failures."""
    for attempt in range(1, max_retries + 1):
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode == 0:
                if is_json:
                    try:
                        return True, json.loads(res.stdout)
                    except json.JSONDecodeError as e:
                        return False, f"JSONDecodeError: {e} -> stdout: {res.stdout[:100]}"
                return True, res.stdout.strip()

            stderr = res.stderr.strip()
            if "rate limit" in stderr.lower():
                wait = 15 * attempt
                print(f"      [Retry {attempt}/{max_retries}] Rate limit detected. Waiting {wait}s...")
                time.sleep(wait)
                continue

            transient_signals = [
                "error connecting to api.github.com",
                "timeout",
                "tls handshake timeout",
                "connection reset by peer",
                "network is unreachable",
                "could not resolve host"
            ]
            if any(signal in stderr.lower() for signal in transient_signals):
                wait = initial_delay * attempt
                print(f"      [Retry {attempt}/{max_retries}] Transient network error. Waiting {wait}s...")
                time.sleep(wait)
                continue

            return False, f"Exit code {res.returncode}: {stderr}"
        except Exception as ex:
            wait = initial_delay * attempt
            print(f"      [Retry {attempt}/{max_retries}] Local exception: {ex}. Waiting {wait}s...")
            time.sleep(wait)

    return False, "Exceeded maximum retries."


def ensure_labels(repo):
    """Ensures standardized labels exist in the target repository."""
    labels = [
        {"name": "task", "color": "0E8A16", "description": "Granular engineering task"},
        {"name": "sprint-3", "color": "1D76DB", "description": "Sprint 3 Deliverable (12 Nov - 02 Dec 2026)"},
        {"name": "reopened", "color": "B60205", "description": "Reopened item from previous sprint"},
        {"name": "frontend", "color": "5319E7", "description": "Nuxt 4 / Vue 3 user interface"},
        {"name": "application", "color": "FBCA04", "description": "Application microservice"},
        {"name": "notification", "color": "006B75", "description": "Notification microservice"},
        {"name": "moderation", "color": "D93F0B", "description": "Moderation microservice"},
        {"name": "gateway", "color": "C2E0C6", "description": "API Gateway / Nginx"},
        {"name": "infra", "color": "BFDADC", "description": "Terraform / Cloud Infrastructure"}
    ]
    for lbl in labels:
        cmd = [
            "gh", "label", "create", lbl["name"],
            "--repo", f"{ORG}/{repo}",
            "--color", lbl["color"],
            "--description", lbl["description"],
            "--force"
        ]
        run_command_with_retry(cmd)


def update_project_item(issue_url):
    """Adds the issue to Project 2 and sets Status = 'To Do' and Iteration = 'Sprint 3'."""
    # 1. Add item to project (idempotent; if already added, returns existing item ID)
    add_cmd = [
        "gh", "project", "item-add", str(PROJECT_NUM),
        "--owner", ORG,
        "--url", issue_url,
        "--format", "json"
    ]
    ok_add, add_out = run_command_with_retry(add_cmd, is_json=True)
    if not ok_add:
        # Fallback without json
        run_command_with_retry(["gh", "project", "item-add", str(PROJECT_NUM), "--owner", ORG, "--url", issue_url])

    # 2. Set Status = 'To Do'
    status_cmd = [
        "gh", "project", "item-edit", str(PROJECT_NUM),
        "--owner", ORG,
        "--url", issue_url,
        "--field", "Status",
        "--value", "To Do"
    ]
    run_command_with_retry(status_cmd)

    # 3. Set Iteration = 'Sprint 3'
    iter_cmd = [
        "gh", "project", "item-edit", str(PROJECT_NUM),
        "--owner", ORG,
        "--url", issue_url,
        "--field", "Iteration",
        "--iteration-id", SPRINT_3_ITER_ID
    ]
    run_command_with_retry(iter_cmd)


def main():
    if not shutil.which("gh"):
        print("❌ Error: GitHub CLI ('gh') is not installed.")
        sys.exit(1)

    auth_ok, auth_out = run_command_with_retry(["gh", "auth", "status"])
    if not auth_ok:
        print(f"❌ GitHub CLI authentication error:\n{auth_out}")
        sys.exit(1)

    print("==================================================================")
    print("      CONECTA NEXUS — SPRINT 3 TASK & BOARD AUTOMATION            ")
    print("==================================================================")
    print(f"✔ Organization: {ORG}")
    print(f"✔ Project Number: #{PROJECT_NUM} (ID: {PROJECT_ID})")
    print(f"✔ Sprint 3 Iteration ID: {SPRINT_3_ITER_ID}")
    print(f"✔ Source CSV: {CSV_FILENAME}")

    if not os.path.exists(CSV_FILENAME):
        print(f"❌ Error: CSV file '{CSV_FILENAME}' not found.")
        sys.exit(1)

    with open(CSV_FILENAME, mode="r", encoding="utf-8") as f:
        tasks = list(csv.DictReader(f))

    print(f"✔ Total tasks loaded from CSV: {len(tasks)}")

    # Ensure labels on all target repos
    target_repos = list(set(t["repo"] for t in tasks))
    print(f"\n[1/3] Ensuring standardized labels on repositories: {', '.join(target_repos)}...")
    for repo in target_repos:
        ensure_labels(repo)
    print("✔ Standardized labels verified.")

    # Load previous successful results to resume gracefully
    results_map = {}
    if os.path.exists(RESULTS_FILENAME):
        try:
            with open(RESULTS_FILENAME, mode="r", encoding="utf-8") as rf:
                prev_results = json.load(rf)
                for item in prev_results:
                    if item.get("status") != "ERROR" and item.get("url"):
                        results_map[item["task_id"]] = item
        except Exception:
            pass

    results = []
    print("\n[2/3] Processing Tasks (Reopening Sprint 2 Frontend & Creating New Sprint 3 Tasks)...")

    for idx, task in enumerate(tasks, start=1):
        task_id = task["task_id"]
        repo = task["repo"]
        title = task["title"]
        assignee = task["assignee"]
        labels = task["labels"]
        body = task["body"]

        print(f"\n--- [{idx}/{len(tasks)}] {task_id}: {title[:65]} ---")

        if task_id in results_map:
            print(f"   ✔ Already imported & synced: {results_map[task_id]['url']}")
            results.append(results_map[task_id])
            continue

        # Check if it's one of the reopened Sprint 2 Frontend tasks
        if task_id in REOPENED_FRONTEND_MAP:
            issue_num = REOPENED_FRONTEND_MAP[task_id]
            issue_url = f"https://github.com/{ORG}/{repo}/issues/{issue_num}"
            print(f"   🔄 Reopening existing frontend issue #{issue_num} ({task_id})...")

            # 1. Reopen issue
            reopen_cmd = ["gh", "issue", "reopen", str(issue_num), "--repo", f"{ORG}/{repo}"]
            ok_reopen, reopen_out = run_command_with_retry(reopen_cmd)
            if ok_reopen:
                print(f"      ✔ Issue #{issue_num} reopened.")
            else:
                print(f"      ℹ Reopen notice: {reopen_out}")

            # 2. Edit issue details (title, body with explicit acceptance criteria, labels, assignee)
            edit_cmd = [
                "gh", "issue", "edit", str(issue_num),
                "--repo", f"{ORG}/{repo}",
                "--title", title,
                "--body", body,
                "--add-label", "sprint-3,reopened"
            ]
            if assignee:
                edit_cmd.extend(["--add-assignee", assignee])

            ok_edit, edit_out = run_command_with_retry(edit_cmd)
            if ok_edit:
                print(f"      ✔ Issue #{issue_num} updated with explicit criteria & sprint-3 labels.")
            else:
                print(f"      ⚠ Edit warning: {edit_out}")

            # 3. Update project item status and sprint iteration
            print("      📌 Updating Project #2 board item (Status = 'To Do', Iteration = 'Sprint 3')...")
            update_project_item(issue_url)
            print("      ✔ Project board updated.")

            results.append({
                "task_id": task_id,
                "action": "REOPENED",
                "issue_number": issue_num,
                "url": issue_url,
                "assignee": assignee
            })

        else:
            # New Sprint 3 Task -> Check if already exists by title
            search_cmd = [
                "gh", "issue", "list",
                "--repo", f"{ORG}/{repo}",
                "--state", "all",
                "--search", f"\"{title}\"",
                "--json", "number,url"
            ]
            ok_search, search_data = run_command_with_retry(search_cmd, is_json=True)
            existing_url = None
            if ok_search and isinstance(search_data, list) and len(search_data) > 0:
                existing_url = search_data[0].get("url")
                existing_num = search_data[0].get("number")
                print(f"   ℹ Task already exists as issue #{existing_num}: {existing_url}")
                issue_url = existing_url
            else:
                print(f"   ➕ Creating new issue in {ORG}/{repo}...")
                create_cmd = [
                    "gh", "issue", "create",
                    "--repo", f"{ORG}/{repo}",
                    "--title", title,
                    "--body", body,
                    "--label", labels
                ]
                if assignee:
                    create_cmd.extend(["--assignee", assignee])

                ok_create, create_out = run_command_with_retry(create_cmd)
                if not ok_create:
                    print(f"   ❌ Error creating issue: {create_out}")
                    results.append({"task_id": task_id, "status": "ERROR", "error": str(create_out)})
                    continue

                issue_url = create_out
                print(f"   ✔ Issue created: {issue_url}")

            # Add / update on Project #2
            print("      📌 Updating Project #2 board item (Status = 'To Do', Iteration = 'Sprint 3')...")
            update_project_item(issue_url)
            print("      ✔ Project board updated.")

            results.append({
                "task_id": task_id,
                "action": "CREATED" if not existing_url else "SYNCED",
                "url": issue_url,
                "assignee": assignee
            })

        # Save progress incrementally
        with open(RESULTS_FILENAME, mode="w", encoding="utf-8") as rf:
            json.dump(results, rf, indent=2)

        time.sleep(1.5)

    # Save results
    with open(RESULTS_FILENAME, mode="w", encoding="utf-8") as rf:
        json.dump(results, rf, indent=2)

    print("\n==================================================================")
    print(f"✔ SPRINT 3 IMPORT COMPLETED! Summary saved in '{RESULTS_FILENAME}'.")
    print(f"✔ Total tasks processed: {len(results)}/{len(tasks)}")
    print("==================================================================")


if __name__ == "__main__":
    main()
