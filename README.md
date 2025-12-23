# Salat Time - Home Assistant Custom Component

Composant personnalisé Home Assistant pour récupérer les horaires de prière depuis le site du Ministère des Habous et des Affaires Islamiques du Maroc.

## Structure du projet

```
salate-time/
├── custom_components/
│   └── salat_time/
│       ├── __init__.py          # Initialisation du composant
│       ├── manifest.json         # Métadonnées du composant
│       ├── const.py              # Constantes
│       ├── sensor.py             # Sensor principal
│       └── README.md             # Documentation du composant
├── .github/
│   └── workflows/
│       └── validate.yml          # Validation HACS
├── hacs.json                     # Configuration HACS
├── requirements.txt              # Dépendances Python
├── configuration.yaml.example    # Exemple de configuration
└── README.md                     # Ce fichier
```

## Installation dans Home Assistant

### Méthode 1 : Installation via HACS (Recommandé)

1. **Installer HACS** si ce n'est pas déjà fait : [Documentation HACS](https://hacs.xyz/docs/setup/download)

2. **Ajouter ce dépôt à HACS** :
   - Allez dans **HACS** → **Integrations**
   - Cliquez sur les **3 points** (⋮) en haut à droite
   - Sélectionnez **Custom repositories**
   - Ajoutez le dépôt :
     - **Repository**: `https://github.com/medbenk1/hass-habous`
     - **Category**: `Integration`
   - Cliquez sur **Add**

3. **Installer le composant** :
   - Recherchez "Salat Time (Morocco)" dans HACS
   - Cliquez sur **Download**
   - Redémarrez Home Assistant

4. **Configuration** :
   Ajoutez la configuration dans votre `configuration.yaml` :

```yaml
sensor:
  - platform: salat_time
    ville: 7  # ID de la ville (voir liste ci-dessous)
    scan_interval: 3600  # Optionnel, défaut: 3600 secondes
```

5. **Redémarrer** Home Assistant

### Méthode 2 : Installation manuelle

#### Étape 1 : Copier les fichiers

Copiez le dossier `custom_components/salat_time` dans votre installation Home Assistant :

```bash
# Sur Home Assistant OS/Supervised
cp -r custom_components/salat_time /config/custom_components/

# Sur Home Assistant Core (Docker)
cp -r custom_components/salat_time /path/to/homeassistant/config/custom_components/
```

#### Étape 2 : Installation depuis GitHub

```bash
# Se connecter à Home Assistant via SSH
cd /config
git clone https://github.com/medbenk1/hass-habous.git temp_repo
cp -r temp_repo/custom_components/salat_time custom_components/
rm -rf temp_repo
```

#### Étape 3 : Configuration

Ajoutez la configuration dans votre `configuration.yaml` :

```yaml
sensor:
  - platform: salat_time
    ville: 7  # ID de la ville (voir liste ci-dessous)
    scan_interval: 3600  # Optionnel, défaut: 3600 secondes
```

#### Étape 4 : Redémarrer

Redémarrez Home Assistant pour charger le composant.

## Liste des villes (ID)

Quelques exemples d'IDs de villes :

- `1` = الرباط (Rabat)
- `7` = القنيطرة (Kenitra)
- `14` = طنجة (Tanger)
- `58` = الدار البيضاء (Casablanca)
- `81` = فاس (Fes)
- `99` = مكناس (Meknes)
- `104` = مراكش (Marrakech)
- `117` = أكادير (Agadir)

Pour la liste complète, consultez le code source ou le site [habous.gov.ma](https://www.habous.gov.ma/prieres/horaire-api.php).

## Utilisation

Une fois installé, le composant crée un sensor `sensor.salat_time` avec :

- **État** : Nom de la prochaine prière
- **Attributs** : Tous les horaires de prière du jour

### Exemple dans les automations

```yaml
automation:
  - alias: "Notification Al-Fajr"
    trigger:
      - platform: time
        at: "{{ state_attr('sensor.salat_time', 'alfajr_time') }}"
    action:
      - service: notify.mobile_app
        data:
          message: "Il est temps pour Al-Fajr"
```


## Développement

### Dépendances

Les dépendances sont définies dans `requirements.txt` :

- `beautifulsoup4 >= 4.14.0`
- `requests >= 2.32.0`

### Installation des dépendances pour développement

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Documentation

Pour plus de détails sur l'utilisation du composant, consultez :
- [README du composant](custom_components/salat_time/README.md)
- [Exemple de configuration](configuration.yaml.example)

## Licence

MIT License

