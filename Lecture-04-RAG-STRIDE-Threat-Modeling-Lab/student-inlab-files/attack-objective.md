# SECURITY INCIDENT — HR FILES

Northbridge University's security team discovered that a student received
information from a confidential HR document through NORA.

Known facts:

- The student was not an HR employee.
- The student had no direct access to the HR repository.
- No administrator credentials were compromised.
- The student claims the question was normal.
- NORA's architecture operated as designed.

## Team mission

Construct a plausible attack path explaining how a normal student account could
cause NORA to reveal restricted HR information.

## Attacker constraints

The attacker:

- Has a normal authenticated student account
- Cannot steal administrator credentials
- Cannot log in as HR
- Cannot directly access the HR repository
- Cannot modify application source code
- May use only functionality described in the system facts

## Attack objective

```text
Obtain information contained in a restricted HR document through NORA.
```

## Your task

1. Choose Retrieval Abuse or Context Manipulation.
2. Select the necessary System Facts.
3. Put the facts in attack order.
4. Explain why each step enables the next.
5. Add trust boundaries, assets, and STRIDE labels.

The final step must explain how restricted HR information reaches the student.
Do not add capabilities that are absent from the architecture or facts.
