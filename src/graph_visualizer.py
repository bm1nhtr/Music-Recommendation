"""
Module pour visualiser le graphe de connaissances
Utilise networkx et matplotlib pour créer des visualisations simples et claires
"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import defaultdict
import os


def visualize_graph_structure(kg, output_file='graph_structure.png', dataset_info=None, max_nodes=50):
    """
    Visualiser la structure générale du graphe de connaissances
    Montre les artistes, utilisateurs et leurs relations de manière claire
    
    Args:
        kg: Dictionnaire {head: [(tail, relation, weight), ...]}
        output_file: Nom du fichier de sortie
        dataset_info: Dictionnaire avec info sur le dataset
        max_nodes: Nombre maximum de nœuds à afficher
    """
    print(f'Création de la visualisation de la structure du graphe...')
    
    G = nx.DiGraph()
    all_nodes = set()
    all_edges = []
    
    # Collecter tous les nœuds et arêtes
    for head, tails in kg.items():
        all_nodes.add(head)
        for tail_info in tails:
            if len(tail_info) == 3:
                tail, relation, weight = tail_info
            else:
                tail, relation = tail_info
                weight = 1
            all_nodes.add(tail)
            all_edges.append((head, tail, relation, weight))
    
    print(f'Graphe total: {len(all_nodes)} nœuds, {len(all_edges)} arêtes')
    
    # Limiter le nombre de nœuds si nécessaire
    if len(all_nodes) > max_nodes:
        print(f'Limitation à {max_nodes} nœuds pour la visualisation...')
        node_degrees = defaultdict(int)
        for head, tails in kg.items():
            node_degrees[head] += len(tails)
            for tail_info in tails:
                tail = tail_info[0]
                node_degrees[tail] += 1
        
        top_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
        selected_nodes = set([node for node, _ in top_nodes])
        
        filtered_edges = [(h, t, r, w) for h, t, r, w in all_edges 
                         if h in selected_nodes and t in selected_nodes]
        
        for node in selected_nodes:
            G.add_node(node)
        for head, tail, relation, weight in filtered_edges:
            G.add_edge(head, tail, relation=relation, weight=weight)
    else:
        for node in all_nodes:
            G.add_node(node)
        for head, tail, relation, weight in all_edges:
            G.add_edge(head, tail, relation=relation, weight=weight)
    
    print(f'Visualisation: {G.number_of_nodes()} nœuds, {G.number_of_edges()} arêtes')
    
    # Créer la visualisation
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
    
    # Détecter le type de nœuds
    n_artists_actual = None
    if dataset_info and 'n_artists_actual' in dataset_info:
        n_artists_actual = dataset_info['n_artists_actual']
    
    # Colorier les nœuds selon leur type
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if n_artists_actual and node >= n_artists_actual:
            node_colors.append('orange')  # Utilisateurs
            node_sizes.append(400)
        else:
            node_colors.append('lightblue')  # Artistes
            node_sizes.append(300)
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=node_sizes, alpha=0.8)
    
    # Dessiner les arêtes par type de relation
    relation_colors = {
        0: 'blue',      # listened_to
        1: 'green',     # listened_by
        2: 'red',       # similar_to
        3: 'purple'     # similar_from
    }
    
    # Grouper les arêtes par relation
    edges_by_relation = defaultdict(list)
    for u, v in G.edges():
        relation = G[u][v].get('relation', 0)
        edges_by_relation[relation].append((u, v))
    
    # Dessiner les arêtes par relation avec des couleurs différentes
    for relation, edges in edges_by_relation.items():
        color = relation_colors.get(relation, 'gray')
        nx.draw_networkx_edges(G, pos, edgelist=edges, 
                              edge_color=color, arrows=True, 
                              arrowsize=8, alpha=0.5, width=1.0)
    
    # Labels seulement pour les nœuds importants
    if G.number_of_nodes() <= 30:
        labels = {node: str(node) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=7)
    
    # Titre
    title = 'Structure du Graphe de Connaissances\n'
    if dataset_info:
        if dataset_info.get('type') == 'filtered':
            title += f"Dataset filtré: {dataset_info.get('n_users_actual', '?')} users, {dataset_info.get('n_artists_actual', '?')} artists"
        else:
            title += f"Dataset complet"
    title += f'\n{G.number_of_nodes()} nœuds, {G.number_of_edges()} arêtes affichés'
    
    plt.title(title, fontsize=11, fontweight='bold')
    plt.axis('off')
    
    # Légende simple
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Patch(facecolor='lightblue', label='Artiste'),
        Patch(facecolor='orange', label='Utilisateur'),
        Line2D([0], [0], color='blue', lw=2, label='listened_to (user → artist)'),
        Line2D([0], [0], color='green', lw=2, label='listened_by (artist → user)'),
        Line2D([0], [0], color='red', lw=2, label='similar_to (artist → artist)'),
        Line2D([0], [0], color='purple', lw=2, label='similar_from (artist → artist)'),
    ]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'Visualisation sauvegardée dans: {output_file}')
    plt.close()


def visualize_relation_type(kg, relation_type, output_file='relation_visualization.png', 
                           dataset_info=None, max_nodes=50):
    """
    Visualiser un seul type de relation pour plus de clarté
    
    Args:
        kg: Dictionnaire du graphe
        relation_type: Type de relation (0, 1, 2, ou 3)
        output_file: Nom du fichier de sortie
        dataset_info: Informations sur le dataset
        max_nodes: Nombre maximum de nœuds
    """
    relation_names = {
        0: 'listened_to (user → artist)',
        1: 'listened_by (artist → user)',
        2: 'similar_to (artist → artist)',
        3: 'similar_from (artist → artist)'
    }
    
    relation_name = relation_names.get(relation_type, f'Relation {relation_type}')
    print(f'Visualisation de la relation: {relation_name}')
    
    # Obtenir n_artists_actual pour valider les types de nœuds
    n_artists_actual = None
    if dataset_info and 'n_artists_actual' in dataset_info:
        n_artists_actual = dataset_info['n_artists_actual']
        n_users_actual = dataset_info.get('n_users_actual', 0)
        print(f'  n_artists_actual = {n_artists_actual}, n_users_actual = {n_users_actual}')
        print(f'  Range attendu: artistes 0-{n_artists_actual-1}, users {n_artists_actual}-{n_artists_actual+n_users_actual-1}')
    else:
        print(f'  ⚠️ n_artists_actual non trouvé dans dataset_info, validation désactivée')
    
    G = nx.DiGraph()
    all_nodes = set()
    all_edges = []
    invalid_edges = []  # Pour détecter les erreurs
    nodes_out_of_range = set()  # Pour détecter les nœuds hors plage
    
    # Collecter seulement les arêtes du type de relation spécifié
    for head, tails in kg.items():
        for tail_info in tails:
            if len(tail_info) == 3:
                tail, relation, weight = tail_info
            else:
                tail, relation = tail_info
                weight = 1
            
            if relation == relation_type:
                # Vérifier si les nœuds sont dans la plage attendue
                if n_artists_actual:
                    n_users_actual = dataset_info.get('n_users_actual', 0) if dataset_info else 0
                    max_node = n_artists_actual + n_users_actual - 1
                    if head > max_node or tail > max_node:
                        nodes_out_of_range.add(head)
                        nodes_out_of_range.add(tail)
                
                # Valider que les types de nœuds correspondent à la relation
                is_valid = True
                if n_artists_actual:
                    head_is_user = head >= n_artists_actual
                    tail_is_user = tail >= n_artists_actual
                    
                    if relation_type == 0:  # listened_to: user → artist
                        if not (head_is_user and not tail_is_user):
                            invalid_edges.append((head, tail, f"devrait être user → artist (head={head} {'user' if head_is_user else 'artist'}, tail={tail} {'user' if tail_is_user else 'artist'})"))
                            is_valid = False
                    elif relation_type == 1:  # listened_by: artist → user
                        if not (not head_is_user and tail_is_user):
                            invalid_edges.append((head, tail, f"devrait être artist → user (head={head} {'user' if head_is_user else 'artist'}, tail={tail} {'user' if tail_is_user else 'artist'})"))
                            is_valid = False
                    elif relation_type in [2, 3]:  # similar_to/similar_from: artist → artist
                        if head_is_user or tail_is_user:
                            invalid_edges.append((head, tail, f"devrait être artist → artist (head={head} {'user' if head_is_user else 'artist'}, tail={tail} {'user' if tail_is_user else 'artist'})"))
                            is_valid = False
                
                if is_valid:
                    all_nodes.add(head)
                    all_nodes.add(tail)
                    all_edges.append((head, tail, weight))
    
    # Afficher les erreurs si trouvées
    if nodes_out_of_range:
        print(f'  ⚠️ ATTENTION: {len(nodes_out_of_range)} nœuds hors plage détectés (premiers 10): {sorted(list(nodes_out_of_range))[:10]}')
        print(f'     Ces nœuds suggèrent que le fichier kg_final.txt provient d\'un ancien preprocessing.')
        print(f'     💡 Solution: Relancez le preprocessing pour régénérer les données.')
    
    if invalid_edges:
        print(f'  ⚠️ ATTENTION: {len(invalid_edges)} arêtes invalides trouvées (premières 5):')
        for head, tail, msg in invalid_edges[:5]:
            print(f'    - ({head}, {tail}): {msg}')
        if len(invalid_edges) > 5:
            print(f'    ... et {len(invalid_edges) - 5} autres')
        if nodes_out_of_range:
            print(f'  💡 Ces erreurs sont probablement dues à un fichier kg_final.txt obsolète.')
            print(f'     Relancez: python preprocess.py --dataset music --reduce --max_users 30 --max_artists 50 --min_co_listens 1')
    
    if len(all_edges) == 0:
        print(f'  ❌ Aucune arête valide trouvée pour {relation_name}')
        if nodes_out_of_range:
            print(f'  💡 Le fichier kg_final.txt semble obsolète. Relancez le preprocessing.')
        elif relation_type in [2, 3]:
            print(f'  💡 Suggestion: Le seuil min_co_listens est peut-être trop élevé.')
            print(f'     Relancez: python preprocess.py --dataset music --reduce --max_users 30 --max_artists 50 --min_co_listens 1')
        return
    
    # Limiter le nombre de nœuds
    if len(all_nodes) > max_nodes:
        node_degrees = defaultdict(int)
        for head, tail, weight in all_edges:
            node_degrees[head] += 1
            node_degrees[tail] += 1
        
        top_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
        selected_nodes = set([node for node, _ in top_nodes])
        
        filtered_edges = [(h, t, w) for h, t, w in all_edges 
                         if h in selected_nodes and t in selected_nodes]
        
        for node in selected_nodes:
            G.add_node(node)
        for head, tail, weight in filtered_edges:
            G.add_edge(head, tail, weight=weight)
    else:
        for node in all_nodes:
            G.add_node(node)
        for head, tail, weight in all_edges:
            G.add_edge(head, tail, weight=weight)
    
    print(f'  ✅ {G.number_of_nodes()} nœuds, {G.number_of_edges()} arêtes valides')
    
    # Visualisation
    plt.figure(figsize=(12, 9))
    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
    
    # Colorier les nœuds selon leur type
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        if n_artists_actual and node >= n_artists_actual:
            node_colors.append('orange')  # Utilisateur
            node_sizes.append(400)
        else:
            node_colors.append('lightblue')  # Artiste
            node_sizes.append(300)
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=node_sizes, alpha=0.8)
    
    # Dessiner les arêtes avec épaisseur selon poids
    if G.number_of_edges() > 0:
        weights_list = [G[u][v].get('weight', 1) for u, v in G.edges()]
        if weights_list:
            min_weight = min(weights_list)
            max_weight = max(weights_list)
            if max_weight > min_weight:
                edge_widths = [0.5 + 2.0 * (G[u][v].get('weight', 1) - min_weight) / (max_weight - min_weight) 
                              for u, v in G.edges()]
            else:
                edge_widths = [1.0] * len(G.edges())
        else:
            edge_widths = [1.0] * len(G.edges())
    else:
        edge_widths = []
    
    relation_colors_map = {
        0: 'blue',
        1: 'green',
        2: 'red',
        3: 'purple'
    }
    edge_color = relation_colors_map.get(relation_type, 'gray')
    
    nx.draw_networkx_edges(G, pos, edge_color=edge_color, 
                          arrows=True, arrowsize=10, alpha=0.6, width=edge_widths)
    
    # Labels
    if G.number_of_nodes() <= 30:
        labels = {node: str(node) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    # Titre avec validation
    title = f'Relation: {relation_name}\n'
    title += f'{G.number_of_nodes()} nœuds, {G.number_of_edges()} arêtes'
    if invalid_edges:
        title += f'\n⚠️ {len(invalid_edges)} arêtes invalides ignorées'
    plt.title(title, fontsize=11, fontweight='bold')
    plt.axis('off')
    
    # Légende
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='lightblue', label='Artiste'),
        Patch(facecolor='orange', label='Utilisateur'),
        Patch(facecolor='white', edgecolor='none', label='---'),
        Patch(facecolor='white', edgecolor='none', label='Épaisseur = Poids (plus épais = plus fort)'),
    ]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f'  Sauvegardé dans: {output_file}')
    plt.close()


def visualize_all_relations(kg, output_dir='.', dataset_info=None, max_nodes=50):
    """
    Créer une visualisation pour chaque type de relation
    
    Args:
        kg: Dictionnaire du graphe
        output_dir: Répertoire de sortie
        dataset_info: Informations sur le dataset
        max_nodes: Nombre maximum de nœuds par visualisation
    """
    print('\n=== Génération des visualisations par type de relation ===')
    
    relation_names = {
        0: 'listened_to',
        1: 'listened_by',
        2: 'similar_to',
        3: 'similar_from'
    }
    
    output_files = []
    for relation_type in [0, 1, 2, 3]:
        relation_name = relation_names[relation_type]
        output_file = os.path.join(output_dir, f'graph_relation_{relation_name}.png')
        visualize_relation_type(kg, relation_type, output_file, dataset_info, max_nodes)
        output_files.append(output_file)
    
    return output_files


def get_graph_statistics(kg):
    """
    Obtenir des statistiques sur le graphe
    
    Args:
        kg: Dictionnaire {head: [(tail, relation, weight), ...]}
    
    Returns:
        Dictionnaire avec les statistiques
    """
    all_nodes = set()
    all_edges = []
    node_degrees = defaultdict(int)
    relation_counts = defaultdict(int)
    
    for head, tails in kg.items():
        all_nodes.add(head)
        for tail_info in tails:
            if len(tail_info) == 3:
                tail, relation, weight = tail_info
            else:
                tail, relation = tail_info
                weight = 1
            
            all_nodes.add(tail)
            all_edges.append((head, tail, relation, weight))
            node_degrees[head] += 1
            node_degrees[tail] += 1
            relation_counts[relation] += 1
    
    degrees = list(node_degrees.values())
    
    stats = {
        'nombre_noeuds': len(all_nodes),
        'nombre_aretes': len(all_edges),
        'nombre_relations': len(relation_counts),
        'degre_moyen': np.mean(degrees) if degrees else 0,
        'degre_max': max(degrees) if degrees else 0,
        'degre_min': min(degrees) if degrees else 0,
        'distribution_relations': dict(relation_counts)
    }
    
    return stats


def print_graph_statistics(kg, dataset_info=None):
    """
    Afficher les statistiques du graphe en français
    
    Args:
        kg: Dictionnaire du graphe
        dataset_info: Dictionnaire avec info sur le dataset
    """
    stats = get_graph_statistics(kg)
    
    dataset_type = "FILTRÉ" if dataset_info and dataset_info.get('type') == 'filtered' else "COMPLET"
    
    print('\n=== Statistiques du Graphe ===')
    print(f'Type de dataset: {dataset_type}')
    if dataset_info:
        if 'n_entity' in dataset_info:
            print(f'Entités totales: {dataset_info["n_entity"]}')
        if 'n_relation' in dataset_info:
            print(f'Types de relations: {dataset_info["n_relation"]}')
    print(f'Nombre de nœuds: {stats["nombre_noeuds"]}')
    print(f'Nombre d\'arêtes: {stats["nombre_aretes"]}')
    print(f'Nombre de types de relations: {stats["nombre_relations"]}')
    print(f'Degré moyen: {stats["degre_moyen"]:.2f}')
    print(f'Degré maximum: {stats["degre_max"]}')
    print(f'Degré minimum: {stats["degre_min"]}')
    print(f'\nDistribution des relations:')
    relation_names = {
        0: 'listened_to (user -> artist)',
        1: 'listened_by (artist -> user)',
        2: 'similar_to (artist -> artist)',
        3: 'similar_from (artist -> artist reverse)'
    }
    for relation, count in sorted(stats['distribution_relations'].items()):
        relation_name = relation_names.get(relation, f'Relation {relation}')
        print(f'  {relation_name}: {count} occurrences')
    print('=' * 30 + '\n')


def visualize_algorithm_result(kg, algorithm_name, result, start_nodes=None, 
                               output_file='algorithm_result.png', dataset_info=None):
    """
    Visualiser le résultat d'un algorithme spécifique
    (Conservé pour les algorithmes futurs)
    
    Args:
        kg: Dictionnaire du graphe {head: [(tail, relation, weight), ...]}
        algorithm_name: Nom de l'algorithme
        result: Résultat de l'algorithme
        start_nodes: Nœuds de départ
        output_file: Fichier de sortie
        dataset_info: Informations sur le dataset
    """
    print(f'Visualisation du résultat de {algorithm_name}...')
    # Cette fonction sera implémentée quand les algorithmes seront prêts
    pass
