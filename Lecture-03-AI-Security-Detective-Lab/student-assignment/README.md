# Individual Assignment — AI Security Incident Report

## Objective

Produce a one-page incident/threat model for Incident #042. Communicate the
mechanism precisely enough that an engineering team could understand what
failed and where controls should be added.

Do not submit a chronological retelling of every clue. Synthesize the evidence.

## Required sections

### 1. Incident summary

Use no more than four sentences.

State:

- What the user requested
- What the system disclosed
- How the sensitive tool became involved
- The resulting impact

### 2. Attack path

Include a compact diagram:

```text
Entry point
  ↓
Retrieved content
  ↓
Instruction/data confusion
  ↓
Model tool request
  ↓
Sensitive tool result
  ↓
Output disclosure
```

Mark the failed trust boundary.

### 3. Assets

Identify the affected data and capabilities, such as:

- Employee HR record
- Salary information
- Leave balance
- Employee identity
- Tool access
- System instructions

### 4. Trust boundaries

Mark at least three relevant boundaries on the architecture. Explain what
crosses each boundary and how it should be treated.

### 5. Threats

Identify three distinct threats. For each state:

```text
Threat → Entry point → Missing control → Impact
```

Do not describe the entire incident only as “prompt injection.”

### 6. Mitigations

Provide one relevant mitigation for each threat. State where the mitigation
belongs:

- Before retrieval
- During context construction
- Before tool execution
- Before returning output
- In monitoring or incident response

Mention at least one limitation. A natural-language instruction to the model is
not a complete authorization mechanism.

### 7. Framework mapping

Map the findings conceptually to:

- OWASP guidance for LLM/GenAI applications
- MITRE ATLAS
- NIST AI RMF

Use `framework-reference.md`. Explain the relationship rather than listing a
name without justification.

## Submission

Submit one page containing:

1. Incident summary
2. Attack-path diagram
3. Assets
4. Trust boundaries
5. Three threats
6. Three mitigations
7. Framework mapping

An appendix is not required. Cite any external references used.

## Accuracy requirements

A strong report distinguishes:

- Root cause from contributing conditions
- Data validity from instruction authority
- Tool schema validation from authorization
- Retrieved content from trusted system instructions
- Sensitive tool results from safe user output
- Suspicious artifacts from evidence that explains the complete path
