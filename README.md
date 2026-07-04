# QMS for AI

A Quality Management System (ISO 9001:2015-aligned) for AI-assisted software development.

## What This Is

This framework formalizes what many AI-assisted development workflows already do informally — write specs, break down tasks, implement incrementally, review exhaustively, record outcomes, and improve continually.

ISO 9001 asks: *Do you have a process? Do you follow it? Can you prove it?* This project answers yes to all three, structured as flat files in your repo.

## How It Works

```
                  ┌──────────────────┐
                  │  Quality Manual  │  ← ISO clauses 4–10
                  └────────┬─────────┘
                           │ maps to
                  ┌────────▼─────────┐
                  │ Process Mappings │  ← clause → skill → agent → record
                  └────────┬─────────┘
                           │ feeds
                  ┌────────▼─────────┐
                  │ Execution Traces │  ← every task leaves evidence
                  └────────┬─────────┘
                           │ on fail
                  ┌────────▼─────────┐
                  │  NCR → CAPA      │  ← root cause → fix → verify
                  └──────────────────┘
```

Three layers:
1. **Define** — quality manual, process mappings, role definitions
2. **Produce** — evidence records (traces, verifications, NCRs)
3. **Improve** — CAPA loop, pattern analysis, management review

## Dependency & Origin

This framework builds on existing skills and standards:

| Dependency | Role | Origin |
|------------|------|--------|
| **self-harness** | Trace + failure collection. Backbone of clause 9.1 (monitoring) and clause 10.2 (nonconformity). | [lidge-jun/self-harness](https://github.com/lidge-jun/self-harness) |
| **spec-driven-development** | Requirements → spec process. Covers clause 8.2 (requirements) and clause 8.3 (design). | [Agent Skills](https://github.com/anthropics/claude-code/tree/main/skills) |
| **incremental-implementation** | Thin-slice execution pattern. Covers clause 8.5 (production). | [Agent Skills](https://github.com/anthropics/claude-code/tree/main/skills) |
| **planning-and-task-breakdown** | Work decomposition. Covers clause 8.1 (operational planning). | [Agent Skills](https://github.com/anthropics/claude-code/tree/main/skills) |
| **code-review-and-quality** | Multi-axis review. Covers clause 9.2 (internal audit). | [Agent Skills](https://github.com/anthropics/claude-code/tree/main/skills) |
| **test-driven-development** | Verification-first. Covers clause 8.6 (release). | [Agent Skills](https://github.com/anthropics/claude-code/tree/main/skills) |
| **doubt-driven-development** | Adversarial review. Covers clause 9.2 (internal audit). | [Agent Skills](https://github.com/anthropics/claude-code/tree/main/skills) |
| **ISO 9001:2015** | The standard this QMS is aligned to. | [ISO](https://www.iso.org/standard/62085.html) |

These skills are part of the **OpenCode Agent Skills** collection and are designed to be loaded by AI coding agents at session start.

## Structure

```
qms/
├── quality-manual.md           # ISO 9001:2015 clauses 4–10
├── process-mappings.md         # clause → skill → agent → record mapping
├── templates/                  # JSON schemas for all record types
├── records/
│   ├── requirements/           # Requirement records (REQ-*)
│   ├── verifications/          # Test/review/audit results (VER-*)
│   ├── nonconformities/        # NCR records (NCR-*)
│   └── reviews/                # Management review reports (REV-*)
├── capa/
│   └── open/                   # Active CAPA records (CAPA-*)
├── trace-matrix.json           # Requirement → spec → code → test → verify
├── quality-manual.md           # The constitution
└── process-mappings.md         # Clause coverage

skills/
└── qms-recorder/SKILL.md       # Agent skill for QMS record creation

scripts/
└── sync_qms.py                 # Backfill records from existing self-harness data
```

## Quick Start

### 1. Copy into your project

```bash
git clone https://github.com/YOUR_USER/qms-for-ai.git
cp -r qms-for-ai/qms ./your-project/qms
cp -r qms-for-ai/skills ./your-project/.opencode/skills
```

### 2. Set up self-harness (clause 9.1)

self-harness captures traces and failures. Install it from the original repo, or use the built-in OpenCode skill.

### 3. Configure your AI agent

Add both skills to your agent's startup instructions:

```
~/.config/opencode/skills/self-harness/SKILL.md
~/.config/opencode/skills/qms-recorder/SKILL.md
```

### 4. Record as you work

After each task:
- Write a trace (self-harness)
- Write NCR if failure, verification if pass (qms-recorder)
- Update trace-matrix for new requirement chains

### 5. Backfill existing data

```bash
python qms-for-ai/scripts/sync_qms.py --project-dir ./your-project
```

### 6. Run management reviews

Periodically aggregate NCRs, CAPA status, and trace-matrix health into `qms/records/reviews/`.

## ISO 9001 Clause Coverage

| Clause | Status | How |
|--------|--------|-----|
| 4. Context | ✅ Defined | Quality Manual §3 |
| 5. Leadership | ✅ Defined | Quality Manual §4 |
| 6. Planning | ⚠️ Partial | Manual risk capture |
| 7. Support | ✅ Deployed | AGENTS.md + context-engineering |
| 8.1 Operational Planning | ✅ Deployed | planning-and-task-breakdown |
| 8.3 Design | ✅ Deployed | spec-driven-development |
| 8.5 Production | ✅ Deployed | incremental-implementation |
| 8.6 Release | ✅ Deployed | code-review-and-quality |
| 9.1 Monitoring | ✅ Deployed | self-harness traces |
| 9.2 Internal Audit | ✅ Deployed | doubt-driven-development |
| 9.3 Management Review | ⚠️ Manual | Periodic human review |
| 10.2 NCR/CAPA | ✅ Deployed | self-harness failures + QMS records |
| 10.3 Continual Improvement | ⚠️ Early | self-harness phases |

## License

MIT

## Acknowledgements

- **[lidge-jun/self-harness](https://github.com/lidge-jun/self-harness)** — Execution trace and failure recording infrastructure
- **OpenCode Agent Skills** — Skill-based workflow definitions
- **ISO 9001:2015** — The quality management standard this framework aligns to
- **oh-my-opencode-slim** — Prompt tuning and agent management layer
