# HEARTBEAT.md

## Comportement
- À chaque heartbeat, effectuer au moins une action utile.
- Vérifier dans l'ordre : emails, calendrier, notifications WhatsApp en attente.
- Si rien à signaler : répondre `HEARTBEAT_OK`.
- Consigner l'état dans `memory/heartbeat-state.json`.

## Fréquence
- Définie dans les Cron Jobs de l'agent.