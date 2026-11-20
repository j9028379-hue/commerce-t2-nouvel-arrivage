# T2 comparé à Commerce-T1 : périmètre de conformité

Référence : Commerce-T1 `186e46a` (moteur, tests `cq_architecture.py` et `cq_preparation_catalogue.py`, intégration navigateur). Comparaison fonctionnelle, pas une affirmation que les schémas, les fichiers ou les API sont interchangeables.

| Exigence commune | T2 et preuve |
|---|---|
| Six réponses séparées du tournage | `form/questions.json` → réponses obligatoires → `render-job` ; aucune donnée de la démo préremplie. |
| Quatre scènes d’un article, douze étapes | Guide / enregistrement simulé ou import local / vérification par scène. Au terme du parcours avec quatre prises distinctes, le navigateur exporte le job : réponses, 12 écrans, quatre SHA-256. Le moteur vérifie les fichiers. |
| Réponses visibles au montage | 0–6 s : commerce + article ; 6–14 s : accroche puis prix libre ; 14–21 s : utilisation, sans texte commercial ; 21–30 s : commerce + quartier puis appel WhatsApp + numéro. |
| Canon, catalogue, contrats, référence visuelle | `catalogue/catalogue.json`, `reverse-engineering/effets.json`, `schemas/`, comparaison des 900 images au master silencieux 02. |
| Son propre au marchand, pas de narration de démo imposée | `render/marchand.py` et contre-épreuve GitHub avec de nouvelles réponses, un prix en nairas et l’audio d’une seule prise. Nécessite un cache musical privé vérifié et les dépendances du moteur. |
| Rotation après réussite et niveaux du mix | Quatre pistes, 10 000 décisions simulées, deux rendus GitHub confirmés (4 puis 1). L’essai en échec intermédiaire n’a pas avancé l’état. |
| Paquet contrôlé, adaptateur Cloudflare | ZIP avec manifeste et rejet d’une modification ; Worker lecture seule testé et assemblé à blanc, pas déployé. |

[Contrôle complet du montage](https://github.com/j9028379-hue/commerce-t2-nouvel-arrivage/actions/runs/44691013116) · [Contrôle isolé du job natif du navigateur](https://github.com/j9028379-hue/commerce-t2-nouvel-arrivage/actions/workflows/audit-parcours.yml) · [Validation propriétaire](../approvals/validation.md).

**Limite de la mise en ligne** : Pages sert le film, le formulaire, la simulation et l’export local du job. Il ne téléverse pas de vidéos et ne déclenche pas un rendu marchand. Le rendu GitHub de démonstration est déclenché séparément ; le moteur marchand reçoit un dossier de prises. Ni une caméra Android physique, ni un service public de dispatch authentifié, ni la distribution OTA ne sont certifiés. Le ZIP 1.0.0 reste le paquet historique ; l’export navigateur est une amélioration du site sur `main`.
