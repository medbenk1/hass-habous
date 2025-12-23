# Configuration KNX pour Salat Time

Ce guide explique comment envoyer les horaires de prière sur le bus KNX.

## Prérequis

1. **Intégration KNX installée** dans Home Assistant
2. **Configuration KNX** dans `configuration.yaml` ou via l'interface
3. **Adresses GA (Group Address)** configurées dans votre installation KNX

## Format des données

Deux formats sont disponibles :

### Format 1 : Minutes depuis minuit (DPTValue1Ucount)
- Valeur numérique de 0 à 1439
- Exemple : `06:54` = `414` minutes (6*60 + 54)
- Utilise le fichier : `knx_automations.yaml`

### Format 2 : Format Time KNX (DPTTime)
- Format standard KNX pour les heures
- Format : `HH:MM:SS`
- Utilise le fichier : `knx_automations_advanced.yaml`

## Installation

### Étape 1 : Choisir le format

Copiez l'un des fichiers d'automations dans votre configuration Home Assistant :

```bash
# Pour le format minutes (recommandé pour compatibilité)
cp knx_automations.yaml /config/automations/knx_salat.yaml

# OU pour le format Time KNX standard
cp knx_automations_advanced.yaml /config/automations/knx_salat.yaml
```

### Étape 2 : Configurer les adresses GA

Éditez le fichier et remplacez les adresses GA par défaut (`1/1/1`, `1/1/2`, etc.) par vos adresses :

```yaml
# Exemple avec vos adresses
address: "2/3/10"  # Alfajr
address: "2/3/11"  # Chourouq
address: "2/3/12"  # Dhuhr
# etc.
```

### Étape 3 : Ajouter les automations

Ajoutez le fichier dans votre `configuration.yaml` :

```yaml
automation: !include_dir_merge_list automations/
```

Ou importez-le directement dans l'interface Home Assistant :
- **Paramètres** → **Automations & Scènes** → **Automations**
- Cliquez sur les **3 points** (⋮) → **Importer**

## Adresses GA recommandées

| Prière | Adresse GA | Description |
|--------|------------|-------------|
| Alfajr | `1/1/1` | Heure de la prière Al-Fajr |
| Chourouq | `1/1/2` | Heure du lever du soleil |
| Dhuhr | `1/1/3` | Heure de la prière de midi |
| Asr | `1/1/4` | Heure de la prière de l'après-midi |
| Maghrib | `1/1/5` | Heure de la prière du coucher du soleil |
| Ishae | `1/1/6` | Heure de la prière du soir |
| Next Prayer | `1/1/7` | Code de la prochaine prière (1-6) |

## Codes de prière

Pour le sensor "Next Prayer", les codes sont :
- `1` = Alfajr
- `2` = Chourouq
- `3` = Dhuhr
- `4` = Asr
- `5` = Maghrib
- `6` = Ishae

## Fonctionnement

Les automations :
1. **Se déclenchent** automatiquement quand les sensors changent (mise à jour quotidienne)
2. **Envoient** les valeurs sur le bus KNX
3. **S'exécutent** également au démarrage de Home Assistant pour synchroniser les valeurs

## Test

Pour tester manuellement, vous pouvez déclencher une automation :

```yaml
service: automation.trigger
entity_id: automation.knx_send_alfajr
```

Ou utiliser le service directement :

```yaml
service: knx.send
data:
  address: "1/1/1"
  payload: 414  # Pour 06:54
  type: "DPTValue1Ucount"
```

## Dépannage

### Les valeurs ne sont pas envoyées

1. Vérifiez que l'intégration KNX est active
2. Vérifiez les logs Home Assistant pour les erreurs
3. Vérifiez que les adresses GA sont correctes
4. Vérifiez que les sensors Salat Time fonctionnent

### Format incorrect

- Si vous utilisez un format Time (DPTTime), assurez-vous que votre équipement KNX le supporte
- Sinon, utilisez le format minutes (DPTValue1Ucount)

## Exemple d'utilisation dans un visualiseur KNX

Si vous utilisez un visualiseur KNX (comme ETS), vous pouvez :
1. Créer des objets de données avec les adresses GA configurées
2. Utiliser le type de données approprié (DPT 5.010 pour minutes ou DPT 10.001 pour Time)
3. Afficher les valeurs dans votre interface

