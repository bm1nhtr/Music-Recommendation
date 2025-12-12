import argparse
import numpy as np
import collections
import os

RATING_FILE_NAME = dict({'movie': 'ratings.dat', 'book': 'BX-Book-Ratings.csv', 'news': 'ratings.txt'})
SEP = dict({'movie': '::', 'book': ';', 'news': '\t'})
THRESHOLD = dict({'movie': 4, 'book': 0, 'news': 0})


def filter_raw_data(raw_data_path, max_users=50, max_artists=100):
    """
    Filtrer les données brutes pour créer un sous-ensemble plus petit
    Modifie directement les fichiers dans raw_data_path
    
    Args:
        raw_data_path: Chemin vers rawdata/music
        max_users: Nombre maximum d'utilisateurs à garder
        max_artists: Nombre maximum d'artistes à garder
    """
    print(f'Filtrage des données brutes: max {max_users} utilisateurs, {max_artists} artistes...')
    
    user_artists_file = os.path.join(raw_data_path, 'user_artists.dat')
    if not os.path.exists(user_artists_file):
        print('Fichier user_artists.dat non trouvé, pas de filtrage')
        return None, None
    
    # Lire et analyser user_artists.dat
    user_artist_data = []
    with open(user_artists_file, 'r', encoding='utf-8') as f:
        header = next(f)
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                user_id = int(parts[0])
                artist_id = int(parts[1])
                weight = int(parts[2])
                user_artist_data.append((user_id, artist_id, weight))
    
    print(f'Données originales: {len(user_artist_data)} interactions')
    
    # Sélectionner les utilisateurs et artistes les plus actifs
    user_counts = collections.defaultdict(int)
    artist_counts = collections.defaultdict(int)
    
    for user_id, artist_id, weight in user_artist_data:
        user_counts[user_id] += 1
        artist_counts[artist_id] += weight
    
    sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)
    
    selected_users = set([user for user, _ in sorted_users[:max_users]])
    selected_artists = set([artist for artist, _ in sorted_artists[:max_artists]])
    
    print(f'Sélection: {len(selected_users)} utilisateurs, {len(selected_artists)} artistes')
    
    # Filtrer user_artists.dat
    filtered_data = []
    for user_id, artist_id, weight in user_artist_data:
        if user_id in selected_users and artist_id in selected_artists:
            filtered_data.append((user_id, artist_id, weight))
    
    # Sauvegarder le fichier original (backup)
    backup_file = user_artists_file + '.backup'
    if not os.path.exists(backup_file):
        import shutil
        shutil.copy(user_artists_file, backup_file)
        print(f'Sauvegarde créée: {backup_file}')
    
    # Écrire le fichier filtré
    with open(user_artists_file, 'w', encoding='utf-8') as f:
        f.write(header)
        for user_id, artist_id, weight in filtered_data:
            f.write(f'{user_id}\t{artist_id}\t{weight}\n')
    
    print(f'Fichier filtré: {len(filtered_data)} interactions')
    
    return selected_users, selected_artists


def preprocess_music(raw_data_path, output_path, reduce_data=False, max_users=50, max_artists=100):
    """
    Preprocess music dataset (Last.fm)
    
    Args:
        raw_data_path: Chemin vers rawdata/music (dossier avec fichiers .dat)
        output_path: Chemin vers final_data/music (dossier de sortie)
        reduce_data: Si True, filtre les données brutes avant le preprocessing
        max_users: Nombre maximum d'utilisateurs (si reduce_data=True)
        max_artists: Nombre maximum d'artistes (si reduce_data=True)
    """
    # Filtrer les données brutes si demandé
    selected_users = None
    selected_artists = None
    if reduce_data:
        selected_users, selected_artists = filter_raw_data(raw_data_path, max_users, max_artists)
        if selected_users is None:
            reduce_data = False  # Pas de filtrage possible
    
    print('Prétraitement du dataset music...')
    
    # Step 1: Read artists to create item mapping
    print('Lecture des artistes...')
    artist_id2index = {}
    artist_file = os.path.join(raw_data_path, 'artists.dat')
    with open(artist_file, 'r', encoding='utf-8') as f:
        next(f)  # skip header
        for idx, line in enumerate(f):
            parts = line.strip().split('\t')
            if len(parts) >= 1:
                try:
                    artist_id = int(parts[0])
                    # Si on a filtré, ne garder que les artistes sélectionnés
                    if not reduce_data or artist_id in selected_artists:
                        artist_id2index[artist_id] = len(artist_id2index)
                except ValueError:
                    continue
    
    print(f'{len(artist_id2index)} artistes trouvés')
    
    # Step 2: Convert user_artists.dat to ratings_final.txt
    print('Conversion des interactions utilisateur-artiste en ratings...')
    user_artists_file = os.path.join(raw_data_path, 'user_artists.dat')
    
    # Read all user-artist interactions
    user_pos_ratings = collections.defaultdict(set)
    user_weights = collections.defaultdict(dict)  # user -> {artist: weight}
    
    with open(user_artists_file, 'r', encoding='utf-8') as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                try:
                    user_id = int(parts[0])
                    artist_id = int(parts[1])
                    weight = int(parts[2])
                    
                    # Si on a filtré, ne garder que les utilisateurs et artistes sélectionnés
                    if reduce_data:
                        if user_id not in selected_users or artist_id not in selected_artists:
                            continue
                    
                    if artist_id in artist_id2index:
                        artist_idx = artist_id2index[artist_id]
                        user_weights[user_id][artist_idx] = weight
                        # Consider positive if weight > median (or use a threshold)
                        user_pos_ratings[user_id].add(artist_idx)
                except ValueError:
                    continue
    
    # Calculate threshold (median weight) for positive ratings
    all_weights = [w for weights in user_weights.values() for w in weights.values()]
    threshold = np.median(all_weights) if all_weights else 1
    print(f'Seuil de poids utilisé: {threshold:.2f} pour les ratings positifs')
    
    # Remap user IDs to consecutive indices
    user_id2index = {}
    user_idx = 0
    for user_id in user_pos_ratings.keys():
        user_id2index[user_id] = user_idx
        user_idx += 1
    
    # Write ratings_final.txt
    os.makedirs(output_path, exist_ok=True)
    ratings_file = os.path.join(output_path, 'ratings_final.txt')
    with open(ratings_file, 'w', encoding='utf-8') as writer:
        all_artists = set(artist_id2index.values())
        
        for user_id, pos_artists in user_pos_ratings.items():
            user_idx = user_id2index[user_id]
            
            # Write positive ratings
            for artist_idx in pos_artists:
                weight = user_weights[user_id].get(artist_idx, 0)
                label = 1 if weight >= threshold else 0
                writer.write(f'{user_idx}\t{artist_idx}\t{label}\n')
            
            # Sample negative ratings (artists not listened to)
            neg_artists = all_artists - pos_artists
            n_neg = min(len(pos_artists), len(neg_artists))
            if n_neg > 0:
                sampled_neg = np.random.choice(list(neg_artists), size=n_neg, replace=False)
                for artist_idx in sampled_neg:
                    writer.write(f'{user_idx}\t{artist_idx}\t0\n')
    
    print(f'Nombre d\'utilisateurs: {len(user_id2index)}')
    print(f'Nombre d\'items (artistes): {len(artist_id2index)}')
    
    # Step 3: Build knowledge graph from listening patterns (nombre d'écoutes)
    print('Construction du graphe de connaissances à partir des patterns d\'écoute...')
    
    n_artists = len(artist_id2index)
    n_users = len(user_id2index)
    
    # Entity mapping:
    # - Artists: 0 to n_artists-1
    # - Users: n_artists to n_artists+n_users-1
    entity_id2index = {}
    
    # Map artists
    for aid, idx in artist_id2index.items():
        entity_id2index[f'artist_{aid}'] = idx
    
    # Map users (starting from n_artists)
    for uid, idx in user_id2index.items():
        entity_id2index[f'user_{uid}'] = n_artists + idx
    
    # APPROACH 2: User-Artist relations (basé sur nombre d'écoutes)
    # Relation: user -> artist avec poids = nombre d'écoutes
    print('  - Construction des relations User-Artist...')
    user_artist_relations = []  # (user_idx, artist_idx, weight)
    
    # Re-read user_artists.dat to get weights
    with open(user_artists_file, 'r', encoding='utf-8') as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                try:
                    raw_user_id = int(parts[0])
                    raw_artist_id = int(parts[1])
                    weight = int(parts[2])  # nombre d'écoutes
                    
                    if reduce_data:
                        if raw_user_id not in selected_users or raw_artist_id not in selected_artists:
                            continue
                    
                    if raw_user_id in user_id2index and raw_artist_id in artist_id2index:
                        user_idx = user_id2index[raw_user_id]
                        artist_idx = artist_id2index[raw_artist_id]
                        user_entity_idx = n_artists + user_idx
                        user_artist_relations.append((user_entity_idx, artist_idx, weight))
                except ValueError:
                    continue
    
    print(f'    {len(user_artist_relations)} relations User-Artist créées')
    
    # APPROACH 3: Artist-Artist similarity (basé sur co-listening pondéré)
    # Relation: artist1 -> artist2 avec poids = nombre d'users qui ont écouté les deux
    print('  - Construction des relations Artist-Artist (similarité pondérée)...')
    
    # Construire artist-user mapping pour calculer co-listening
    artist_users = collections.defaultdict(dict)  # artist_idx -> {user_idx: weight}
    
    for user_entity_idx, artist_idx, weight in user_artist_relations:
        user_idx = user_entity_idx - n_artists  # Convert back to user index
        artist_users[artist_idx][user_idx] = weight
    
    # Calculer similarité entre artistes (co-listening pondéré)
    artist_similarity = collections.defaultdict(int)  # (artist1, artist2) -> co-listening count
    
    # Pour chaque utilisateur, créer des connexions entre artistes qu'il a écoutés
    for user_idx in range(n_users):
        user_artists = []
        for artist_idx, user_dict in artist_users.items():
            if user_idx in user_dict:
                user_artists.append(artist_idx)
        
        # Créer des connexions entre toutes les paires d'artistes pour cet utilisateur
        for i in range(len(user_artists)):
            for j in range(i + 1, len(user_artists)):
                artist1, artist2 = user_artists[i], user_artists[j]
                # Ordre canonique pour éviter les doublons
                if artist1 > artist2:
                    artist1, artist2 = artist2, artist1
                artist_similarity[(artist1, artist2)] += 1
    
    # Filtrer: seulement garder les connexions avec au moins min_co_listens utilisateurs
    min_co_listens = 2
    artist_artist_relations = []
    for (artist1, artist2), count in artist_similarity.items():
        if count >= min_co_listens:
            artist_artist_relations.append((artist1, artist2, count))
    
    print(f'    {len(artist_artist_relations)} relations Artist-Artist créées (seuil: {min_co_listens} co-écoutes)')
    
    # Write kg_final.txt
    kg_file = os.path.join(output_path, 'kg_final.txt')
    relation_id2index = {
        'listened_to': 0,      # user -> artist (Approach 2)
        'listened_by': 1,      # artist -> user (reverse, Approach 2)
        'similar_to': 2,       # artist1 -> artist2 (Approach 3)
        'similar_from': 3      # artist2 -> artist1 (reverse, Approach 3)
    }
    
    n_kg_triples = 0
    with open(kg_file, 'w', encoding='utf-8') as writer:
        # APPROACH 2: User -> Artist relations (listened_to)
        for user_entity_idx, artist_idx, weight in user_artist_relations:
            writer.write(f'{user_entity_idx}\t{relation_id2index["listened_to"]}\t{artist_idx}\n')
            n_kg_triples += 1
        
        # APPROACH 2: Artist -> User relations (listened_by) - reverse
        for user_entity_idx, artist_idx, weight in user_artist_relations:
            writer.write(f'{artist_idx}\t{relation_id2index["listened_by"]}\t{user_entity_idx}\n')
            n_kg_triples += 1
        
        # APPROACH 3: Artist -> Artist relations (similar_to)
        for artist1, artist2, weight in artist_artist_relations:
            writer.write(f'{artist1}\t{relation_id2index["similar_to"]}\t{artist2}\n')
            n_kg_triples += 1
        
        # APPROACH 3: Reverse Artist -> Artist relations (similar_from)
        for artist1, artist2, weight in artist_artist_relations:
            writer.write(f'{artist2}\t{relation_id2index["similar_from"]}\t{artist1}\n')
            n_kg_triples += 1
    
    n_entities = len(entity_id2index)
    n_relations = len(relation_id2index)
    
    print(f'Graphe de connaissances créé:')
    print(f'  - Nombre d\'entités: {n_entities} ({n_artists} artistes + {n_users} utilisateurs)')
    print(f'  - Nombre de relations: {n_relations}')
    print(f'    * listened_to/listened_by: {len(user_artist_relations) * 2} triplets')
    print(f'    * similar_to/similar_from: {len(artist_artist_relations) * 2} triplets')
    print(f'  - Nombre total de triplets KG: {n_kg_triples}')
    
    # Sauvegarder les métadonnées du dataset
    metadata_file = os.path.join(output_path, 'dataset_metadata.txt')
    with open(metadata_file, 'w', encoding='utf-8') as f:
        f.write(f'filtered={reduce_data}\n')
        if reduce_data:
            f.write(f'max_users_requested={max_users}\n')
            f.write(f'max_artists_requested={max_artists}\n')
        # Sauvegarder les valeurs RÉELLES, pas les max demandés
        f.write(f'n_users_actual={len(user_id2index)}\n')
        f.write(f'n_artists_actual={n_artists}\n')
        f.write(f'n_entities={n_entities}\n')
        f.write(f'n_relations={n_relations}\n')
        f.write(f'n_kg_triples={n_kg_triples}\n')
    
    print('Métadonnées sauvegardées dans dataset_metadata.txt')
    print('Terminé!')


def read_item_index_to_entity_id_file():
    file = '../data/' + DATASET + '/item_index2entity_id_rehashed.txt'
    print('Lecture du fichier de mapping item index vers entity id: ' + file + ' ...')
    i = 0
    for line in open(file, encoding='utf-8').readlines():
        item_index = line.strip().split('\t')[0]
        satori_id = line.strip().split('\t')[1]
        item_index_old2new[item_index] = i
        entity_id2index[satori_id] = i
        i += 1


def convert_rating():
    file = '../data/' + DATASET + '/' + RATING_FILE_NAME[DATASET]

    print('Lecture du fichier de ratings ...')
    item_set = set(item_index_old2new.values())
    user_pos_ratings = dict()
    user_neg_ratings = dict()

    for line in open(file, encoding='utf-8').readlines()[1:]:
        array = line.strip().split(SEP[DATASET])

        # remove prefix and suffix quotation marks for BX dataset
        if DATASET == 'book':
            array = list(map(lambda x: x[1:-1], array))

        item_index_old = array[1]
        if item_index_old not in item_index_old2new:  # the item is not in the final item set
            continue
        item_index = item_index_old2new[item_index_old]

        user_index_old = int(array[0])

        rating = float(array[2])
        if rating >= THRESHOLD[DATASET]:
            if user_index_old not in user_pos_ratings:
                user_pos_ratings[user_index_old] = set()
            user_pos_ratings[user_index_old].add(item_index)
        else:
            if user_index_old not in user_neg_ratings:
                user_neg_ratings[user_index_old] = set()
            user_neg_ratings[user_index_old].add(item_index)

    print('Conversion du fichier de ratings ...')
    writer = open('../data/' + DATASET + '/ratings_final.txt', 'w', encoding='utf-8')
    user_cnt = 0
    user_index_old2new = dict()
    for user_index_old, pos_item_set in user_pos_ratings.items():
        if user_index_old not in user_index_old2new:
            user_index_old2new[user_index_old] = user_cnt
            user_cnt += 1
        user_index = user_index_old2new[user_index_old]

        for item in pos_item_set:
            writer.write('%d\t%d\t1\n' % (user_index, item))
        unwatched_set = item_set - pos_item_set
        if user_index_old in user_neg_ratings:
            unwatched_set -= user_neg_ratings[user_index_old]
        for item in np.random.choice(list(unwatched_set), size=len(pos_item_set), replace=False):
            writer.write('%d\t%d\t0\n' % (user_index, item))
    writer.close()
    print('Nombre d\'utilisateurs: %d' % user_cnt)
    print('Nombre d\'items: %d' % len(item_set))


def convert_kg():
    print('Conversion du fichier KG ...')
    entity_cnt = len(entity_id2index)
    relation_cnt = 0

    writer = open('../data/' + DATASET + '/kg_final.txt', 'w', encoding='utf-8')

    files = []
    if DATASET == 'movie':
        files.append(open('../data/' + DATASET + '/kg_part1_rehashed.txt', encoding='utf-8'))
        files.append(open('../data/' + DATASET + '/kg_part2_rehashed.txt', encoding='utf-8'))
    else:
        files.append(open('../data/' + DATASET + '/kg_rehashed.txt', encoding='utf-8'))

    for file in files:
        for line in file:
            array = line.strip().split('\t')
            head_old = array[0]
            relation_old = array[1]
            tail_old = array[2]

            if head_old not in entity_id2index:
                entity_id2index[head_old] = entity_cnt
                entity_cnt += 1
            head = entity_id2index[head_old]

            if tail_old not in entity_id2index:
                entity_id2index[tail_old] = entity_cnt
                entity_cnt += 1
            tail = entity_id2index[tail_old]

            if relation_old not in relation_id2index:
                relation_id2index[relation_old] = relation_cnt
                relation_cnt += 1
            relation = relation_id2index[relation_old]

            writer.write('%d\t%d\t%d\n' % (head, relation, tail))

    writer.close()
    print('Nombre d\'entités (contenant les items): %d' % entity_cnt)
    print('Nombre de relations: %d' % relation_cnt)


if __name__ == '__main__':
    np.random.seed(555)

    parser = argparse.ArgumentParser(description='Prétraitement des données avec option de réduction')
    parser.add_argument('-d', '--dataset', type=str, default='music', 
                       help='Nom du dataset à prétraiter')
    parser.add_argument('--reduce', action='store_true',
                       help='Réduire les données brutes avant le preprocessing')
    parser.add_argument('--max_users', type=int, default=50,
                       help='Nombre maximum d\'utilisateurs (si --reduce)')
    parser.add_argument('--max_artists', type=int, default=100,
                       help='Nombre maximum d\'artistes (si --reduce)')
    
    args = parser.parse_args()
    DATASET = args.dataset

    raw_data_path = f'../rawdata/{DATASET}'
    output_path = f'../final_data/{DATASET}'
    
    if DATASET == 'music':
        # Use new music preprocessing
        preprocess_music(raw_data_path, output_path, 
                        reduce_data=args.reduce,
                        max_users=args.max_users,
                        max_artists=args.max_artists)
    else:
        # Use old preprocessing for movie/book
        entity_id2index = dict()
        relation_id2index = dict()
        item_index_old2new = dict()

        read_item_index_to_entity_id_file()
        convert_rating()
        convert_kg()

        print('Terminé')
