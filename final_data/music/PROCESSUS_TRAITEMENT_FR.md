# Processus de Traitement du Dataset Music

## Schéma d'ensemble

```
FICHIERS DE DONNÉES BRUTES (Input)          FICHIERS TRAITÉS (Output)
───────────────────────────────             ─────────────────────────

user_artists.dat                            ratings_final.txt
├─ userID \t artistID \t weight    →       ├─ user_id \t artist_id \t label
└─ Exemple: 2 \t 51 \t 13883               └─ Exemple: 0 \t 45 \t 1

user_taggedartists.dat                      kg_final.txt
├─ userID \t artistID \t tagID     →       ├─ head \t relation \t tail
└─ Exemple: 2 \t 52 \t 13                  └─ Exemple: 46 \t 0 \t 17761

artists.dat
└─ id \t name \t url

tags.dat
└─ tagID \t tagValue
```

## Détails étape par étape

### ÉTAPE 1: Créer `ratings_final.txt`

**Input**: `user_artists.dat`
```
userID	artistID	weight
2	51	13883
2	52	11690
2	53	11351
```

**Traitement**:
1. Lire toutes les interactions utilisateur-artiste
2. Calculer le weight médian comme seuil
3. Remapper les IDs:
   - IDs utilisateur: 2, 3, 4... → 0, 1, 2...
   - IDs artiste: 51, 52, 53... → 0, 1, 2...
4. Classification:
   - Weight >= seuil → label = 1 (positive)
   - Weight < seuil → label = 0 (négative)
5. Échantillonnage négatif: Sélectionner aléatoirement des artistes non écoutés

**Output**: `ratings_final.txt`
```
user_id	artist_id	label
0	45	1      ← L'utilisateur 0 a écouté l'artiste 45 (positive)
0	46	1      ← L'utilisateur 0 a écouté l'artiste 46 (positive)
0	100	0      ← L'utilisateur 0 n'a pas écouté l'artiste 100 (échantillon négatif)
```

### ÉTAPE 2: Créer `kg_final.txt`

**Input**: `user_taggedartists.dat` + `artists.dat` + `tags.dat`

**Traitement**:
1. Lire les artistes → remapper en indices 0 → n_artists-1
2. Lire les tags → remapper en indices n_artists → n_artists+n_tags-1
3. Lire les relations artiste-tag depuis `user_taggedartists.dat`
4. Créer 2 types de relations:
   - Relation 0 (`has_tag`): artiste → tag
   - Relation 1 (`tagged_by`): tag → artiste (inverse)

**Exemple**:
- L'artiste 46 est tagué avec le tag 17761
- Créer 2 triplets:
  - `46 \t 0 \t 17761` (L'artiste 46 a le tag 17761)
  - `17761 \t 1 \t 46` (Le tag 17761 est attribué à l'artiste 46)

**Output**: `kg_final.txt`
```
head	relation	tail
46	0	17761    ← L'artiste 46 a le tag 17761
17761	1	46      ← Le tag 17761 est attribué à l'artiste 46 (inverse)
```

## Comment exécuter le preprocessing

```bash
cd src
python preprocess.py --dataset music
```

**Sortie console**:
```
Preprocessing music dataset...
Reading artists...
Found 17632 artists
Converting user-artist interactions to ratings...
Using weight threshold: 1234.00 for positive ratings
Number of users: 1892
Number of items (artists): 17632
Building knowledge graph from tags...
Knowledge graph created:
  - Number of entities: 21851 (17632 artists + 4219 tags)
  - Number of relations: 2
  - Number of KG triples: 216874
Done!
```

## Mapping des IDs

### IDs Utilisateur
- **Brut**: 2, 3, 4, 5, ... (non consécutifs)
- **Traité**: 0, 1, 2, 3, ... (consécutifs à partir de 0)

### IDs Artiste  
- **Brut**: 51, 52, 53, ... (non consécutifs)
- **Traité**: 0, 1, 2, 3, ... (consécutifs à partir de 0)

### IDs Entité dans le KG
- **Artistes**: 0 → 17631 (n_artists - 1)
- **Tags**: 17632 → 21850 (n_artists → n_artists + n_tags - 1)

## Pourquoi le preprocessing est nécessaire?

1. **Standardisation du format**: Les données brutes ont plusieurs formats → standardisation en format simple
2. **Remapping des IDs**: Les IDs dans les données brutes ne sont pas consécutifs → remapping en 0, 1, 2... pour faciliter le traitement
3. **Création d'échantillons négatifs**: Les données brutes n'ont que des interactions positives → besoin d'échantillons négatifs pour l'entraînement
4. **Construction du Graphe de Connaissances**: À partir des données de tagging → créer une structure de graphe pour le modèle

