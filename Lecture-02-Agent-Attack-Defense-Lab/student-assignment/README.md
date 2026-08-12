# Individual Assignment — Threat Model and Secure a Support Agent

## Scenario

A university customer-support agent can:

```text
search_knowledge_base(query)
lookup_customer(customer_id)
create_support_ticket(customer_id, title, description)
```

The agent receives questions from users and retrieves articles from an internal
knowledge base. Some articles originated from external vendors. The
`lookup_customer` tool returns synthetic contact and account information.
`create_support_ticket` changes system state by creating a new record.

Assume:

- Users may be anonymous.
- Knowledge-base content can be outdated or attacker-influenced.
- Tool results enter the model context.
- The model can request any of the three tools.
- The initial design executes every valid model-generated tool request.
- All customer information in the assignment is fictional.

## Objective

Apply the security reasoning from the lab to a different agent. Identify trust
boundaries, design two attacks, and redesign the agent with application-level
defenses.

This is individual work. No attack should be executed against a real service.

## Part 1 — Architecture and trust boundaries

Create one diagram containing:

- User
- API/application
- LLM
- Knowledge base
- All three tools
- Synthetic customer data
- Tool results
- Final response

Mark:

- Trusted components
- Untrusted or partially trusted inputs
- Sensitive data
- State-changing actions
- Every location where data crosses a trust boundary

## Part 2 — Attack design

Design two distinct attacks.

### Attack 1: Indirect prompt injection

Explain:

- Attacker-controlled content
- How it becomes retrievable
- How it enters model context
- What instruction the model may interpret
- Which security boundary is crossed
- Potential effect

### Attack 2: Unauthorized tool use

Explain:

- The sensitive tool
- Why the user is not authorized for the action
- How the model could request the action
- Why schema-valid arguments are not the same as authorization
- Potential effect

Use only synthetic identifiers and data.

## Part 3 — Defense design

Design a defense for each attack.

For each defense explain:

- Where it is implemented
- Whether it acts before or after model generation
- Which trusted component enforces it
- Why it should reduce the attack
- What normal behavior must continue working
- At least one limitation or bypass possibility

At least one defense must be deterministic application code rather than a
natural-language instruction to the model.

## Part 4 — Secure architecture

Produce a revised diagram showing:

- Separation of trusted instructions and untrusted retrieved data
- Authorization between model tool requests and tool execution
- Customer-access checks
- Validation of tool arguments
- Audit events for sensitive actions
- The safe path when a tool request is denied

## Part 5 — Synthesis

Answer:

> Why is relying entirely on the LLM's system prompt insufficient for securing
> this agent?

Your answer should distinguish model behavior from application enforcement.

## Deliverables

Submit:

1. A two-to-three-page report
2. Original architecture diagram
3. Secure architecture diagram
4. Two attack paths
5. Two defense designs
6. Defense limitations
7. Final synthesis response

Use `report-template.md` if helpful.

## Boundaries

- Do not interact with a real customer-support system.
- Do not use real customer information.
- Do not provide executable malware or exfiltration code.
- Keep every tool and destination conceptual or simulated.
- Cite sources used.
