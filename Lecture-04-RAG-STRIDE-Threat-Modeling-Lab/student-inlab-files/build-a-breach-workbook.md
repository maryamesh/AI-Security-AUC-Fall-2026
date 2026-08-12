# BUILD-A-BREACH — Team Engineering Workbook

Team:

Members:

## Instructions

1. Choose Retrieval Abuse or Context Manipulation.
2. Select only the facts needed for that route.
3. Arrange them into the shortest attack chain.
4. Explain every connection.
5. Add trust boundaries, assets, and STRIDE labels.

## Part 1 — Architecture and trust boundaries

Identify at least four trust boundaries.

| TB | Components | Data crossing | Controller | Required decision |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |

## Part 2 — Find the weak links

Classify each fact as necessary, helpful, irrelevant, or mainly investigative.

| Fact | Classification | Reason |
|---|---|---|
| A |  |  |
| B |  |  |
| C |  |  |
| D |  |  |
| E |  |  |
| F |  |  |
| G |  |  |
| H |  |  |
| I |  |  |
| J |  |  |

## Part 3 — Build the shortest breach

Choose one route:

```text
[ ] Retrieval abuse
    Question → semantic similarity → restricted retrieval → answer

[ ] Context manipulation
    Attacker document → retrieval → LLM context → instruction influence
    → disclosure
```

Use the minimum facts required for your selected route.

```text
Student account
  ↓
[Fact ___] ______________________________________
  ↓
[Fact ___] ______________________________________
  ↓
[Fact ___] ______________________________________
  ↓
[Fact ___] ______________________________________
  ↓
Restricted HR information reaches student
```

For every arrow cite its system fact, trust boundary, and affected asset.

## Part 4 — Annotate with STRIDE

Add a STRIDE category only where a specific property is violated.

| Attack step | STRIDE category | Path or impact? | Evidence |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

Answer:

```text
Final impact category:

Categories that describe the path:
```

## Final engineering statement

```text
The most critical weakness is ______________________________ because
_____________________________________________________________________.
```
