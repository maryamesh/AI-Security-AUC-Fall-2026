# Lab 3 — AI Security Detective

## Case

**Incident #042: The Vacation Policy Breach**

An internal AI assistant disclosed sensitive HR information after an employee
asked:

```text
What is the company's vacation policy?
```

No administrator login was recorded. No employee directly queried the HR
database. Security logs show that the assistant invoked `employee_lookup`.

Your team is the incident-response group. Reconstruct the application from
evidence, determine what happened, identify the failed trust boundary, and
recommend controls.

Do not assume the cause before examining the evidence.

## Learning outcomes

After the investigation, you should be able to:

1. Reconstruct an AI-integrated application from traces and artifacts.
2. Identify every source that contributes to model context.
3. Distinguish valid data from authorized instructions.
4. Classify system prompts, users, documents, memory, and tool results by trust.
5. Identify a failed trust boundary precisely.
6. Trace retrieved content into a model decision and sensitive tool action.
7. Separate root cause, contributing conditions, impact, and false leads.
8. Map findings to professional AI-risk frameworks.
9. Produce a concise one-page incident/threat model.

## Safety

- This is a deterministic local simulation.
- All employee information is fictional.
- There is no real HR database or external model.
- Do not introduce real personal data.
- Do not test external applications.

## Setup

From `student-inlab-files`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Phase 1 — Explore the normal application

Do not request the incident evidence yet.

Use `POST /chat` for:

```text
What is the company's vacation policy?
What is the remote work policy?
What are the password requirements?
```

For each response:

1. Record its `request_id`.
2. Call `GET /trace/{request_id}`.
3. Identify each component shown in the trace.
4. Call `GET /documents`.
5. Build a provisional architecture from what you can prove.

Do not add components merely because a typical AI application might contain
them. Every component in your provisional architecture should have evidence.

## Phase 2 — Receive Incident #042

The TA will release Evidence A–F after the normal exploration.

Use:

```text
GET /trace/REQ-042
```

Compare the incident trace with a normal trace.

Your investigation must answer:

1. What did the employee request?
2. What additional data entered context?
3. Which source introduced instruction-like content?
4. Which tool was requested?
5. What sensitive information did it return?
6. Which information appeared in the final output?
7. Where did data begin influencing control flow?
8. Which deterministic application control was missing?

## Phase 3 — Build the detective board

Using only supported findings, reconstruct:

```text
Entry point
  ↓
Application/context construction
  ↓
Retrieved content
  ↓
Model decision
  ↓
Sensitive tool
  ↓
Tool result
  ↓
Final output
```

Mark:

- Assets
- Data sources
- Instruction sources
- Trust boundaries
- Sensitive actions
- Impact

## Phase 4 — Trust classification

Classify:

- System prompt
- User request
- Retrieved document
- Session memory
- Tool result
- Message from another agent

Use these categories:

- Trusted instruction
- Untrusted data
- Data that may influence future actions
- High-risk control input

One source may require more than one statement. For example, a tool result may
be trusted as data from a particular system while still not being trusted as an
instruction.

## Phase 5 — Separate the findings

Document:

### Root cause

The direct mechanism that produced the incident.

### Contributing conditions

Design choices that made the root cause possible or increased impact.

### Impact

The information or capability affected.

### False lead

An artifact that initially looks suspicious but does not explain the observed
tool path.

Do not use “prompt injection” as the entire root-cause statement. Explain the
complete mechanism.

## Phase 6 — Framework mapping

Use the assignment framework reference to communicate the finding through:

- OWASP guidance for LLM/GenAI applications
- MITRE ATLAS
- NIST AI RMF

Exact identifiers are less important than a justified conceptual mapping.

## Final lab output

Use your investigation notes to prepare the separate one-page AI Security
Incident Report described in `student-assignment`.

## Suggested sequence

```text
0–10 minutes   Trust classification discussion
10–20 minutes  Normal application exploration
20–30 minutes  Incident and evidence release
30–50 minutes  Evidence investigation
50–60 minutes  Attack-path reconstruction
60–70 minutes  Framework mapping
70–85 minutes  One-page report preparation
85–90 minutes  Debrief
```

## Final question

```text
In an AI application, what can the model interpret as an instruction?
```
