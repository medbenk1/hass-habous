# Guide de déploiement - Salat Time Home Assistant

## Prérequis

- Home Assistant installé et fonctionnel
- Accès au répertoire de configuration de Home Assistant (généralement `/config`)

## Déploiement

### Option 1 : Déploiement manuel (recommandé pour débuter)

1. **Copier les fichiers**

   ```bash
   # Depuis votre machine locale
   scp -r custom_components/salat_time user@homeassistant:/config/custom_components/
   
   # Ou si vous avez un accès direct au système
   cp -r custom_components/salat_time /config/custom_components/
   ```

2. **Vérifier la structure**

   La structure devrait être :
   ```
   /config/custom_components/salat_time/
   ├── __init__.py
   ├── manifest.json
   ├── const.py
   ├── sensor.py
   └── README.md
   ```

3. **Ajouter la configuration**

   Éditez `/config/configuration.yaml` et ajoutez :

   ```yaml
   sensor:
     - platform: salat_time
       ville: 7
       scan_interval: 3600
   ```

4. **Redémarrer Home Assistant**

   - Via l'interface : Paramètres → Système → Redémarrer
   - Via SSH : `ha core restart`

5. **Vérifier l'installation**

   - Allez dans Paramètres → Appareils et services
   - Cherchez "Salat Time" dans la liste
   - Vérifiez que le sensor `sensor.salat_time` apparaît dans les entités

### Option 2 : Déploiement via Samba/File Editor

1. Accédez à votre Home Assistant via Samba ou l'add-on File Editor
2. Naviguez vers `/config/custom_components/`
3. Créez le dossier `salat_time` si nécessaire
4. Copiez tous les fichiers du dossier `custom_components/salat_time/`
5. Suivez les étapes 3-5 de l'option 1

### Option 3 : Déploiement via Git (pour développement)

Si vous avez Git installé sur votre Home Assistant :

```bash
cd /config/custom_components
git clone https://github.com/votre-repo/salate-time.git salat_time
cd salat_time
# Suivez les étapes 3-5 de l'option 1
```

## Vérification

### Vérifier les logs

```bash
# Via SSH
tail -f /config/home-assistant.log | grep salat_time

# Ou via l'interface
Paramètres → Système → Logs
```

### Tester le sensor

1. Allez dans Paramètres → Appareils et services
2. Cliquez sur "Salat Time"
3. Vérifiez que le sensor affiche les horaires

### Vérifier les attributs

Dans l'interface de développement :

```yaml
# Dans Developer Tools → States
sensor.salat_time
```

Vous devriez voir :
- **State** : Nom de la prochaine prière
- **Attributes** : Tous les horaires de prière

## Dépannage

### Le composant n'apparaît pas

1. Vérifiez que les fichiers sont dans `/config/custom_components/salat_time/`
2. Vérifiez les permissions des fichiers
3. Vérifiez les logs pour les erreurs
4. Redémarrez Home Assistant

### Erreur "Platform not found"

1. Vérifiez que `manifest.json` est présent et valide
2. Vérifiez que `__init__.py` existe
3. Vérifiez les logs pour plus de détails

### Les horaires ne se mettent pas à jour

1. Vérifiez votre connexion Internet
2. Vérifiez que le site habous.gov.ma est accessible
3. Vérifiez les logs pour les erreurs de requête
4. Augmentez `scan_interval` si nécessaire

### Erreur de dépendances

Si vous voyez des erreurs concernant `beautifulsoup4` ou `requests` :

1. Redémarrez Home Assistant (les dépendances sont installées automatiquement)
2. Vérifiez que vous avez une connexion Internet
3. Vérifiez les logs pour plus de détails

## Mise à jour

Pour mettre à jour le composant :

1. Sauvegardez votre configuration actuelle
2. Remplacez les fichiers dans `/config/custom_components/salat_time/`
3. Redémarrez Home Assistant

## Désinstallation

1. Supprimez la configuration de `configuration.yaml`
2. Supprimez le dossier `/config/custom_components/salat_time/`
3. Redémarrez Home Assistant

