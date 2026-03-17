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
- **TOUJOURS commit + push** après chaque modification sur le projet quantique-saas
- **Toujours créer des tâches MC** pour les sprints et affecter aux bons agents

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
- **Règle** : TOUJOURS passer par l'API MC pour assigner les tâches
- **WhatsApp** : notifier à chaque assignation ET à chaque completion de tâche
- **Commentaire obligatoire** : chaque agent DOIT ajouter un commentaire précis dans la tâche
- **Rejet aegis** → tâche passe en review → la queue NE LA REPREND PAS → PUT en assigned manuellement
- **Projet Quantique-SAAS** : id=3 (pas le projet General id=1)

## Projet Quantique-SaaS

### Infrastructure
- **Frontend** : Next.js 14 sur port **3001** (dev mode)
- **Backend** : Fastify/Node.js sur port **4001** (lancer avec `PORT=4001`)
- **Mission Control** : Docker sur port **3000**
- **Redis Docker** : mot de passe `R3d1s_2026` (container `quantique-redis`)
- **Redis URL** : `redis://:R3d1s_2026@localhost:6379`
- **PostgreSQL** : localhost:5432, password: `Qu4nt1qu3_2026!`
- **DATABASE_URL** : `postgresql://quantique:Qu4nt1qu3_2026!@localhost:5432/quantique?schema=public`
- **JWT_SECRET** : `jwt_s3cr3t_k3y_quantique_2026_v3ry_l0ng_4nd_s3cur3`
- **Branche** : `feature/saas-platform`
- **Repository** : https://github.com/Yoann81/Quantique.git

### Lancement Backend (OBLIGATOIRE avec env vars)
```bash
cd /root/.openclaw/workspace/quantique-saas/app
export DATABASE_URL="postgresql://quantique:Qu4nt1qu3_2026!@localhost:5432/quantique?schema=public"
export REDIS_URL="redis://:R3d1s_2026@localhost:6379"
export JWT_SECRET="jwt_s3cr3t_k3y_quantique_2026_v3ry_l0ng_4nd_s3cur3"
export PORT=4001
export NODE_ENV=development
nohup npx tsx backend/src/index.ts > /tmp/backend4.log 2>&1 &
```

### Lancement Frontend
```bash
cd /root/.openclaw/workspace/quantique-saas/app/frontend
rm -rf .next
nohup npx next dev -p 3001 > /tmp/nextjs-frontend.log 2>&1 &
```

### Compte test
- Email : `test@test.com`
- Password : `Test123456!`

### Problèmes connus et leurs fixes
1. **Route login** : `/auth/login` → `/login` (double prefix avec `/api/auth`)
2. **CORS** : `NEXT_PUBLIC_API_URL=http://194.163.168.14:4001` en dur dans `.env` → supprimé, utiliser URLs relatives + proxy Next.js
3. **Tailwind JIT** : Next.js dev server ne génère pas toujours les classes responsive → ajouter manuellement les classes critiques dans `globals.css`
4. **Chunks JS 404** : Next.js dev server parfois ne sert pas les chunks → `rm -rf .next` + restart
5. **tailwind.config.ts** : Ne jamais supprimer (les agents l'ont fait une fois → page cassée)
6. **Framer-motion** : `useInView` ne se déclenche pas dans Playwright sans scroll → scroller avant screenshot
7. **JSON dupliqué JSX** : Agents ont ajouté des `</motion.p>` orphelines → vérifier après chaque modification agent
8. **tsx backend** : agents utilisent mauvais port → toujours spécifier `PORT=4001`
9. **tsconfig.tsbuildinfo** : fichier généré, mettre dans .gitignore

### Playwright E2E
- **Installé** : v1.58.2
- **Config** : `playwright.config.ts` (port 3001)
- **Tests** : `tests/e2e/*.spec.ts` (19 tests passent)
- **Lancer** : `cd app/frontend && npx playwright test --reporter=list`
- **Screenshots visuels** : `tests/e2e/visual-audit.spec.ts`
- **Rapports** : `RAPPORT_E2E_QS-11.md`, `RAPPORT_AUDIT_QS-10.7.md`

### Règles critiques pour agents
- **NE JAMAIS supprimer tailwind.config.ts**
- **NE JAMAIS supprimer postcss.config.js**
- **NE PAS modifier le port** (3001 frontend, 4001 backend)
- **Toujours commit + push** après modifications
- **Toujours ajouter commentaire MC** après completion
- **Ne pas décrire — agir** (écrire le code, ne pas dire ce qu'on ferait)

## Sprints terminés
- QS-10 ✅ — Typo, landing, dashboard, admin, audit visuel, fix bugs
- QS-11 ✅ — Tests E2E Playwright (19/19 passant)
- QS-12 ✅ — UX polish (icons, hover effects, empty states, spacing audit)
- QS-13 (partiel) — Fix chunks 404, responsive CSS workaround

## Historique important
- **17 mars 2026** : Journée productive — sprints QS-10 à QS-13, fix majeurs (CORS, route login, Tailwind JIT, chunks JS 404), Playwright installé, audit visuel complet
- Agent developpeur a supprimé tailwind.config.ts par accident → restauré
- Agent chef-de-projet n'a rien produit (faux positifs) → relancer avec instructions plus strictes
- Agents échouent quand trop de tâches → une seule tâche par agent, instructions courtes

## À faire
- QS-12.4/12.5 : icônes features landing + audit global (pas encore lancés correctement)
- QS-13 : fix complet du serveur (certains problèmes persistent)
- Traduire login/register en français (audit QS-10.7)
- Harmoniser tokens couleur (surface-* vs slate-*)
- Synchroniser mémoire dans tous les agents (ce fichier)
