# Lecture 1 Assignment Report

Name:

Student ID:

Model/backend:

## 1. API architecture

Explain the roles of:

- Swagger
- HTTP
- FastAPI
- The configured LLM backend

Include a simple data-flow diagram from request entry to generated response.

## 2. Annotated request

Paste one successful `/chat` request.

Annotate:

- HTTP method
- Endpoint
- Caller-controlled fields
- Validation constraints
- Message roles and context
- Validation constraints

## 3. Annotated response

Paste the corresponding response.

Annotate:

- Generated text
- Model
- Temperature
- Input tokens
- Output tokens
- Usage source
- Latency
- Finish reason

## 4. Controlled experiments

Summarize the temperature, system-message, and user-message experiments.

Describe:

- Similarities and differences
- Whether temperature 0 produced identical responses
- Whether higher temperature produced visible variation
- Why six runs are insufficient for broad statistical conclusions

## 5. Few-shot experiment

Paste or reference the few-shot evidence.

Explain:

- Where the example appeared in the message sequence
- How it became part of the context
- Whether the generated response followed the demonstrated format

## 6. Comparing `/chat` and `/compare`

Compare their request and response schemas.

Explain how `/compare` keeps messages constant while varying temperature.

Identify all caller-controlled fields and all server/model-generated fields.

## 7. Invalid-request exploration

Paste or reference the validation-error evidence.

Explain why the API rejected the request and whether it reached the model.

## 8. Connection to AI security

Explain why developers must understand message roles, context, sampling, and
generated output before assessing an LLM application's security.

## 9. Limitations

State at least three limitations, such as:

- Mock versus real model behavior
- Provider-specific token accounting
- Small experiment count
- Nondeterminism
- Differences between models

## 10. References

List documentation or external sources used.
