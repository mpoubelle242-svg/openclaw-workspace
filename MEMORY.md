# MEMORY.md — Mémoire longue durée

## Résumé
Synthèse des informations importantes accumulées au fil du temps.
À lire et mettre à jour uniquement en session principale.

## Contacts
- Franck Veron : +33679545409 (WhatsApp, confiance partielle)

## Préférences utilisateur
- Langue : Français
- Style : Direct, concis
- Confirmation requise avant toute action externe irréversible

## Agents disponibles
- **main** — Le Patron (superviseur)
- **calendrier** — Calendrier
- **chef-de-projet** — Chef de Projet
- **data-scientist** — Data Scientist
- **developpeur** — Développeur
- **directeur-de-projet** — Directeur de Projet
- **email** — Email
- **files** — Files (gestion fichiers/documents)
- **research** — Research (recherche web)
- **testeur** — Testeur
- **whatsapp** — WhatsApp

## Mission Control — Procédure API
- **API Key** : `f155f04a198e8ca7361349530d44bf39d88d0e198f0537140a80b7f112423cc8`
- **Header** : `Authorization: Bearer <API_KEY>`
- **URL** : `http://localhost:3000/api`
- ⚠️ **PATCH ne marche pas** → utiliser **PUT** pour les updates
- **Doc complète** : `docs/mission-control-api.md`
- **Règle** : TOUJOURS passer par l'API MC pour assigner les tâches, jamais faire le travail soi-même
- **WhatsApp** : notifier à chaque assignation ET à chaque completion de tâche
- **Commentaire obligatoire** : chaque agent DOIT ajouter un commentaire précis dans la tâche détaillant ce qu'il a fait (fichiers créés/modifiés, endpoints ajoutés, tests passés, commits, etc.)
- **Rejet aegis** → tâche passe en `review`/`quality_review` → la queue NE LA REPREND PAS → il faut `PUT` en `assigned` manuellement

## Règles projet
- **TOUJOURS commit + push** après chaque modification sur le projet quantique-saas
- Branch: `feature/saas-platform`
- Backend: `PORT=4001 REDIS_URL="redis://:R3d1s_2026@localhost:6379"` (lancer avec export env vars)
- Redis Docker password: `R3d1s_2026`
- DB: PostgreSQL sur localhost:5432, password: `Qu4nt1qu3_2026!`
- Playwright installé pour tests E2E (v1.58.2)

## Sprints terminés
- QS-10 ✅ (typo, landing, dashboard, admin, audit visuel, fix auth/CORS/JSX)

## Sprint en cours
- QS-11 — Tests E2E Playwright (217-221)

## Historique important
- **17 mars 2026** : Fix majeur CORS (NEXT_PUBLIC_API_URL en dur), route login (/auth/login → /login), Redis auth, PORT backend conflit, JSX dupliqué