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

### Méthode 1 : Installation automatique via script (Recommandé)

1. **Téléchargez le script d'installation** :
   ```bash
   curl -O https://raw.githubusercontent.com/medbenk1/hass-habous/main/install.sh
   chmod +x install.sh
   ```

2. **Exécutez le script** :
   ```bash
   # Sur Home Assistant OS/Supervised (chemin par défaut)
   ./install.sh
   
   # Ou spécifiez le chemin de votre config
   export HOME_ASSISTANT_CONFIG=/path/to/config
   ./install.sh
   ```

3. **Configuration** :
   Ajoutez la configuration dans votre `configuration.yaml` :

```yaml
sensor:
  - platform: salat_time
    ville: 7  # ID de la ville (voir liste ci-dessous)
    scan_interval: 3600  # Optionnel, défaut: 3600 secondes
```

4. **Redémarrer** Home Assistant

### Méthode 2 : Installation manuelle via Git

```bash
# Se connecter à Home Assistant via SSH
cd /config

# Cloner le dépôt temporairement
git clone https://github.com/medbenk1/hass-habous.git temp_repo

# Copier le custom component
cp -r temp_repo/custom_components/salat_time custom_components/

# Nettoyer
rm -rf temp_repo
```

Puis ajoutez la configuration dans `configuration.yaml` et redémarrez Home Assistant.

### Méthode 3 : Installation manuelle (copie de fichiers)

1. Clonez le dépôt localement :
   ```bash
   git clone https://github.com/medbenk1/hass-habous.git
   ```

2. Copiez le dossier `custom_components/salat_time` dans votre Home Assistant :
   ```bash
   # Sur Home Assistant OS/Supervised
   cp -r custom_components/salat_time /config/custom_components/
   
   # Sur Home Assistant Core (Docker)
   cp -r custom_components/salat_time /path/to/homeassistant/config/custom_components/
   ```

3. Ajoutez la configuration dans `configuration.yaml` et redémarrez.

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

