# COMMERCE-T2 · Nouvel arrivage

**Étape : recherche de références — lot 01 proposé, non validé.** Aucun moteur, média de production, paquet stable ni déploiement OTA. Aucun changement à COMMERCE-T1. Le contrat de montage et son identité audio ne seront pas copiés de T1 par défaut.

- [Les six questions et leurs exemples](form/questions.json). Même ordre métier que T1 ; libellés T2 fournis par le propriétaire. Un seul article, prix et devise libres.
- [Les textes proposés pour les douze écrans](capture-guide/12-ecrans.md). Dans l'ordre : article entier, détails, utilisation, présentation finale. Chaque scène est guidée, enregistrée puis vérifiée.
- [Lot 01 : quatre films à regarder pour choisir les transitions](research/lot-01.md).

Après retour sur le lot : analyser les raccords retenus et leur faisabilité avec quatre prises ; soumettre les écrans et le contrat ; rendre le film silencieux. Valider ensuite quatre musiques, la voix et les mixes avec le propriétaire. La rotation inter-rendus, le contrôle d'architecture et la préparation du canon pour un futur catalogue feront l'objet de preuves propres à T2.

## Mise à jour — choix des transitions

Le propriétaire a retenu les références **1 et 4** exclusivement. [Effets et fenêtres en JSON](reverse-engineering/effets.json) · [Rapport d'adaptation en quatre prises](reverse-engineering/REPORT.md). Les paramètres proposés documentent l'aspect à reconstruire ; ce ne sont pas des réglages propriétaires exportés. Étape actuelle : adaptation à valider, moteur non développé.

## Parcours à examiner

[Ouvrir le formulaire et les douze écrans](https://j9028379-hue.github.io/commerce-t2-nouvel-arrivage/) · [JSON des douze écrans](capture-guide/ecrans.json). Maquette de validation : chronomètres simulés, relecture facultative de fichiers locaux ; aucune capture caméra ni production de film. `python tools/construire.py` reconstruit la page autonome à partir des deux JSON.

## Sonorisation Sillon Studio — référence hébergée

Le workflow manuel **Voix, quatre musiques et conformité** repasse le formulaire et les quatre prises, compare 900 images reconstruites au master plein cadre, puis utilise le master approuvé sans réencodage vidéo. Les quatre voix WAV de ce **seul cas marchand** proviennent de la voix française synthétique choisie au deuxième duel. Le banc refuse un job différent au lieu de lui attribuer cette narration. Pas de synthèse automatique pour d'autres clients. Les quatre pistes sont approuvées ; les mixes restent soumis à l'écoute humaine. Aucune redistribution de MP3 brut. Les URL officielles et leurs SHA-256 figurent dans `audio/catalogue.json`.

Le Worker commun (`shared/cloudflare-control-plane/`) lit le catalogue : GET `/v1/catalogue` et `/v1/health`, pas d'écriture. Contrôle Wrangler **à blanc**, sans secret ni déploiement. Le canon reste local (`reverse-engineering/effets.json`). Le GitHub Runner réalise le montage. La rotation lit la branche dédiée `state/commerce-autoplay`; toute absence inattendue de l'état bloque le rendu. Après vérification et upload, un job distinct confirme la dernière piste par comparaison de révision ; pas d'avancement en cas d'échec du rendu. Les quatre variantes d'audition d'un même job ne sont pas quatre avancements.

`package/livrer.py verify FICHIER.zip` vérifie les empreintes et le manifeste sans installer le paquet. La preuve de conformité du runner couvre le cas Sillon Studio et les tests listés, pas Android physique, ni OTA signé, ni infrastructure Cloudflare en production.
