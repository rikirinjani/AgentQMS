---
name: qms-recorder
description: Records QMS evidence — NCRs, verifications, requirements, CAPA records. Use in tandem with self-harness after every task. Trigger when self-harness trace or failure is written.
---

# QMS Recorder

Generates structured QMS records from execution output. Run after every task alongside `self-harness`.

## Integration with self-harness

self-harness already writes traces and failures. QMS Recorder extends each:

| self-harness action | QMS action |
|---------------------|------------|
| Trace written (pass) | Write verification record if applicable |
| Trace written (fail) | Write NCR |
| Failure with root cause | Write CAPA record |
| New requirement/spec | Write requirement record + update trace-matrix |

## Record writing rules

### 1. Write NCR on failure

When a self-harness failure is recorded AND the failure is a process violation (not an external error), also write:

```
qms/records/nonconformities/{timestamp}-ncr-{slug}.json
```

Fields to fill:
- `ncr_id`: `NCR-{YYYY}-{NNN}`
- `trigger`: one of `execution_failure`, `process_violation`, `role_violation`, `procedure_gap`
- `severity`: `critical` if blocked, `major` if incorrect output, `minor` if process deviation
- `trace_id`: link back to the parent trace
- `agent`, `role`: who/what caused it
- `root_cause`: use 5-Why or doubt-driven-review
- `status`: `open`

### 2. Write verification on test pass

When a test passes or a review approves, write:

```
qms/records/verifications/{timestamp}-{verdict}-{slug}.json
```

Fields:
- `ver_id`: `VER-{YYYY}-{NNN}`
- `result`: `pass`
- `linked_tasks`: which tasks are verified
- `linked_specs`: which specs are confirmed
- `evidence_path`: test log or review path

### 3. Write requirement from spec

When a spec is created, write:

```
qms/records/requirements/{timestamp}-{slug}.json
```

### 4. Update trace-matrix

After linking requirement → spec → task → test, update:

```
qms/trace-matrix.json
```

Append a new chain entry linking all parts.

## Record locations

All QMS records are written under `qms/` in the project root:

```
{project}/
├── qms/
│   ├── records/
│   │   ├── nonconformities/
│   │   ├── verifications/
│   │   ├── requirements/
│   │   ├── traces/          (symlink → self-harness/traces/)
│   │   └── reviews/
│   ├── capa/
│   │   ├── open/
│   │   └── closed/
│   ├── templates/           (JSON schemas)
│   ├── trace-matrix.json
│   ├── quality-manual.md
│   └── process-mappings.md
└── self-harness/
    ├── traces/
    ├── failures/
    └── proposals/
```

## NCR triggers checklist

Before closing a task, check:

- [ ] Trace written? → self-harness/traces/
- [ ] Was there a failure? → write NCR if yes
- [ ] Was there a test/review? → write verification if yes
- [ ] Was a new requirement introduced? → write requirement record
- [ ] Does trace-matrix need updating? → append chain

## Role violation detection

An NCR with trigger `role_violation` fires when an agent operates outside its authorized scope:

| Agent | Authorized | Violation if |
|-------|-----------|-------------|
| Coordinator | Write code | Doing research |
| Platform | Architecture, design | Writing implementation |
| Librarian | Research docs | Coding |
| Explorer | Scouting context | Making decisions |
| Oracle | Review, critique | Producing output |
| Fixer | Targeted fixes | Adding features |
| Designer | UI polish | Changing logic |
