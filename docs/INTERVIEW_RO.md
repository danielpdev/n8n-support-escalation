# Pregătire pentru interviu — n8n Support Escalation

Roluri țintă: n8n / Support Automation.

## Prezentare de 90 de secunde

1. Explică problema concretă și cine folosește rezultatul.
2. Rulează `make demo` sau fluxul din UI.
3. Arată testul pentru un caz de eșec, apoi explică mecanismul din cod.
4. Spune ce limite are demonstrația și ce ai construi pentru producție.

Decizia de explicat: A deterministic classifier assigns route and SLA deadline. The workflow branches to on-call or support. A unique ticket/channel key prevents repeated delivery to the local inbox.

## Cinci întrebări

1. Cum alegi SLA-ul?
2. Cum previi duplicate la retry?
3. Ce faci cu clasificările greșite?
4. Cum testezi o ramură n8n?
5. Ce se întâmplă în afara programului?

## Exercițiu înainte de a aplica

Add business calendars, escalation timers and an authorized notification adapter.

Alege o parte mică a acestei modificări, implementeaz-o personal, adaugă un test care verifică comportamentul și descrie rezultatul într-un commit real. Nu declara că ai înțeles sau construit singur o parte pe care nu o poți explica.

## Checklist personal

- [ ] Pot porni proiectul dintr-un checkout curat.
- [ ] Pot urmări cererea până la rezultatul salvat.
- [ ] Pot explica diferența dintre fixture și model local.
- [ ] Pot demonstra un eșec și recuperarea lui.
- [ ] Am făcut o modificare proprie și o pot explica în engleză.

Aceste puncte necesită review-ul tău; nu au fost bifate automat.
