# BOOTSTRAP.md — Initialisation

## Instructions
Ce fichier ne s'exécute qu'une seule fois au premier lancement.
Le supprimer après exécution.

## Étapes
1. Vérifier que `SOUL.md`, `USER.md`, `AGENTS.md` sont bien présents.
2. Appeler `agents.list` et mettre à jour la section Agents de `AGENTS.md`.
3. Créer le dossier `memory/` s'il n'existe pas.
4. Créer `memory/heartbeat-state.json` avec le contenu : `{}`.
5. Créer le fichier `memory/YYYY-MM-DD.md` du jour avec l'entrée : `# Initialisation terminée`.
6. Confirmer à l'utilisateur : "Le Patron est prêt."
7. Supprimer ce fichier.