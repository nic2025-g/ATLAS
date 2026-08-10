# 08 — Modèle Power BI ATLAS

## Présentation

Ce dossier documente le modèle de données Power BI construit à partir des 17 fichiers Excel normalisés issus du MCD Merise validé.

## Approche

La démarche suivie est celle d'un cabinet de conseil :
1. **Concevoir sur papier** — répondre aux questions des élus avant de placer le moindre visuel
2. **Construire le modèle** — relations, mesures DAX
3. **Valider le modèle** — cartes de comptage sur chaque table
4. **Construire le dashboard** — visuels répondant aux questions métier

## Architecture du modèle

```
Sources (17 fichiers Excel OneDrive)
        │
        ▼
Power BI Desktop — Modèle de données
        │
        ├── 17 tables (relations validées)
        ├── Table _Mesures (mesures DAX centralisées)
        └── 4 pages dashboard
```

## Fichiers

| Fichier | Contenu |
|---------|---------|
| `README.md` | Ce fichier — vue d'ensemble |
| `Relations.md` | Les 17 relations du modèle avec cardinalités |
| `Mesures_DAX.md` | Toutes les mesures DAX documentées |
| `Tests.md` | Validation du modèle — cartes de comptage |
| `Dashboard.md` | Conception sur papier — questions élus → visuels |

## Statut

| Étape | Statut |
|-------|--------|
| 17 tables chargées | ✅ |
| 17 relations créées | ✅ |
| Validation modèle (cartes) | ✅ |
| Mesures DAX | ✅ |
| Dashboard page 1 — Synthèse élus | ⏳ |
| Dashboard page 2 — Pilotage DGST | ⏳ |
| Dashboard page 3 — Suivi opération | ⏳ |
| Dashboard page 4 — Finances | ⏳ |

---

*ATLAS · Stage Data Engineering 2026 · BAMANIA Nicolas*
