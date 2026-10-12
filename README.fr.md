# ESPHome : contrôle Bluetooth local des hottes Best / Broan-NuTone

Contrôlez une hotte **Best HBN1306SS** (app « Best Kitchen ») depuis Home Assistant **sans nuage**, avec un ESP32 bon marché sous ESPHome.

Dans Home Assistant : ventilateur (4 vitesses), lumière (3 niveaux), SmartSense (mode automatique), arrêt différé, état de la connexion Bluetooth, modèle, signal Wi-Fi, boutons Redémarrer / Reconnecter. Les boutons de la hotte se reflètent tout de suite dans HA, et l'app du téléphone continue de marcher.

## Installation

1. Copier `best-hood.yaml` dans le dossier ESPHome.
2. Ajouter dans `secrets.yaml` : `wifi_ssid`, `wifi_password`, `best_hood_api_key`, `best_hood_ap_password`.
3. Mettre l'adresse Bluetooth de votre hotte dans `hood_mac` : installer une première fois, lire les journaux de l'ESP32 (la hotte apparaît sous le nom `BEST HBN1306SS` une fois réveillée), puis réinstaller.
4. Ajouter l'appareil dans Home Assistant (découvert automatiquement).

## Fonctionnement

1. **Annonce de réveil** : la hotte reste invisible tant qu'elle ne capte pas l'identifiant `0x5665` + `E4 D6 14 27 35 47`, que l'ESP32 diffuse en continu. Ces 6 octets ne sont **pas une adresse** : c'est une constante fixe inscrite dans l'app Best Kitchen, la même pour toutes les hottes et tous les téléphones (rien à changer).
2. **Chiffrement sans jumelage** (`no_bond`, Just Works), refait à chaque connexion : la hotte coupe la liaison si on lui demande d'enregistrer un jumelage.
3. **Valeurs** : un chiffre ASCII par caractéristique (voir le tableau du README anglais).

L'ESP32 n'écrit rien avant d'avoir reçu l'état de la hotte : un redémarrage de l'ESP32 n'éteint jamais la hotte.

## Limites connues

Testé sur **une** HBN1306SS (septembre 2026). On ne sait pas encore si l'annonce de réveil est la même pour toutes les hottes. Une mise à jour de la hotte pourrait changer le protocole. Signalez votre modèle (ça marche ou non) dans une « issue ».

Licence MIT — © 2026 WheapLabs. Aucun lien avec Best ou Broan-NuTone.
