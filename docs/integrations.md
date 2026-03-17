# Intégrations à finaliser

## Email (agent `email`)
- Statut : agent déclaré mais non configuré (pas de compte lié).
- À fournir :
  - Adresse email et fournisseur (IMAP/SMTP ou API).
  - Identifiants ou token OAuth (à stocker via `openclaw secrets` si possible).
  - Dossier/scope à surveiller (inbox, label, etc.).
- Étapes :
  1. `openclaw email setup --provider <provider>` ou configuration manuelle dans `openclaw.json`.
  2. Tester via `openclaw email list --limit 5`.

## Calendrier (agent `calendrier`)
- Statut : agent déclaré mais désactivé.
- À fournir :
  - Compte Google/Microsoft ou ICS.
  - Credentials API/service account.
- Étapes :
  1. Configurer l’agent via `openclaw calendrier setup`.
  2. Vérifier `openclaw calendrier events --next 5`.

## WhatsApp outbound
- Symptôme : envoi impossible (« No active WhatsApp Web listener ») malgré `channels status` OK.
- Actions déjà tentées : relogin, restart gateway, doctor. Toujours KO.
- Recommandations :
  - Mettre à jour OpenClaw dès qu’un correctif WhatsApp est publié.
  - Ouvrir un ticket (#whatsapp sur Discord) avec les logs `openclaw logs --follow | grep whatsapp`.
  - En attendant, utiliser un autre canal (Signal/Telegram) pour les envois externes.
