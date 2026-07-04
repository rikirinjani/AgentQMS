# Quality Manual

**Document ID:** QM-001
**Version:** v0.1
**Date:** 2026-07-04
**Status:** Draft
**Classification:** Open Source

---

## 0. Scope

This Quality Manual defines the Quality Management System for AI-assisted software development using autonomous agents. It governs how agentic workflows are specified, executed, verified, recorded, and improved.

**Standard:** ISO 9001:2015 (clauses 4–10)
**Domain:** Agentic AI software development
**Applicable to:** All agents operating within this system — human and AI alike

---

## 1. Normative References

- ISO 9001:2015 — Quality Management Systems
- ISO 9000:2015 — Quality Management Systems (Fundamentals and Vocabulary)

---

## 2. Terms and Definitions

| Term | Definition |
|------|------------|
| Agent | An AI or human actor that performs work within the system |
| Spec | A documented requirement or specification |
| Trace | A structured record of an execution |
| NCR | Nonconformity Report — a record of a deviation from the defined process |
| CAPA | Corrective and Preventive Action — the lifecycle from finding a problem to verifying its fix |
| Skill | A documented procedure that defines how an agent should perform a specific task |

---

## 3. Context of the Organization (Clause 4)

### 4.1 Understanding the Organization
The system operates as an AI-assisted development environment. Work is specified by humans, decomposed by agents, executed iteratively, and verified independently.

### 4.2 Interested Parties
| Party | Interest |
|-------|----------|
| Human developers | Quality outputs, traceable decisions |
| AI agents | Clear procedures, bounded roles |
| Auditors | Evidence of conformance |
| Open source community | Reproducible process |

### 4.3 Scope of the QMS
All development activities executed by or with AI agents: specification, implementation, testing, review, documentation, and deployment.

### 4.4 Quality Management System and Processes
The QMS is implemented as:
- **Procedures:** Skills — one markdown file per process
- **Records:** Structured JSON files under `qms/records/`
- **Evidence:** Traces, verifications, NCRs, CAPAs
- **Governance:** This manual + Constitution (`self-harness/constitution.md`)

---

## 4. Leadership (Clause 5)

### 5.1 Leadership and Commitment
Human operators are responsible for approving the Quality Manual and any amendments.

### 5.2 Quality Policy
> We produce software through a documented, traceable, and continuously improving process. Every execution leaves evidence. Every failure triggers improvement. Every agent — human or AI — follows the same procedures.

### 5.3 Organizational Roles and Responsibilities
| Role | Responsibility | Scope |
|------|---------------|-------|
| **Orchestrator** | Delegates work, coordinates agents | Planning, oversight |
| **Explorer** | Scouts codebase, gathers context | Investigation |
| **Librarian** | Researches external documentation | Reference |
| **Coordinator** | Writes and implements code | Production |
| **Platform** | Researches architecture and systems | Design |
| **Oracle** | Reviews architecture and correctness | Verification |
| **Fixer** | Applies targeted fixes | Correction |
| **Designer** | Polishes UI/UX | Presentation |
| **Human (Lead)** | Approves specs, reviews, policy changes | Authority |

Each agent role has a defined scope. Operating outside scope without authorization is a nonconformity (clause 10.2).

---

## 5. Planning (Clause 6)

### 6.1 Actions to Address Risks and Opportunities
Risks are identified during spec development (see `spec-driven-development`)
and during planning (see `planning-and-task-breakdown`). Risks are recorded in the spec or task plan.

### 6.2 Quality Objectives and Planning
| Objective | Measure | Owner |
|-----------|---------|-------|
| Trace completeness | 100% of tasks produce a trace | Agent |
| Process conformance | 0 unaddressed NCRs | Human Lead |
| Continual improvement | Quarterly management review | Human Lead |

### 6.3 Planning of Changes
Changes to the Quality Manual, Constitution, or process definitions require human approval.

---

## 6. Support (Clause 7)

### 7.1 Resources
The system infrastructure (tools, context window, file system) must be adequate for each agent to execute its defined procedures.

### 7.2 Competence
Each agent is prompted with its role definition and applicable skills. Competence is verified through:
- Trace records showing correct execution
- Review outcomes (see `code-review-and-quality`)
- NCRs identifying capability gaps

### 7.3 Awareness
The Quality Manual and process mappings are available to all agents at session start.

### 7.4 Communication
Records flow: agent → `qms/records/` → human review. NCRs and CAPAs are reviewed by human.

### 7.5 Documented Information
| Category | Location | Controls |
|----------|----------|----------|
| Quality Manual | `qms/quality-manual.md` | Human-approve changes |
| Process definitions | `qms/process-mappings.md` + Skills | Version-controlled |
| Records | `qms/records/` | Timestamped, immutable |
| Templates | `qms/templates/` | Version-controlled |

---

## 7. Operation (Clause 8)

### 8.1 Operational Planning and Control
Every task begins with a plan. The plan specifies:
- **Requirement** — what is needed
- **Spec** — how it is defined
- **Task breakdown** — the steps
- **Verification criteria** — what proves it works

These map to: `spec-driven-development` → `planning-and-task-breakdown` → `incremental-implementation` → `test-driven-development`.

### 8.2 Requirements for Products and Services
Requirements originate from human input (see `interview-me`, `spec-driven-development`).
Each requirement is recorded as a requirement record (`qms/records/requirements/`).

### 8.3 Design and Development
Design follows spec-driven development:
1. Spec is written and approved
2. Tasks are broken down
3. Each task is implemented incrementally
4. Each increment is verified

### 8.4 Control of Externally Provided Processes
External dependencies (libraries, APIs, MCP servers) are documented in the spec or task plan.

### 8.5 Production and Service Provision
Production follows `incremental-implementation`:
- One slice at a time
- Each slice is compilable and tested
- Each slice produces a trace

### 8.6 Release of Products and Services
Code is released after:
- All tests pass
- Code review approves (`code-review-and-quality`)
- Optionally: adversarial review (`doubt-driven-development`)

### 8.7 Control of Nonconforming Outputs
Nonconforming outputs are recorded as NCRs (see 10.2).

---

## 8. Performance Evaluation (Clause 9)

### 9.1 Monitoring, Measurement, Analysis and Evaluation
| What | How | Record |
|------|-----|--------|
| Execution | Trace every task | `self-harness/traces/` |
| Failures | Record each failure | `self-harness/failures/` |
| Test results | Pass/fail per slice | `qms/records/verifications/` |
| Reviews | Multi-axis scores | `qms/records/verifications/` |

### 9.2 Internal Audit
Internal audits are performed periodically:
- **Per-cycle:** Adversarial review (`doubt-driven-development`, `code-review-and-quality`)
- **Periodic:** Trace-matrix completeness check
- **Triggered:** After significant NCR or process change

Each audit produces a record in `qms/records/reviews/`.

### 9.3 Management Review
Quarterly (or per-project-end) the following are reviewed by the Human Lead:
- NCR summary: count, severity, closure rate
- CAPA effectiveness: were fixes verified?
- Trace-matrix: any broken chains?
- Skill updates: any procedures need revision?
- Quality objectives: progress against targets

Each review produces a record in `qms/records/reviews/`.

---

## 9. Improvement (Clause 10)

### 10.1 General
Improvement is an ongoing activity. Every NCR, CAPA, and review feeds the improvement cycle.

### 10.2 Nonconformity and Corrective Action

**What triggers an NCR:**

| Category | Example |
|----------|---------|
| Execution failure | Bug, broken build, test failure |
| Process violation | Trace not recorded, role boundary crossed |
| Procedure gap | Spec missing, skipped review |

**NCR lifecycle:**
1. NCR opened (automatic or manual)
2. Root cause analysis performed
3. CAPA opened if correction is needed beyond the immediate fix
4. Action taken
5. Effectiveness verified
6. NCR closed

NCRs are stored in `qms/records/nonconformities/`.
CAPAs are stored in `qms/capa/`.

### 10.3 Continual Improvement
Continual improvement operates through self-harness:
1. **Collect:** Traces and failures accumulate (current phase)
2. **Analyze:** Patterns are identified in failure data
3. **Propose:** Improvement proposals are created (`self-harness/proposals/`)
4. **Approve:** Human reviews and approves proposals
5. **Apply:** Approved proposals update skills, prompts, or config
6. **Verify:** The change is traced and monitored

This cycle is governed by `self-harness/constitution.md` (Article IA: failure to record is itself a failure; proposals require human approval).

---

## Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| v0.1 | 2026-07-04 | System | Initial draft |
