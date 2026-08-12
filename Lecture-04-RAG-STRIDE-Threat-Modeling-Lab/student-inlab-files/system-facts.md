# SYSTEM FACTS — NORA

These are architecture facts, not pre-labeled vulnerabilities. Determine which
facts contribute to a plausible breach.

## Fact A — Document submission

Any authenticated university account can submit a document through the
knowledge-base upload portal.

## Fact B — Automatic indexing

Uploaded documents are automatically parsed, chunked, embedded, and added to
the vector store within five minutes. There is no manual review before they
become searchable.

## Fact C — Uploader-controlled metadata

The uploader supplies:

```text
department
document_type
author
access_group
```

The system accepts values such as:

```text
department = Human Resources
document_type = Internal Policy
access_group = HR
```

## Fact D — Semantic retrieval

NORA ranks documents using semantic similarity to the user's question:

```text
Question → embedding → vector similarity → top five documents
```

The user's role is not considered during ranking.

## Fact E — No retrieval authorization

After retrieval, the application does not check whether the current user is
authorized to access each selected document.

## Fact F — Context construction

Retrieved chunks are inserted into LLM context with the system prompt and user
question:

```text
SYSTEM PROMPT

USER QUESTION

RETRIEVED DOCUMENTS
```

The application does not enforce a strong distinction between document data
and trusted instructions.

## Fact G — LLM behavior

The LLM is instructed to answer using retrieved documents and may quote
relevant passages.

## Fact H — Output

NORA returns the LLM answer after basic formatting. No document-level
authorization check occurs before output.

## Fact I — Audit logging

Logs contain the user's question and final answer but not:

- Retrieved document identities
- Selected chunks
- Retrieval ranking
- Reasons for selection
- Context presented to the LLM

## Fact J — Existing HR documents

The shared vector store contains restricted documents including:

```text
HR_Salary_Bands_2026.pdf
HR_Employee_Benefits.pdf
HR_Compensation_Guidelines.pdf
HR_Leave_Policy.pdf
```

Students cannot directly access these files through the document repository.
