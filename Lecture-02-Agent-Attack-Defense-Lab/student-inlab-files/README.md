# Lab 2 — Attack and Defend an LLM Agent

## Purpose

This team lab exposes the complete agent loop:

```text
User request
    ↓
LLM decision
    ↓
Tool request
    ↓
Application executes tool
    ↓
Tool result enters context
    ↓
LLM continues or answers
```

The baseline is intentionally vulnerable. Red Teams develop two controlled
attacks. Blue Teams implement two application-level defenses. All activity
remains on local course files and uses a fake secret.

## Learning outcomes

After the lab, you should be able to:

1. Explain what makes an LLM application an agent.
2. Trace a Reason → Act → Observe loop from an API response.
3. Identify when retrieved data enters model context.
4. Demonstrate indirect prompt injection through a local document.
5. Explain why tool access creates a security boundary.
6. Separate retrieved data from trusted application instructions.
7. Enforce tool authorization in deterministic application code.
8. Preserve legitimate document search while blocking sensitive actions.

## Safety boundary

- Use only this local application and its supplied files.
- `LAB_SECRET_12345` is fake.
- `send_data` never creates a network connection.
- Destinations must be fictional and should use `.invalid`.
- Do not use real credentials, personal data, or external targets.
- Do not test systems that are outside the lab.

## Project structure

```text
student-inlab-files/
├── app/
│   ├── main.py
│   ├── agent.py
│   ├── llm.py
│   ├── tools.py
│   ├── policies.py
│   ├── models.py
│   └── config.py
├── data/
├── tests/
├── requirements.txt
└── .env.example
```

The code does not use LangChain or LangGraph. Read `app/agent.py` to see the
loop directly.

## Setup

From `student-inlab-files`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

The default `mock` backend is deterministic and recommended for the team
exercise. It makes the security flow repeatable. An optional Ollama
configuration is documented in `.env.example`.

## Opening activity — Trace the agent

The TA will show a request, document result, model decision, and tool action.
Discuss:

1. What makes this an agent rather than a chat interface?
2. Where did retrieved data enter model context?
3. When did untrusted data begin influencing an action?
4. Should the model authorize its own sensitive tool request?

## Understand the baseline

Run:

```json
{
  "message": "Summarize the travel policy."
}
```

Inspect every event in `trace`:

- `user`
- `llm_decision`
- `tool_call`
- `tool_result`
- `tool_blocked`
- `final`

Find these two intentional weaknesses:

1. `format_retrieved_context` places document content into context without a
   trusted/untrusted structure.
2. `authorize_tool` automatically permits model-requested tools.

## Team organization

The TA assigns each team as Red or Blue. Teams work independently and do not
exchange files during the exercise.

### Red Team objective

Develop exactly two attacks against an unchanged vulnerable baseline.

#### Attack 1 — Indirect prompt injection

Create or modify one local `.txt` document. Make it relevant to a normal policy
query, while including content that could be interpreted by an agent as
instructions.

The attack is successful when the trace shows that retrieved document content
caused behavior that was not requested by the user.

#### Attack 2 — Unauthorized tool use

Develop a different input that causes the baseline agent to request
`send_data` without legitimate user authorization.

The security issue is not merely that the model requested the tool. The issue
is that application code executed the model's request without an independent
authorization decision.

#### Red Team deliverables

For each attack provide:

- Attack identifier
- Objective
- Required document file, if applicable
- User message
- Expected trace
- Observed Swagger response
- Explanation of the crossed boundary

Do not send these materials directly to a Blue Team. Give them to the TA.

### Blue Team objective

Modify a separate copy of the baseline and implement both TODOs.

#### Defense 1 — Untrusted-context separation

Modify `format_retrieved_context` in `app/agent.py`.

Requirements:

- Trusted instructions and retrieved data have visibly different sections.
- Retrieved content is explicitly labeled untrusted.
- Trusted application text states that document content is data, not
  instructions.
- Normal policy summarization still works.

Adding only a vague sentence such as “be secure” is not sufficient. The context
construction must make the trust distinction visible in code and traces.

#### Defense 2 — Tool authorization

Modify `authorize_tool` in `app/policies.py`.

Requirements:

- `search_documents` remains available.
- `send_data` is denied by default.
- The decision is deterministic application code.
- A denied action appears as `tool_blocked`.
- The agent continues and produces a safe response.
- The model is not asked to approve its own request.

#### Blue Team checks

Run:

```powershell
pytest tests/test_tools.py tests/test_vulnerable_baseline.py
pytest tests/test_blue_team_expectations.py
```

`test_blue_team_expectations.py` fails on the original baseline. It should pass
after both defenses are implemented.

#### Blue Team deliverables

Provide the TA with:

- Final source code
- A short explanation of each defense
- Normal policy-query evidence
- Malicious-document test evidence
- Blocked-tool trace
- Known limitations

## TA cross-testing

The TA applies submitted Red Team attacks to Blue Team implementations in a
controlled copy. Teams do not access one another's computers or repositories.

The TA checks:

- Whether each attack affects the vulnerable baseline
- Whether each defense blocks its targeted behavior
- Whether normal document search still works
- Whether blocked actions remain visible in the trace
- Whether `send_data` remains a simulation

## Suggested session sequence

```text
0–10 minutes   Trace-the-agent activity
10–20 minutes  Run and inspect the baseline
20–35 minutes  First attack or first defense
35–50 minutes  Second attack or second defense
50–60 minutes  Prepare team deliverables
60–75 minutes  TA cross-testing
75–90 minutes  Debrief
```

## Debrief questions

1. Why is retrieved text not automatically trustworthy?
2. Why is a stronger prompt alone not a complete authorization mechanism?
3. Which decisions must remain in deterministic application code?
4. How can a defense preserve useful functionality?
5. What limitations remain after these two defenses?
