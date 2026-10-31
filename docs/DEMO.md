# Demo walkthrough

## Start

```bash
make setup
make demo
make test
make eval
```

## What to show

A deterministic classifier assigns route and SLA deadline. The workflow branches to on-call or support. A unique ticket/channel key prevents repeated delivery to the local inbox.

## Failure case to discuss

Urgent routing, exact SLA boundary, incorrect-channel rejection and duplicate notification. The exported branch workflow executed in n8n.

## Evidence

Open the JSON evaluation report alongside the implementation. Distinguish synthetic fixture outputs, synthetic trace timing, actual elapsed evaluation time, and local model inference. Do not present a tiny test set as a production benchmark.

## Closing tradeoff

Rules are a transparent baseline, not an LLM classifier. The inbox is local; no Slack, email or real on-call person is contacted. SLA status is queried, not scheduled by a background monitor.

The repository's `docs/demo.webm` or `docs/demo.mp4`, when present, records the demonstration. A terminal replay is also available for focused projects as `docs/demo.cast`.
