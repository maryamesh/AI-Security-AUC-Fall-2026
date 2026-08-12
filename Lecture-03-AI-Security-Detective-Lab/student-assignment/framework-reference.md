# Framework Reference for Incident #042

Frameworks evolve. Use the version assigned by the instructor and cite it.
Exact identifiers are optional unless the instructor provides a required
version.

## OWASP guidance for LLM/GenAI applications

Consider concepts related to:

- Prompt injection, including instructions arriving through external content
- Sensitive information disclosure
- Excessive agency or overpowered tool access
- Improper output handling and downstream exposure

Ask:

```text
Which application weakness allowed untrusted content to influence the model?
Which weakness allowed the resulting action or disclosure?
```

One incident may relate to more than one category.

## MITRE ATLAS

Use ATLAS to describe adversarial behavior and the attack path.

Look for concepts related to:

- Prompt injection
- Indirect influence through model inputs or data sources
- Abuse of model-integrated tools or capabilities
- Collection or exposure of sensitive information

Ask:

```text
What did the attacker-controlled source influence?
What action followed?
What information became exposed?
```

Do not invent a technique identifier. Use the assigned ATLAS reference and
justify the closest behavioral mapping.

## NIST AI RMF

Use the four functions as a risk-management communication map:

- **Govern:** roles, policies, accountability, and permitted tool use
- **Map:** system context, assets, actors, data flows, and trust boundaries
- **Measure:** tests, traces, indicators, and evidence about failure
- **Manage:** mitigations, monitoring, response, and residual risk

Incident #042 can involve all four functions. Identify the most relevant
activity for each recommendation.

## Mapping quality

A useful mapping explains:

```text
Observed evidence
  ↓
Framework concept
  ↓
Why the concept applies
  ↓
Engineering or risk-management action
```

A category name alone is not an explanation.
