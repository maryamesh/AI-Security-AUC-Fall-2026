# CASE FILE — NORA Architecture

## Northbridge University

Northbridge University operates **NORA — Northbridge Online Research
Assistant**. Students and employees ask natural-language questions across:

- Student policies
- Scholarship policies
- Faculty policies
- Research documents
- Human Resources documents
- IT documentation

The university states that users can access only information appropriate for
their role. A student account must never receive restricted HR content.

## Query flow

```text
                         ┌──────────────┐
                         │   STUDENT    │
                         │   ACCOUNT    │
                         └──────┬───────┘
                                │ Question
                                ▼
                       ┌──────────────────┐
                       │     RAG API      │
                       │ Authentication   │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │    RETRIEVER     │
                       │ Semantic search  │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   VECTOR STORE   │
                       │ Student docs     │
                       │ Faculty docs     │
                       │ Research docs    │
                       │ HR docs          │
                       └────────┬─────────┘
                                │ Retrieved chunks
                                ▼
                       ┌──────────────────┐
                       │       LLM        │
                       │ System prompt    │
                       │ User question    │
                       │ Retrieved data   │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │      ANSWER      │
                       └────────┬─────────┘
                                │
                                ▼
                              STUDENT
```

## Separate document-ingestion flow

```text
University staff / users
          │
          ▼
┌──────────────────┐
│ Document upload  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Document parser  │
│ Chunk + metadata │
│ Embedding        │
└────────┬─────────┘
         │
         ▼
   Vector store
```

## Architecture review

Mark at least four trust boundaries:

```text
TB-1: _______________________________________________

TB-2: _______________________________________________

TB-3: _______________________________________________

TB-4: _______________________________________________
```

For each boundary state:

- Components on each side
- Data crossing
- Who controls the data
- Security decision required

The architecture is functionally correct. Your task is to determine which
interactions are insecure.
