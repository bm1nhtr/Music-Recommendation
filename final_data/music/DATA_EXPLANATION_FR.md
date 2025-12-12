# Explication du Dataset Music

## Vue d'ensemble

Les fichiers `ratings_final.txt` et `kg_final.txt` sont générés à partir des **fichiers de données brutes** du dataset Last.fm via le script `preprocess.py`.

## Fichiers de Données Brutes (Input)

### 1. `user_artists.dat`
**Format**: `userID \t artistID \t weight`
- Contient les informations sur quels artistes chaque utilisateur a écoutés et le nombre d'écoutes (weight)
- Exemple: `2 \t 51 \t 13883` → L'utilisateur 2 a écouté l'artiste 51 avec 13,883 écoutes

### 2. `user_taggedartists.dat`
**Format**: `userID \t artistID \t tagID \t day \t month \t year`
- Contient les informations sur quels tags les utilisateurs ont attribués aux artistes
- Exemple: `2 \t 52 \t 13 \t 1 \t 4 \t 2009` → L'utilisateur 2 a tagué l'artiste 52 avec le tag 13

### 3. `artists.dat`
**Format**: `id \t name \t url \t pictureURL`
- Liste de tous les artistes dans le dataset

### 4. `tags.dat`
**Format**: `tagID \t tagValue`
- Liste de tous les tags (exemples: "rock", "metal", "pop")

## Fichiers Traités (Output)

### 1. `ratings_final.txt` - Interactions Utilisateur-Item

**Créé à partir de**: `user_artists.dat`

**Processus**:
1. Lire `user_artists.dat` → extraire les interactions utilisateur-artiste avec les weights
2. Calculer un seuil (weight médian) pour classer positive/négative
3. Remapper les IDs utilisateur et artiste en indices consécutifs (0, 1, 2, ...)
4. Pour chaque utilisateur:
   - Ratings positifs (label=1): Artistes avec weight >= seuil
   - Ratings négatifs (label=0): Échantillonnage aléatoire d'artistes non écoutés

**Format**: `user_id \t artist_id \t label`
- `user_id`: ID de l'utilisateur (remappé)
- `artist_id`: ID de l'artiste (remappé)  
- `label`: 1 = interaction positive, 0 = interaction négative

**Exemple**:
```
0	45	1    # L'utilisateur 0 a écouté l'artiste 45 (positive)
0	46	1    # L'utilisateur 0 a écouté l'artiste 46 (positive)
0	100	0    # L'utilisateur 0 n'a pas écouté l'artiste 100 (échantillon négatif)
```

### 2. `kg_final.txt` - Graphe de Connaissances

**Créé à partir de**: `user_taggedartists.dat` + `artists.dat` + `tags.dat`

**Processus**:
1. Lire les tags depuis `tags.dat`
2. Lire les relations artiste-tag depuis `user_taggedartists.dat`
3. Créer les entités:
   - Artistes: indices 0 → n_artists-1
   - Tags: indices n_artists → n_artists+n_tags-1
4. Créer les relations:
   - Relation 0: `has_tag` (artiste → tag)
   - Relation 1: `tagged_by` (tag → artiste) - relation inverse

**Format**: `head_entity \t relation \t tail_entity`
- `head_entity`: ID de l'entité source (artiste ou tag)
- `relation`: ID de la relation (0 ou 1)
- `tail_entity`: ID de l'entité cible (artiste ou tag)

**Exemple**:
```
46	0	17761    # L'artiste 46 a le tag 17761
17761	1	46      # Le tag 17761 est attribué à l'artiste 46 (inverse)
```

## Comment régénérer les fichiers traités

Si vous souhaitez régénérer `ratings_final.txt` et `kg_final.txt` à partir des données brutes:

```bash
cd src
python preprocess.py --dataset music
```

Le script va:
1. Lire les fichiers de données brutes depuis `data/music/`
2. Les traiter et les convertir au format standard
3. Écrire `ratings_final.txt` et `kg_final.txt`

## Notes

- Les fichiers `.npy` sont des versions mises en cache des fichiers `.txt` pour un chargement plus rapide
- Si vous avez déjà `ratings_final.txt` et `kg_final.txt`, vous n'avez pas besoin de relancer le preprocessing
- Les fichiers de données brutes (`*.dat`) sont l'input, les fichiers traités (`*_final.txt`) sont l'output

