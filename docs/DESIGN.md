# Design record

## Decision

A deterministic classifier assigns route and SLA deadline. The workflow branches to on-call or support. A unique ticket/channel key prevents repeated delivery to the local inbox.

## Failure model

Urgent routing, exact SLA boundary, incorrect-channel rejection and duplicate notification. The exported branch workflow executed in n8n.

## Tradeoffs

Rules are a transparent baseline, not an LLM classifier. The inbox is local; no Slack, email or real on-call person is contacted. SLA status is queried, not scheduled by a background monitor.

## Next change to defend in review

Add business calendars, escalation timers and an authorized notification adapter.

## Reproducibility

`uv.lock` pins Python dependencies; the web lockfile pins the React build where present. Model-backed evaluations use a separately installed local service. Dataset examples are synthetic and intentionally small. Reported timing is a local observation, not a throughput SLA. Run `make test` after changing state transitions and `make eval` after changing decisions. Keep inference quality separate from deterministic invariant checks.
