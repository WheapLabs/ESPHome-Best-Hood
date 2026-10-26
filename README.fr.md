# ESPHome : contrôle Bluetooth local des hottes Best / Broan-NuTone

Contrôlez une hotte **Best** (app « Best Kitchen ») depuis Home Assistant **sans nuage**, avec un ESP32 bon marché sous ESPHome.

## Modèles

| Modèle | Fichier | Ce qui marche en Bluetooth |
|---|---|---|
| **HBN1306SS** | `best-hood.yaml` | tout ce qui suit |
| **HBN65366SS** | `best-hood.yaml` | tout ce qui suit (testé dans la [PR n° 5](https://github.com/WheapLabs/esphome-best-hood/pull/5)) |
| **WCS1306SS** | `best-hood.yaml` | tout ce qui suit (testé dans l'[issue n° 1](https://github.com/WheapLabs/esphome-best-hood/issues/1), avec la version 1.0.1) |

Les trois modèles confirmés utilisent le même fichier, `best-hood.yaml`.

Avec `best-hood.yaml`, dans Home Assistant : ventilateur (4 vitesses), lumière (3 niveaux), SmartSense (mode automatique), arrêt différé, état de la connexion Bluetooth, modèle, signal Wi-Fi, boutons Redémarrer / Reconnecter. Les boutons de la hotte se reflètent tout de suite dans HA, et l'app du téléphone continue de marcher.

## Installation

1. Copier `best-hood.yaml` dans le dossier ESPHome.
2. Ajouter dans `secrets.yaml` : `wifi_ssid`, `wifi_password`, `best_hood_api_key`, `best_hood_ap_password`.
3. Mettre l'adresse Bluetooth de votre hotte dans `hood_mac` : installer une première fois avec l'adresse d'exemple, puis lire les journaux de l'ESP32 pendant une minute. Tant qu'il n'est pas connecté, il affiche chaque hotte dont le nom commence par `BEST`, par exemple `[I][hood]: Found 'BEST WCS1306SS' at XX:XX:XX:XX:XX:XX`. Copier cette adresse dans `hood_mac` et réinstaller. D'ici là, les lignes `status=133` sont normales. Raccourci : sur notre HBN1306SS, l'adresse Bluetooth = l'adresse Wi-Fi de la hotte + 2. Rien n'apparaît ? Rapprocher l'ESP32 de la hotte et fermer l'app Best Kitchen pendant le test.
4. Ajouter l'appareil dans Home Assistant (découvert automatiquement).

## Fonctionnement

1. **Annonce de réveil** : la hotte reste invisible tant qu'elle ne capte pas l'identifiant `0x5665` + `E4 D6 14 27 35 47`, que l'ESP32 diffuse en continu. Ces 6 octets ne sont **pas une adresse** : c'est une constante fixe inscrite dans l'app Best Kitchen, la même pour toutes les hottes et tous les téléphones (rien à changer).
2. **Chiffrement sans jumelage** (`no_bond`, Just Works), refait à chaque connexion : la hotte coupe la liaison si on lui demande d'enregistrer un jumelage.
3. **Valeurs** : un chiffre ASCII par caractéristique (voir le tableau du README anglais).

L'ESP32 n'écrit rien avant d'avoir reçu l'état de la hotte : un redémarrage de l'ESP32 n'éteint jamais la hotte.

## Limites connues

Testé sur **une** HBN1306SS (septembre 2026), **une** WCS1306SS (octobre 2026, [issue n° 1](https://github.com/WheapLabs/esphome-best-hood/issues/1)) et **une** HBN65366SS (octobre 2026, [PR n° 5](https://github.com/WheapLabs/esphome-best-hood/pull/5)). L'annonce de réveil marche sur les deux modèles. ESPHome écrit « Cannot poll, not connected » pour une caractéristique que la hotte n'a pas, même quand la connexion va bien. Il l'écrit aussi pour une caractéristique que l'ESP32 ne *voit* pas : par défaut, ESP-IDF ne garde que 40 caractéristiques GATT et ignore les autres sans prévenir. Une hotte Best peut en avoir plus (54 sur une HBN65366SS, dont `21026` et `21050`). `best-hood.yaml` fixe `CONFIG_BT_GATTC_MAX_CACHE_CHAR: "100"` : c'est ce qui a rendu la WCS1306SS complète (ventilateur 4 vitesses, lumière avec curseur continu calé sur ses niveaux, arrêt différé, SmartSense). Une ancienne copie du fichier a besoin de cette ligne. Une mise à jour de la hotte pourrait changer le protocole. Signalez votre modèle (ça marche ou non) dans une « issue ».

## Contribuer

Les issues et les pull requests sont bienvenues. Travaillez sur une branche, donnez à la pull request
un titre en anglais `type(scope): summary`, remplissez le [modèle](.github/pull_request_template.md)
et ajoutez une ligne au [CHANGELOG.md](CHANGELOG.md) sous `## [Unreleased]`. L'historique des
changements est dans [CHANGELOG.md](CHANGELOG.md).

Licence MIT — © 2026 WheapLabs. Aucun lien avec Best ou Broan-NuTone.
