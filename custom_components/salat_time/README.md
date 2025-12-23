# Salat Time (Morocco) - Home Assistant Custom Component

Ce composant personnalisé pour Home Assistant récupère les horaires de prière depuis le site du Ministère des Habous et des Affaires Islamiques du Maroc.

## Installation

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
    ville: 7  # ID de la ville (7 = القنيطرة / Kenitra)
    scan_interval: 3600  # Intervalle de mise à jour en secondes (optionnel, défaut: 3600)
```

### Méthode 2 : Installation manuelle

1. Copiez le dossier `custom_components/salat_time` dans le répertoire `custom_components` de votre installation Home Assistant.
   - Chemin typique : `/config/custom_components/salat_time`

2. Redémarrez Home Assistant.

3. Ajoutez la configuration dans votre `configuration.yaml` :

```yaml
sensor:
  - platform: salat_time
    ville: 7  # ID de la ville (7 = القنيطرة / Kenitra)
    scan_interval: 3600  # Intervalle de mise à jour en secondes (optionnel, défaut: 3600)
```

## Configuration

### Paramètres

- **ville** (requis) : ID numérique de la ville marocaine
  - Exemples :
    - `1` = الرباط (Rabat)
    - `7` = القنيطرة (Kenitra)
    - `58` = الدار البيضاء (Casablanca)
    - `81` = فاس (Fes)
    - `104` = مراكش (Marrakech)
    - Voir la liste complète dans le code source

- **scan_interval** (optionnel) : Intervalle de mise à jour en secondes
  - Défaut : `3600` (1 heure)
  - Recommandé : Ne pas descendre en dessous de 3600 pour éviter de surcharger le serveur

## Entités créées

Le composant crée un sensor `sensor.salat_time` avec les attributs suivants :

- **État** : Nom de la prochaine prière
- **Attributs** :
  - `alfajr` : Heure ISO de la prière Al-Fajr
  - `alfajr_time` : Heure formatée (HH:MM) de Al-Fajr
  - `chourouq` : Heure ISO de Chourouq (lever du soleil)
  - `chourouq_time` : Heure formatée de Chourouq
  - `dhuhr` : Heure ISO de Dhuhr (midi)
  - `dhuhr_time` : Heure formatée de Dhuhr
  - `asr` : Heure ISO de Asr (après-midi)
  - `asr_time` : Heure formatée de Asr
  - `maghrib` : Heure ISO de Maghrib (coucher du soleil)
  - `maghrib_time` : Heure formatée de Maghrib
  - `ishae` : Heure ISO de Ishae (soir)
  - `ishae_time` : Heure formatée de Ishae
  - `next_prayer` : Nom de la prochaine prière
  - `next_prayer_time` : Heure ISO de la prochaine prière
  - `time_until_next` : Temps restant jusqu'à la prochaine prière

## Exemple d'utilisation dans les automations

```yaml
automation:
  - alias: "Notification avant Al-Fajr"
    trigger:
      - platform: time
        at: "{{ state_attr('sensor.salat_time', 'alfajr_time') }}"
    action:
      - service: notify.mobile_app
        data:
          message: "Il est temps pour Al-Fajr"
  
  - alias: "Notification avant Maghrib"
    trigger:
      - platform: time
        at: "{{ state_attr('sensor.salat_time', 'maghrib_time') }}"
    action:
      - service: notify.mobile_app
        data:
          message: "Il est temps pour Maghrib"
```

## Dépendances

- `beautifulsoup4 >= 4.14.0`
- `requests >= 2.32.0`

Ces dépendances sont installées automatiquement par Home Assistant.

## Dépannage

Si le sensor ne fonctionne pas :

1. Vérifiez les logs Home Assistant pour les erreurs
2. Vérifiez que l'ID de la ville est correct
3. Vérifiez votre connexion Internet
4. Vérifiez que le site https://www.habous.gov.ma est accessible

## Support

Pour signaler un problème ou proposer une amélioration, ouvrez une issue sur GitHub.

## Licence

MIT License

