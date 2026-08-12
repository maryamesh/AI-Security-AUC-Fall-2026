# STRIDE Reference — Attack-Chain Annotation

Use STRIDE after constructing the breach. Label each stage according to the
security property it violates.

## S — Spoofing

Did an actor or artifact pretend to be a trusted identity or source?

Examples:

- Student-supplied metadata claims Human Resources ownership
- Unverified document presented as official HR policy

## T — Tampering

Was content, metadata, context, or another security-relevant artifact
manipulated?

Examples:

- Attacker-controlled document enters the knowledge base
- Document content manipulates retrieval or model behavior

## R — Repudiation

Can an actor deny an action because evidence is missing?

Examples:

- Upload identity is absent
- Retrieved chunks are not logged
- Investigators cannot reconstruct the answer path

## I — Information Disclosure

Was restricted information exposed to an unauthorized recipient?

Example:

- HR content appears in the student's answer

## D — Denial of Service

Were availability, latency, capacity, or cost attacked?

This category may not be necessary for the shortest HR breach chain.

## E — Elevation of Privilege

Did an actor gain access or capability beyond their authorized role?

Example:

- A student role causes restricted HR content to enter its model context

## Path versus impact

Ask:

```text
Which categories describe the path?
Which category describes the final impact?
```

A defensible chain may include:

```text
Tampering → Spoofing → Elevation of Privilege → Information Disclosure
```

Do not add a category merely to use every STRIDE letter. Every label must point
to a specific step.
