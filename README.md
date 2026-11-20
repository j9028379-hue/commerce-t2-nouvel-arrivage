# COMMERCE-T2 · Nouvel arrivage

**Film sonore disponible : [regarder sur GitHub Pages](https://j9028379-hue.github.io/commerce-t2-nouvel-arrivage/film.html) · [quatre écoutes sur GitHub](https://github.com/j9028379-hue/commerce-t2-nouvel-arrivage/releases/tag/ecoutes-sonores-01).** Le master silencieux 02 reste intact.

- [Les six questions et leurs exemples](form/questions.json). Même ordre métier que T1 ; libellés T2 fournis par le propriétaire. Un seul article, prix et devise libres.
- [Les textes proposés pour les douze écrans](capture-guide/12-ecrans.md). Dans l'ordre : article entier, détails, utilisation, présentation finale. Chaque scène est guidée, enregistrée puis vérifiée.
- [Lot 01 : quatre films à regarder pour choisir les transitions](research/lot-01.md).

Transitions retenues : références **1 et 4**. [Contrat de montage](reverse-engineering/effets.json) · [analyse des effets](reverse-engineering/REPORT.md).

## Parcours à examiner

[Ouvrir le formulaire et les douze écrans](https://j9028379-hue.github.io/commerce-t2-nouvel-arrivage/) · [JSON des douze écrans](capture-guide/ecrans.json). Maquette de validation : chronomètres simulés, relecture facultative de fichiers locaux ; aucune capture caméra ni production de film. `python tools/construire.py` reconstruit la page autonome à partir des deux JSON.

## Sonorisation Sillon Studio — référence hébergée

Le workflow manuel **Voix, quatre musiques et conformité** repasse le formulaire et les quatre prises, compare 900 images reconstruites au master plein cadre, puis utilise le master approuvé sans réencodage vidéo. Les quatre voix WAV de ce **seul cas marchand** proviennent de la voix française synthétique choisie au deuxième duel. Le banc refuse un job différent au lieu de lui attribuer cette narration. Pas de synthèse automatique pour d'autres clients. Les quatre pistes sont approuvées ; les mixes restent soumis à l'écoute humaine. Aucune redistribution de MP3 brut. Les URL officielles et leurs SHA-256 figurent dans `audio/catalogue.json`.

Le Worker commun (`shared/cloudflare-control-plane/`) lit le catalogue : GET `/v1/catalogue` et `/v1/health`, pas d'écriture. Contrôle Wrangler **à blanc**, sans secret ni déploiement. Le canon reste local (`reverse-engineering/effets.json`). Le GitHub Runner réalise le montage. La rotation lit la branche dédiée `state/commerce-autoplay`; toute absence inattendue de l'état bloque le rendu. Après vérification et upload, un job distinct confirme la dernière piste par comparaison de révision ; pas d'avancement en cas d'échec du rendu. Les quatre variantes d'audition d'un même job ne sont pas quatre avancements.

`package/livrer.py verify FICHIER.zip` vérifie les empreintes et le manifeste sans installer le paquet. La preuve de conformité du runner couvre le cas Sillon Studio et les tests listés, pas Android physique, ni OTA signé, ni infrastructure Cloudflare en production.

**Autre commerçant, sans réseau.** `python render/marchand.py --job PRISES --out DOSSIER_NEUF --state etat.json --cache CACHE_MP3_PRIVE --id IDENTIFIANT_UNIQUE`. Le dossier `PRISES` contient `job.json` (contrat du navigateur) et `S1.mp4` à `S4.mp4` avec les empreintes correspondantes. Ce chemin lit la propre bande-son des prises, ou ne met que la musique si elles sont muettes. Il n'injecte pas la narration de Sillon Studio. Le cache est privé et préautorisé ; aucun MP3 original dans le ZIP. Le verrou local et la confirmation atomique persistent la sélection après succès ; les rendus hébergés de la démo ont en plus le registre Git commun entre runners. Une contre-épreuve avec d'autres réponses, une autre devise et de l'audio uniquement dans la prise 2 est exécutée sur GitHub.

**[Paquet et audit du deuxième rendu](https://github.com/j9028379-hue/commerce-t2-nouvel-arrivage/releases/tag/commerce-t2-v1.0.0)** · [preuves de rotation et de mixage](qc/preuves/).
