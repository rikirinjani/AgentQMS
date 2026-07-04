# Process Mappings

**Document ID:** QM-002
**Version:** v0.1
**Date:** 2026-07-04
**Status:** Draft

---

Maps ISO 9001:2015 clauses to skills, agent roles, and record types.

---

## Clause 7.5 — Documented Information

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| `context-engineering` | Explorer | Rules files (CLAUDE.md, AGENTS.md) | Project root |
| `spec-driven-development` | Human + Agent | Spec document | `qms/records/specs/` |

**Possible NCRs:**
- Spec missing for a feature
- Rules file not maintained

---

## Clause 8.1 — Operational Planning and Control

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| `interview-me` | Oracle | Requirements clarification | `qms/records/requirements/` |
| `spec-driven-development` | Human + Agent | Spec document | `qms/records/specs/` |
| `planning-and-task-breakdown` | Orchestrator | Task list | `qms/records/tasks/` |

**Possible NCRs:**
- Task started without a plan
- Requirement not traced to spec

---

## Clause 8.3 — Design and Development

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| `context-engineering` | Explorer | Context summary | `self-harness/traces/` |
| `spec-driven-development` | Human + Agent | Spec document | `qms/records/specs/` |
| `incremental-implementation` | Coordinator | Implemented slice | Commit log + trace |

**Possible NCRs:**
- Code written without spec reference
- Slice not tested before next slice started

---

## Clause 8.5 — Production and Service Provision

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| `incremental-implementation` | Coordinator | Code + trace | Commit + `self-harness/traces/` |
| `test-driven-development` | Coordinator | Test results | `qms/records/verifications/` |
| `api-and-interface-design` | Coordinator | Interface definitions | Source code |

**Possible NCRs:**
- Agent role violation (Coordinator doing research instead of coding)
- Missing test for a new feature
- Trace not recorded after execution

---

## Clause 8.6 — Release of Products and Services

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| `code-review-and-quality` | Reviewer | Review report | `qms/records/verifications/` |
| `doubt-driven-development` | Oracle | Adversarial review | `qms/records/verifications/` |
| `test-driven-development` | Coordinator | Test results | `qms/records/verifications/` |

**Possible NCRs:**
- Code merged without review
- Review flagged issues not resolved before merge

---

## Clause 8.7 — Control of Nonconforming Outputs

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| `debugging-and-error-recovery` | Fixer | Root cause analysis | `self-harness/failures/` |
| `self-harness` (failure) | Any | NCR | `qms/records/nonconformities/` |

**Possible NCRs:**
- Bug not recorded as NCR
- Root cause not identified

---

## Clause 9.1 — Monitoring, Measurement, Analysis and Evaluation

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| `self-harness` (trace) | Any | Execution trace | `self-harness/traces/` |
| `test-driven-development` | Coordinator | Pass/fail results | `qms/records/verifications/` |

**Possible NCRs:**
- Trace omitted
- Test result not recorded

---

## Clause 9.2 — Internal Audit

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| `doubt-driven-development` | Oracle | Adversarial review | `qms/records/verifications/` |
| `code-review-and-quality` | Reviewer | Code review | `qms/records/verifications/` |

**Possible NCRs:**
- No review performed before release
- Review missed clearly identifiable issue

---

## Clause 9.3 — Management Review

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| None (manual process) | Human | Review report | `qms/records/reviews/` |

**Trigger:** Quarterly or per-project-end
**Inputs:** NCR summary, CAPA status, trace-matrix health, quality objectives

---

## Clause 10.2 — Nonconformity and Corrective Action

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| `self-harness` (failure) | Any | NCR | `qms/records/nonconformities/` |
| `self-harness` (proposal) | Any | CAPA proposal | `self-harness/proposals/` |
| `debugging-and-error-recovery` | Fixer | Root cause + fix | `qms/capa/` |

**Possible NCRs:**
- NCR opened but no CAPA created
- CAPA not verified for effectiveness

---

## Clause 10.3 — Continual Improvement

| Skill | Agent | Record Produced | Location |
|-------|-------|----------------|----------|
| `self-harness` (phase progression) | Human + Agent | Improvement proposals | `self-harness/proposals/` |
| `self-harness` (constitution) | Human | Governance evolution | `self-harness/constitution.md` |

**NCR Categories** (for role violations):

| Agent Role | Authorized Scope | Violation Example |
|------------|-----------------|-------------------|
| Orchestrator | Delegate, plan, coordinate | Writing code directly |
| Explorer | Scout codebase, gather context | Making architectural decisions |
| Librarian | Research docs, find references | Implementing code |
| Coordinator | Write and implement code | Doing research instead |
| Platform | Architecture, system design | Writing implementation code |
| Oracle | Review, analyze, critique | Producing production code |
| Fixer | Targeted bug fixes | Adding new features |
| Designer | UI/UX polish | Changing business logic |
| Human | Approve, decide, set policy | None — authority is unbounded |

---

## ISO Clause Coverage Summary

| Clause | Covered By | Status |
|--------|-----------|--------|
| 4. Context of the Organization | Quality Manual | Defined |
| 5. Leadership | Quality Manual + Constitution | Defined |
| 6. Planning | `planning-and-task-breakdown` | Partial |
| 7. Support | `context-engineering` | Partial |
| 8.1 Operational Planning | `spec-driven-development` | Deployed |
| 8.3 Design | `spec-driven-development` | Deployed |
| 8.5 Production | `incremental-implementation` | Deployed |
| 8.6 Release | `code-review-and-quality` | Deployed |
| 9.1 Monitoring | `self-harness` | Deployed |
| 9.2 Internal Audit | `doubt-driven-development` | Deployed |
| 9.3 Management Review | Manual process | Gap |
| 10.2 NCR/CAPA | `self-harness` failures | Partial |
| 10.3 Continual Improvement | `self-harness` phases | Early |
