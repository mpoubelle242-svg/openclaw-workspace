# Mission Control — Procédure API

## Authentification
- **API Key** : `f155f04a198e8ca7361349530d44bf39d88d0e198f0537140a80b7f112423cc8`
- **Header** : `Authorization: Bearer <API_KEY>`
- **URL base** : `http://localhost:3000/api`

## Endpoints utiles

### Lister les tâches
```bash
curl -s -H "Authorization: Bearer $MC_KEY" "http://localhost:3000/api/tasks?limit=100"
```

### Mettre à jour une tâche (statut, assigné, etc.)
⚠️ **PATCH ne fonctionne pas** → utiliser **PUT**
```bash
curl -s -X PUT -H "Authorization: Bearer $MC_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status":"assigned"}' \
  "http://localhost:3000/api/tasks/<ID>"
```

### Statuts possibles
- `inbox` — créée, pas encore assignée
- `assigned` — assignée à un agent (prise en charge auto par la queue)
- `in_progress` — en cours de traitement par l'agent
- `review` / `quality_review` — en revue (⚠️ la queue ne prend PAS ces tâches)
- `done` — terminée

### ⚠️ Après un rejet aegis
Quand aegis rejette une tâche, elle passe en `review` ou `quality_review`.
**La queue ne reprend PAS ces statuts.** Il faut impérativement :
1. `PUT /api/tasks/<ID>` avec `{"status":"assigned"}`
2. Ajouter un commentaire avec les exigences corrigées

### Vérifier la queue d'un agent
```bash
curl -s -H "Authorization: Bearer $MC_KEY" \
  "http://localhost:3000/api/tasks/queue?agent=<NOM_AGENT>"
```

## Workflow Sprint → Tâches

1. **Vérifier les tâches du sprint** : `GET /api/tasks?limit=100` et filtrer sur le titre (ex: `QS-6.`)
2. **Assigner les tâches** : `PUT /api/tasks/<ID>` avec `{"status":"assigned"}`
3. **Les agents pollent la queue** et prennent les tâches automatiquement
4. **Notifier WhatsApp** à chaque assignation ET à chaque completion

## Mapping Agents
⚠️ **Les noms doivent correspondre exactement** (minuscules, sans accents)

| Tâche assigned_to | Agent OpenClaw |
|---|---|
| Développeur | `developpeur` |
| Testeur | `testeur` |
| Chef de Projet | `chef-de-projet` |
| Data Scientist | `data-scientist` |
| Research | `research` |

**Toujours utiliser le nom OpenClaw** (colonne droite) dans `assigned_to`.

## Règles à suivre TOUJOURS
1. ✅ Passer par l'API Mission Control pour assigner les tâches
2. ✅ Utiliser PUT (pas PATCH) pour les updates
3. ✅ Notifier WhatsApp à chaque assignation de tâche
4. ✅ Notifier WhatsApp à chaque tâche terminée
5. ✅ NE PAS faire le travail moi-même — les agents le font via la queue
6. ✅ Chaque agent DOIT ajouter un commentaire précis dans la tâche détaillant ce qu'il a fait (fichiers créés, endpoints ajoutés, tests passés, etc.)
7. ✅ Notifier WhatsApp IMMÉDIATEMENT à chaque tâche terminée (done) OU rejetée (quality_review/review rejeté par aegis)
8. ✅ VÉRIFIER le commit git avant de notifier "terminé" — si pas de commit = faux positif = repasser en assigned

---
*Dernière mise à jour : 2026-03-17*
