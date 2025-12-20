"""
Module pour charger et construire le graphe de connaissances
Séparé du code ML/recommendation pour se concentrer sur les algorithmes graph classiques
"""
import collections
import os
import numpy as np
import hashlib


def compute_file_hash(file_path):
    """
    Calculer le hash SHA256 d'un fichier pour vérifier l'intégrité des données.
    
    Cette fonction calcule un checksum cryptographique (SHA256) d'un fichier,
    permettant de détecter toute modification ou corruption des données. Le hash
    est utilisé pour garantir la reproducibility entre différentes machines.
    
    Algorithme:
    - Utilise SHA256 (Secure Hash Algorithm 256 bits)
    - Lit le fichier par chunks de 4KB pour gérer les gros fichiers efficacement
    - Retourne le hash en format hexadécimal (64 caractères)
    
    Utilisation:
    - Lors du preprocessing: calcule les hash de kg_final.txt et ratings_final.txt
    - Les hash sont sauvegardés dans dataset_metadata.txt
    - Lors du chargement: compare les hash actuels avec ceux sauvegardés
    
    Args:
        file_path: Chemin absolu ou relatif vers le fichier à hasher
        
    Returns:
        str: Hash SHA256 en hexadécimal (64 caractères)
            Exemple: "a1b2c3d4e5f6..."
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        IOError: Si le fichier ne peut pas être lu
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Lire le fichier par chunks de 4KB pour optimiser la mémoire
        # Cela permet de gérer les gros fichiers sans charger tout en mémoire
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def load_dataset_metadata(dataset_path, dataset_name='music'):
    """
    Charger les métadonnées du dataset
    
    Returns:
        dict: Métadonnées du dataset ou None si pas de fichier
    """
    metadata_file = os.path.join(dataset_path, dataset_name, 'dataset_metadata.txt')
    if not os.path.exists(metadata_file):
        return None
    
    metadata = {}
    with open(metadata_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                # Convertir les valeurs booléennes et numériques
                if value.lower() == 'true':
                    metadata[key] = True
                elif value.lower() == 'false':
                    metadata[key] = False
                else:
                    try:
                        metadata[key] = int(value)
                    except ValueError:
                        metadata[key] = value
    return metadata


def verify_data_integrity(dataset_path, dataset_name='music', use_small=False, verbose=True):
    """
    Vérifier l'intégrité des données en comparant les checksums
    
    Cette fonction permet de vérifier que les fichiers .txt correspondent
    aux checksums sauvegardés dans metadata, garantissant que deux personnes
    avec les mêmes paramètres de preprocessing ont les mêmes données.
    
    Args:
        dataset_path: Chemin vers le dossier final_data
        dataset_name: Nom du dataset
        use_small: Si True, utilise les fichiers _small
        verbose: Si True, affiche les résultats de vérification
        
    Returns:
        dict: Résultats de vérification avec clés:
            - 'kg_valid': bool - Le fichier KG correspond au checksum
            - 'ratings_valid': bool - Le fichier ratings correspond au checksum
            - 'all_valid': bool - Tous les fichiers sont valides
            - 'kg_hash_current': str - Hash actuel du fichier KG
            - 'kg_hash_expected': str - Hash attendu depuis metadata
            - 'ratings_hash_current': str - Hash actuel du fichier ratings
            - 'ratings_hash_expected': str - Hash attendu depuis metadata
    """
    metadata = load_dataset_metadata(dataset_path, dataset_name)
    if not metadata:
        if verbose:
            print('[VERIFICATION] Pas de metadata trouvée, impossible de vérifier')
        return {'all_valid': False, 'error': 'no_metadata'}
    
    suffix = '_small' if use_small else ''
    kg_file = os.path.join(dataset_path, dataset_name, f'kg_final{suffix}.txt')
    ratings_file = os.path.join(dataset_path, dataset_name, f'ratings_final{suffix}.txt')
    
    results = {
        'kg_valid': False,
        'ratings_valid': False,
        'all_valid': False
    }
    
    # Vérifier KG
    if os.path.exists(kg_file) and 'kg_file_hash' in metadata:
        kg_hash_current = compute_file_hash(kg_file)
        kg_hash_expected = metadata['kg_file_hash']
        results['kg_valid'] = (kg_hash_current == kg_hash_expected)
        results['kg_hash_current'] = kg_hash_current
        results['kg_hash_expected'] = kg_hash_expected
        
        if verbose:
            if results['kg_valid']:
                print(f'✅ [VERIFICATION] Fichier KG valide (hash: {kg_hash_current[:16]}...)')
            else:
                print(f'❌ [VERIFICATION] Fichier KG INVALIDE!')
                print(f'   Hash actuel:   {kg_hash_current}')
                print(f'   Hash attendu:  {kg_hash_expected}')
                print(f'   → Les données ne correspondent pas aux métadonnées')
    elif not os.path.exists(kg_file):
        if verbose:
            print(f'⚠️ [VERIFICATION] Fichier KG non trouvé: {kg_file}')
        results['kg_valid'] = False
    elif 'kg_file_hash' not in metadata:
        if verbose:
            print('⚠️ [VERIFICATION] Pas de checksum KG dans metadata (ancien format?)')
        results['kg_valid'] = None  # Inconnu
    
    # Vérifier Ratings
    if os.path.exists(ratings_file) and 'ratings_file_hash' in metadata:
        ratings_hash_current = compute_file_hash(ratings_file)
        ratings_hash_expected = metadata['ratings_file_hash']
        results['ratings_valid'] = (ratings_hash_current == ratings_hash_expected)
        results['ratings_hash_current'] = ratings_hash_current
        results['ratings_hash_expected'] = ratings_hash_expected
        
        if verbose:
            if results['ratings_valid']:
                print(f'✅ [VERIFICATION] Fichier Ratings valide (hash: {ratings_hash_current[:16]}...)')
            else:
                print(f'❌ [VERIFICATION] Fichier Ratings INVALIDE!')
                print(f'   Hash actuel:   {ratings_hash_current}')
                print(f'   Hash attendu:  {ratings_hash_expected}')
                print(f'   → Les données ne correspondent pas aux métadonnées')
    elif not os.path.exists(ratings_file):
        if verbose:
            print(f'⚠️ [VERIFICATION] Fichier Ratings non trouvé: {ratings_file}')
        results['ratings_valid'] = False
    elif 'ratings_file_hash' not in metadata:
        if verbose:
            print('⚠️ [VERIFICATION] Pas de checksum Ratings dans metadata (ancien format?)')
        results['ratings_valid'] = None  # Inconnu
    
    # Résultat global
    if results['kg_valid'] is not False and results['ratings_valid'] is not False:
        results['all_valid'] = (results['kg_valid'] is True and results['ratings_valid'] is True)
    else:
        results['all_valid'] = False
    
    if verbose:
        if results['all_valid']:
            print('✅ [VERIFICATION] Tous les fichiers sont valides - Reproducibility garantie!')
        elif results['kg_valid'] is None or results['ratings_valid'] is None:
            print('⚠️ [VERIFICATION] Impossible de vérifier complètement (metadata incomplète)')
        else:
            print('❌ [VERIFICATION] Certains fichiers sont invalides - Reproducibility NON garantie!')
    
    return results


def load_kg(dataset_path, dataset_name='music', use_small=False):
    """
    Charger le graphe de connaissances depuis un fichier
    
    Args:
        dataset_path: Chemin vers le dossier final_data (ex: '../final_data')
        dataset_name: Nom du dataset (ex: 'music')
        use_small: Si True, utilise kg_final_small.txt au lieu de kg_final.txt (déprécié, utilise metadata)
    
    Returns:
        tuple: (n_entity, n_relation, kg, metadata)
            - n_entity: Nombre d'entités
            - n_relation: Nombre de relations
            - kg: Dictionnaire {head: [(tail, relation), ...]}
            - metadata: Dictionnaire avec métadonnées du dataset
    """
    print('Lecture du fichier KG ...')
    
    # Charger les métadonnées
    metadata = load_dataset_metadata(dataset_path, dataset_name)
    
    # Si metadata existe et indique filtered, on utilise le dataset filtré
    # Sinon, on utilise use_small flag (pour compatibilité)
    if metadata and metadata.get('filtered', False):
        print('Dataset filtré détecté depuis les métadonnées')
    
    suffix = '_small' if use_small else ''
    kg_file = os.path.join(dataset_path, dataset_name, f'kg_final{suffix}')
    
    # Vérifier si le cache est valide (pour garantir reproducibility)
    cache_needs_reload = False
    cache_valid = False
    
    if os.path.exists(kg_file + '.npy') and os.path.exists(kg_file + '.txt'):
        # Vérifier 1: Le fichier .txt a-t-il été modifié après le cache?
        txt_mtime = os.path.getmtime(kg_file + '.txt')
        npy_mtime = os.path.getmtime(kg_file + '.npy')
        
        if txt_mtime > npy_mtime:
            # Le fichier source a été modifié après le cache
            cache_needs_reload = True
            print(f'[INFO] Le fichier source .txt a été modifié après le cache')
            print(f'   Cache sera régénéré pour garantir la cohérence')
        else:
            # Vérifier 2: Cohérence avec metadata (si disponible)
            if metadata and metadata.get('n_artists_actual') is not None and metadata.get('n_users_actual') is not None:
                expected_entities = metadata.get('n_artists_actual', 0) + metadata.get('n_users_actual', 0)
                # Charger temporairement pour vérifier
                temp_kg_np = np.load(kg_file + '.npy')
                temp_n_entity = len(set(temp_kg_np[:, 0]) | set(temp_kg_np[:, 2]))
                if temp_n_entity != expected_entities:
                    cache_needs_reload = True
                    print(f'[ATTENTION] Incoherence detectee entre cache et metadonnees!')
                    print(f'   - Entites dans le cache (.npy): {temp_n_entity}')
                    print(f'   - Entites attendues (metadata): {expected_entities}')
                    print(f'   - Artistes: {metadata.get("n_artists_actual")}, Users: {metadata.get("n_users_actual")}')
                else:
                    cache_valid = True
            else:
                # Pas de metadata, on assume que le cache est valide si .txt n'a pas changé
                cache_valid = True
    
    # Supprimer le cache si nécessaire
    if cache_needs_reload:
        print(f'[ACTION] Suppression automatique du cache obsolete...')
        try:
            if os.path.exists(kg_file + '.npy'):
                os.remove(kg_file + '.npy')
                print(f'   ✅ Cache supprime: {kg_file}.npy')
            # Supprimer aussi le cache ratings si existe
            rating_file = os.path.join(dataset_path, dataset_name, f'ratings_final{suffix}')
            if os.path.exists(rating_file + '.npy'):
                os.remove(rating_file + '.npy')
                print(f'   ✅ Cache ratings supprime: {rating_file}.npy')
        except Exception as e:
            print(f'   ⚠️ Erreur lors de la suppression du cache: {e}')
        print(f'   Le cache sera régénéré automatiquement depuis le fichier .txt')
    
    # Charger le fichier (depuis cache ou .txt)
    if os.path.exists(kg_file + '.npy') and cache_valid and not cache_needs_reload:
        kg_np = np.load(kg_file + '.npy')
        print(f'   ✅ Cache valide utilise (reproducibility garantie)')
    else:
        # Détecter le nombre de colonnes (3 ou 4)
        with open(kg_file + '.txt', 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            num_cols = len(first_line.split('\t'))
        
        if num_cols == 4:
            # Format avec weights
            kg_np = np.loadtxt(kg_file + '.txt', dtype=np.int32)
        else:
            # Format ancien sans weights (backward compatibility)
            kg_data = np.loadtxt(kg_file + '.txt', dtype=np.int32)
            # Ajouter une colonne de poids = 1 par défaut
            kg_np = np.column_stack([kg_data, np.ones(len(kg_data), dtype=np.int32)])
        
        np.save(kg_file + '.npy', kg_np)
    
    #nombre d'entités à la fois colonne tête et queue
    n_entity = len(set(kg_np[:, 0]) | set(kg_np[:, 2])) # Têtes et queues, union
    n_relation = len(set(kg_np[:, 1]))
    
    kg = construct_kg(kg_np)
    
    # Mettre à jour metadata avec les valeurs réelles
    if metadata is None:
        metadata = {}
    metadata['n_entity'] = n_entity
    metadata['n_relation'] = n_relation
    metadata['type'] = 'filtered' if metadata.get('filtered', False) else 'full'
    
    # Vérification finale (devrait toujours être cohérent maintenant)
    if metadata.get('n_artists_actual') is not None and metadata.get('n_users_actual') is not None:
        expected_entities = metadata.get('n_artists_actual', 0) + metadata.get('n_users_actual', 0)
        if n_entity != expected_entities:
            print(f'[ERREUR] Incoherence persistante apres rechargement!')
            print(f'   - Entites chargees: {n_entity}')
            print(f'   - Entites attendues (metadata): {expected_entities}')
            print(f'   [SOLUTION] Relancez le preprocessing pour regenerer les donnees.')
    
    print(f'Graphe de connaissances chargé: {n_entity} entités, {n_relation} relations')
    
    # Vérifier l'intégrité des données (reproducibility)
    verify_results = verify_data_integrity(dataset_path, dataset_name, use_small, verbose=True)
    if not verify_results.get('all_valid', False) and verify_results.get('kg_valid') is False:
        print(f'[ATTENTION] Les données ne correspondent pas aux checksums sauvegardés!')
        print(f'   Cela peut indiquer que les fichiers ont été modifiés ou corrompus.')
        print(f'   Pour garantir la reproducibility, relancez le preprocessing avec les mêmes paramètres.')
    
    return n_entity, n_relation, kg, metadata


def construct_kg(kg_np):
    """
    Construire la structure du graphe depuis un array numpy
    
    Args:
        kg_np: Array numpy de shape (n_triples, 3) ou (n_triples, 4)
               avec [head, relation, tail] ou [head, relation, tail, weight]
    
    Returns:
        Dictionnaire {head: [(tail, relation, weight), ...]}
        Si pas de weight, weight = 1 par défaut
    """
    print('Construction du graphe de connaissances ...')
    kg = collections.defaultdict(list)
    
    if kg_np.shape[1] == 4:
        # Format avec weights
        for head, relation, tail, weight in kg_np:
            kg[head].append((tail, relation, weight))
    else:
        # Format ancien sans weights (backward compatibility)
        for head, relation, tail in kg_np:
            kg[head].append((tail, relation, 1))  # Poids par défaut = 1
    
    return kg


def load_ratings(dataset_path, dataset_name='music', use_small=False):
    """
    Charger les ratings utilisateur-item (optionnel, pour analyse)
    
    Args:
        dataset_path: Chemin vers le dossier final_data
        dataset_name: Nom du dataset
        use_small: Si True, utilise ratings_final_small.txt au lieu de ratings_final.txt (déprécié)
    
    Returns:
        Array numpy de shape (n_ratings, 3) avec [user_id, item_id, label]
    """
    print('Lecture du fichier de ratings ...')
    
    # Vérifier metadata pour savoir si dataset est filtré
    metadata = load_dataset_metadata(dataset_path, dataset_name)
    
    suffix = '_small' if use_small else ''
    rating_file = os.path.join(dataset_path, dataset_name, f'ratings_final{suffix}')
    
    # Vérifier si le cache est valide (même logique que pour kg)
    cache_valid = False
    if os.path.exists(rating_file + '.npy') and os.path.exists(rating_file + '.txt'):
        txt_mtime = os.path.getmtime(rating_file + '.txt')
        npy_mtime = os.path.getmtime(rating_file + '.npy')
        if txt_mtime <= npy_mtime:
            cache_valid = True
    
    if cache_valid:
        rating_np = np.load(rating_file + '.npy')
    else:
        rating_np = np.loadtxt(rating_file + '.txt', dtype=np.int32)
        np.save(rating_file + '.npy', rating_np)
    
    print(f'Ratings chargés: {rating_np.shape[0]} interactions')
    return rating_np


def get_user_history(ratings_np):
    """
    Extraire l'historique des utilisateurs depuis les ratings
    
    Args:
        ratings_np: Array numpy avec [user_id, item_id, label]
    
    Returns:
        Dictionnaire {user_id: [item_id, ...]} avec seulement les interactions positives (label=1)
    """
    user_history = collections.defaultdict(list)
    
    for user_id, item_id, label in ratings_np:
        if label == 1:  # Seulement les interactions positives
            user_history[user_id].append(item_id)
    
    return user_history

