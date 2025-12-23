# Installation du Blueprint KNX pour Salat Time

Ce blueprint permet d'envoyer automatiquement les horaires de prière sur le bus KNX.

## Installation

### Méthode 1 : Via l'interface Home Assistant (Recommandé)

1. **Téléchargez le fichier blueprint**
   - Téléchargez `blueprint.yaml` depuis le dépôt GitHub
   - Ou copiez son contenu

2. **Importez le blueprint**
   - Allez dans **Paramètres** → **Automations & Scènes**
   - Cliquez sur l'onglet **Blueprints**
   - Cliquez sur **IMPORTER UN BLUEPRINT** en bas à droite
   - Collez le contenu du fichier `blueprint.yaml` ou importez le fichier

3. **Créez une automation depuis le blueprint**
   - Cliquez sur **CRÉER UNE AUTOMATION**
   - Sélectionnez **Utiliser un blueprint**
   - Cherchez "Salat Time - Envoyer sur KNX"
   - Cliquez sur **UTILISER CE BLUEPRINT**

4. **Configurez les adresses GA**
   - Remplissez les champs avec vos adresses de groupe KNX :
     - **Adresse GA Alfajr** : `1/1/1` (ou votre adresse)
     - **Adresse GA Chourouq** : `1/1/2`
     - **Adresse GA Dhuhr** : `1/1/3`
     - **Adresse GA Asr** : `1/1/4`
     - **Adresse GA Maghrib** : `1/1/5`
     - **Adresse GA Ishae** : `1/1/6`
     - **Adresse GA Prochaine Prière** : `1/1/7`
   - **ID de la ville** : Laissez `7` par défaut (ou changez si nécessaire)

5. **Sauvegardez**
   - Donnez un nom à votre automation (ex: "Salat Time KNX")
   - Cliquez sur **CRÉER**

### Méthode 2 : Via le système de fichiers

1. **Copiez le fichier blueprint**
   ```bash
   cp blueprint.yaml /config/blueprints/automation/salat_time_knx.yaml
   ```

2. **Redémarrez Home Assistant**

3. **Créez l'automation depuis le blueprint** (voir Méthode 1, étape 3)

## Format des données

### Heures de prière
- **Format** : Minutes depuis minuit (0-1439)
- **Type KNX** : `DPTValue1Ucount` (16-bit unsigned)
- **Exemple** : `06:54` → `414` minutes (6×60 + 54)

### Prochaine prière
- **Format** : Code numérique (1-6)
- **Type KNX** : `DPTValue1Ucount`
- **Codes** :
  - `1` = Alfajr
  - `2` = Chourouq
  - `3` = Dhuhr
  - `4` = Asr
  - `5` = Maghrib
  - `6` = Ishae

## Fonctionnement

Le blueprint crée une automation qui :
1. **Se déclenche** quand les sensors Salat Time changent (mise à jour quotidienne)
2. **Envoie** automatiquement les valeurs sur le bus KNX
3. **Synchronise** toutes les valeurs au démarrage de Home Assistant

## Configuration des adresses GA

### Exemple de configuration

Si vos adresses GA sont dans le groupe `2/3/` :

- Alfajr : `2/3/10`
- Chourouq : `2/3/11`
- Dhuhr : `2/3/12`
- Asr : `2/3/13`
- Maghrib : `2/3/14`
- Ishae : `2/3/15`
- Prochaine Prière : `2/3/16`

### Configuration dans ETS

Dans ETS (Engineering Tool Software), créez des objets de données avec :
- **Type de données** : `DPT 5.010` (Value 1 Ucount) ou `DPT 7.001` (Unsigned 16-bit)
- **Adresses GA** : Correspondant à celles configurées dans le blueprint

## Test

Pour tester manuellement :

1. Allez dans **Paramètres** → **Automations & Scènes**
2. Trouvez votre automation créée depuis le blueprint
3. Cliquez sur les **3 points** (⋮) → **Déclencher**

Ou utilisez le service directement :

```yaml
service: knx.send
data:
  address: "1/1/1"
  payload: 414  # Pour 06:54
  type: "DPTValue1Ucount"
```

## Dépannage

### Le blueprint n'apparaît pas

1. Vérifiez que le fichier est dans `/config/blueprints/automation/`
2. Vérifiez la syntaxe YAML du fichier
3. Redémarrez Home Assistant
4. Vérifiez les logs pour les erreurs

### Les valeurs ne sont pas envoyées

1. Vérifiez que l'intégration KNX est active et fonctionnelle
2. Vérifiez que les adresses GA sont correctes
3. Vérifiez que les sensors Salat Time fonctionnent
4. Vérifiez les logs Home Assistant pour les erreurs

### Format incorrect

- Assurez-vous que votre équipement KNX supporte le type `DPTValue1Ucount`
- Vérifiez que les adresses GA sont bien configurées dans ETS avec le bon type de données

## Avantages du Blueprint

- ✅ **Réutilisable** : Créez plusieurs automations avec différentes adresses GA
- ✅ **Configurable** : Interface graphique pour la configuration
- ✅ **Maintenable** : Mise à jour facile du blueprint
- ✅ **Partageable** : Partagez facilement avec d'autres utilisateurs

## Partage

Pour partager ce blueprint avec d'autres utilisateurs :

1. Partagez le fichier `blueprint.yaml`
2. Ou partagez le lien GitHub du fichier
3. Les utilisateurs peuvent l'importer directement dans leur Home Assistant

