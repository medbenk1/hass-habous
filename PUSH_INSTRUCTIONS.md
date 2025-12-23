# Instructions pour pousser sur GitHub

Le dépôt Git est prêt avec tous les fichiers commités. Pour pousser sur GitHub, vous avez plusieurs options :

## Option 1 : Utiliser un Personal Access Token (Recommandé)

1. **Créer un Personal Access Token sur GitHub** :
   - Allez sur https://github.com/settings/tokens
   - Cliquez sur "Generate new token" → "Generate new token (classic)"
   - Donnez un nom (ex: "hass-habous")
   - Sélectionnez les permissions : `repo` (accès complet aux dépôts)
   - Cliquez sur "Generate token"
   - **Copiez le token** (vous ne pourrez plus le voir après)

2. **Pousser avec le token** :
   ```bash
   cd /Users/mohammedbenkirane/perso-dev/salate-time
   git push -u origin main
   ```
   Quand il demande le mot de passe, utilisez le **Personal Access Token** au lieu de votre mot de passe.

## Option 2 : Utiliser GitHub CLI (gh)

Si vous avez GitHub CLI installé :

```bash
gh auth login
gh repo set-default medbenk1/hass-habous
cd /Users/mohammedbenkirane/perso-dev/salate-time
git push -u origin main
```

## Option 3 : Configurer les credentials Git

```bash
# Supprimer les anciennes credentials
git credential-osxkeychain erase
host=github.com
protocol=https

# Puis pousser (il vous demandera vos nouvelles credentials)
cd /Users/mohammedbenkirane/perso-dev/salate-time
git push -u origin main
```

## Option 4 : Utiliser SSH (si vous avez une clé SSH configurée)

```bash
# Vérifier si vous avez une clé SSH
ls -la ~/.ssh/id_*.pub

# Si oui, changer l'URL remote
cd /Users/mohammedbenkirane/perso-dev/salate-time
git remote set-url origin git@github.com:medbenk1/hass-habous.git
git push -u origin main
```

## État actuel

✅ Dépôt Git initialisé
✅ Tous les fichiers ajoutés et commités
✅ Remote configuré : https://github.com/medbenk1/hass-habous.git
✅ Branche principale : `main`

Il ne reste plus qu'à authentifier et pousser !

