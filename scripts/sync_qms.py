"""QMS sync script.

Reads self-harness traces/failures and generates corresponding
QMS records (NCRs, verifications, CAPA stubs).

Usage:
    python scripts/sync_qms.py --project-dir /path/to/project
    python scripts/sync_qms.py --project-dir /path/to/project --dry-run
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def next_ncr_id(records_dir):
    existing = list(Path(records_dir / "nonconformities").glob("*.json"))
    n = len(existing) + 1
    return f"NCR-{datetime.now().year}-{n:03d}"

def next_ver_id(records_dir):
    existing = list(Path(records_dir / "verifications").glob("*.json"))
    n = len(existing) + 1
    return f"VER-{datetime.now().year}-{n:03d}"

def process_trace(trace, project_dir, dry_run):
    records_dir = project_dir / "qms" / "records"
    trace_id = trace.get("trace_id", "unknown")
    outcome = trace.get("outcome", "unknown")
    timestamp = trace.get("timestamp", datetime.now(timezone.utc).isoformat())
    slug = trace.get("task_description", "unknown")[:40].replace(" ", "-")

    if outcome == "fail":
        # Create NCR
        ncr_id = next_ncr_id(records_dir)
        ncr = {
            "ncr_id": ncr_id,
            "timestamp": timestamp,
            "trace_id": trace_id,
            "trigger": "execution_failure",
            "severity": trace.get("severity", "major"),
            "category": trace.get("failure_category", "unspecified"),
            "description": trace.get("task_description", ""),
            "agent": trace.get("agent", ""),
            "role": trace.get("agent_role", ""),
            "violation_detail": "",
            "root_cause": "",
            "root_cause_method": "",
            "capa_ref": "",
            "linked_records": [],
            "status": "open",
            "closed": None,
        }
        ncr_path = records_dir / "nonconformities" / f"{timestamp[:10]}-ncr-{slug}.json"
        if not dry_run:
            save_json(ncr_path, ncr)
            print(f"  NCR: {ncr_path.name}")
        else:
            print(f"  [DRY-RUN] NCR would be: {ncr_path.name}")

    elif outcome == "pass":
        # Create verification record
        ver_id = next_ver_id(records_dir)
        ver = {
            "ver_id": ver_id,
            "timestamp": timestamp,
            "trace_id": trace_id,
            "type": "inspection",
            "scope": "task",
            "result": "pass",
            "linked_requirements": [],
            "linked_tasks": [],
            "linked_specs": [],
            "score": trace.get("quality_score", None),
            "findings": [],
            "reviewer_agent": trace.get("agent", ""),
            "evidence_path": "",
        }
        ver_path = records_dir / "verifications" / f"{timestamp[:10]}-pass-{slug}.json"
        if not dry_run:
            save_json(ver_path, ver)
            print(f"  VER: {ver_path.name}")
        else:
            print(f"  [DRY-RUN] VER would be: {ver_path.name}")


def process_failure(failure, project_dir, dry_run):
    records_dir = project_dir / "qms" / "records"
    capa_dir = project_dir / "qms" / "capa" / "open"
    failure_id = failure.get("failure_id", "unknown")
    trace_id = failure.get("trace_id", "unknown")
    timestamp = failure.get("timestamp", datetime.now(timezone.utc).isoformat())
    slug = failure.get("root_cause", "unknown")[:30].replace(" ", "-").lower()

    # Create NCR if trace hasn't already (some failures may lack parent trace)
    ncr_id = next_ncr_id(records_dir)
    ncr = {
        "ncr_id": ncr_id,
        "timestamp": timestamp,
        "trace_id": trace_id,
        "trigger": failure.get("category", "execution_failure"),
        "severity": failure.get("severity", "major"),
        "category": failure.get("verifier_cause", ""),
        "description": failure.get("trace_summary", ""),
        "agent": "",
        "role": "",
        "violation_detail": failure.get("agent_behavior", ""),
        "root_cause": failure.get("root_cause", ""),
        "root_cause_method": "failure_signature",
        "capa_ref": "",
        "linked_records": [f"failure/{failure_id}"],
        "status": "open",
        "closed": None,
    }
    ncr_path = records_dir / "nonconformities" / f"{timestamp[:10]}-ncr-{slug}.json"

    # Create CAPA stub
    capa = {
        "capa_id": f"CAPA-{datetime.now().year}-{uuid.uuid4().hex[:6]}",
        "ncr_ref": ncr_id,
        "trace_id": trace_id,
        "opened": timestamp,
        "root_cause": failure.get("root_cause", ""),
        "action_type": "corrective",
        "action_taken": "",
        "affected_processes": [],
        "affected_skills": [],
        "evidence_paths": [],
        "verified_by": "",
        "verification_trace_id": "",
        "verification_note": "",
        "closed": None,
        "status": "pending",
    }
    capa_path = capa_dir / f"{timestamp[:10]}-capa-{slug}.json"

    if not dry_run:
        save_json(ncr_path, ncr)
        save_json(capa_path, capa)
        print(f"  NCR:  {ncr_path.name}")
        print(f"  CAPA: {capa_path.name}")
        # Update NCR with CAPA ref
        ncr["capa_ref"] = capa["capa_id"]
        save_json(ncr_path, ncr)
    else:
        print(f"  [DRY-RUN] NCR would be: {ncr_path.name}")
        print(f"  [DRY-RUN] CAPA would be: {capa_path.name}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sync self-harness data to QMS records")
    parser.add_argument("--project-dir", required=True, help="Project root containing self-harness/")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    harness_dir = project_dir / "self-harness"
    records_dir = project_dir / "qms" / "records"

    if not harness_dir.exists():
        print(f"No self-harness directory at {harness_dir}")
        sys.exit(1)

    # Ensure QMS directories exist
    for sub in ["nonconformities", "verifications", "requirements"]:
        (records_dir / sub).mkdir(parents=True, exist_ok=True)
    (project_dir / "qms" / "capa" / "open").mkdir(parents=True, exist_ok=True)

    # Process traces
    traces_dir = harness_dir / "traces"
    if traces_dir.exists():
        trace_files = sorted(traces_dir.glob("*.json"))
        print(f"Processing {len(trace_files)} traces...")
        for tf in trace_files:
            trace = load_json(tf)
            if trace:
                process_trace(trace, project_dir, args.dry_run)

    # Process failures
    failures_dir = harness_dir / "failures"
    if failures_dir.exists():
        failure_files = sorted(failures_dir.glob("*.json"))
        print(f"\nProcessing {len(failure_files)} failures...")
        for ff in failure_files:
            failure = load_json(ff)
            if failure:
                process_failure(failure, project_dir, args.dry_run)

    print("\nDone. Run without --dry-run to write records.")


if __name__ == "__main__":
    main()
