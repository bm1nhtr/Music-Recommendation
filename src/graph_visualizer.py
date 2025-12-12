"""
Module pour visualiser le graphe de connaissances
Utilise networkx et matplotlib pour créer des visualisations
"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import defaultdict


def visualize_graph(kg, max_nodes=100, max_edges=200, output_file='graph_visualization.png', 
                   dataset_info=None):
    """
    Visualiser le graphe de connaissances
    
    Args:
        kg: Dictionnaire {head: [(tail, relation), ...]}
        max_nodes: Nombre maximum de nœuds à afficher (pour éviter la surcharge)
        max_edges: Nombre maximum d'arêtes à afficher
        output_file: Nom du fichier de sortie
        dataset_info: Dictionnaire avec info sur le dataset (type: 'full' ou 'filtered', n_entity, n_relation)
    """
    print(f'Création de la visualisation du graphe ...')
    
    # Créer un graphe NetworkX
    G = nx.DiGraph()
    
    # Compter les nœuds et arêtes
    all_nodes = set()
    all_edges = []
    
    for head, tails in kg.items():
        all_nodes.add(head)
        for tail, relation in tails:
            all_nodes.add(tail)
            all_edges.append((head, tail, relation))
    
    # Déterminer le type de dataset
    dataset_type = "FILTRÉ" if dataset_info and dataset_info.get('type') == 'filtered' else "COMPLET"
    if dataset_info:
        print(f'Type de dataset: {dataset_type}')
        if 'n_entity' in dataset_info:
            print(f'Entités totales: {dataset_info["n_entity"]}')
        if 'n_relation' in dataset_info:
            print(f'Types de relations: {dataset_info["n_relation"]}')
    
    print(f'Graphe total: {len(all_nodes)} nœuds, {len(all_edges)} arêtes')
    
    # Limiter le nombre de nœuds et arêtes pour la visualisation
    if len(all_nodes) > max_nodes:
        print(f'Limitation à {max_nodes} nœuds pour la visualisation ...')
        # Prendre les nœuds avec le plus de connexions
        node_degrees = defaultdict(int)
        for head, tails in kg.items():
            node_degrees[head] += len(tails)
            for tail, _ in tails:
                node_degrees[tail] += 1
        
        # Trier par degré et prendre les top nodes
        top_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
        selected_nodes = set([node for node, _ in top_nodes])
        
        # Filtrer les arêtes pour ne garder que celles connectant les nœuds sélectionnés
        filtered_edges = [(h, t, r) for h, t, r in all_edges 
                         if h in selected_nodes and t in selected_nodes][:max_edges]
        
        # Ajouter les nœuds et arêtes au graphe
        for node in selected_nodes:
            G.add_node(node)
        for head, tail, relation in filtered_edges:
            G.add_edge(head, tail, relation=relation)
    else:
        # Ajouter tous les nœuds et arêtes
        for node in all_nodes:
            G.add_node(node)
        edges_to_add = all_edges[:max_edges]
        for head, tail, relation in edges_to_add:
            G.add_edge(head, tail, relation=relation)
    
    print(f'Visualisation: {G.number_of_nodes()} nœuds, {G.number_of_edges()} arêtes')
    
    # Créer la visualisation
    plt.figure(figsize=(16, 12))
    
    # Utiliser un layout spring pour une meilleure distribution
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Dessiner les nœuds
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=300, alpha=0.7)
    
    # Dessiner les arêtes
    nx.draw_networkx_edges(G, pos, edge_color='gray', 
                          arrows=True, arrowsize=10, alpha=0.5, width=0.5)
    
    # Dessiner les labels (seulement pour quelques nœuds pour éviter la surcharge)
    if G.number_of_nodes() <= 50:
        labels = {node: str(node) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    # Créer le titre avec info dataset
    title = f'Vue MACRO - Graphe de Connaissances - Dataset {dataset_type}\n'
    title += f'{G.number_of_nodes()} nœuds affichés (sur {len(all_nodes)} total), {G.number_of_edges()} arêtes affichées (sur {len(all_edges)} total)'
    if dataset_info:
        if dataset_info.get('type') == 'filtered':
            title += f'\nDataset filtré: {dataset_info.get("n_users_actual", "?")} users, {dataset_info.get("n_artists_actual", "?")} artists'
        title += f'\nTotal entités: {dataset_info.get("n_entity", len(all_nodes))}, Relations: {dataset_info.get("n_relation", "?")} types'
    
    plt.title(title, fontsize=12, fontweight='bold')
    plt.axis('off')
    
    # Ajouter une légende détaillée
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='lightblue', label='Nœud = Entité (Artiste ou Utilisateur)'),
        Patch(facecolor='gray', alpha=0.5, label='Arête = Relation (listened_to, similar_to, etc.)'),
    ]
    if dataset_info and dataset_info.get('type') == 'filtered':
        legend_elements.append(Patch(facecolor='lightgreen', alpha=0.3, label='Dataset Filtré (sous-ensemble)'))
    
    # Ajouter des explications
    legend_elements.append(Patch(facecolor='white', edgecolor='none', label='---'))
    legend_elements.append(Patch(facecolor='white', edgecolor='none', label=f'Note: Affichage limité à {max_nodes} nœuds'))
    legend_elements.append(Patch(facecolor='white', edgecolor='none', label='pour lisibilité. Graphe complet plus grand.'))
    
    plt.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.95)
    
    plt.tight_layout()
    
    # Sauvegarder
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f'Visualisation sauvegardée dans: {output_file}')
    plt.close()


def visualize_subgraph(kg, start_nodes, max_hops=2, output_file='subgraph_visualization.png',
                      dataset_info=None, relation_filter=None):
    """
    Visualiser un sous-graphe à partir de nœuds de départ
    
    Args:
        kg: Dictionnaire {head: [(tail, relation), ...]}
        start_nodes: Liste des nœuds de départ (artistes écoutés par l'utilisateur)
        max_hops: Nombre maximum de hops à explorer
        output_file: Nom du fichier de sortie (sans extension, sera ajouté selon relation)
        dataset_info: Dictionnaire avec info sur le dataset
        relation_filter: Si spécifié, seulement visualiser cette relation (0, 1, 2, ou 3)
                        None = créer plusieurs figures, une par relation
    """
    dataset_type = "FILTRÉ" if dataset_info and dataset_info.get('type') == 'filtered' else "COMPLET"
    
    # Relation names
    relation_names = {
        0: 'listened_to',      # user -> artist
        1: 'listened_by',      # artist -> user
        2: 'similar_to',       # artist -> artist
        3: 'similar_from'      # artist -> artist (reverse)
    }
    
    # Si relation_filter est None, créer une figure pour chaque relation
    relations_to_visualize = [relation_filter] if relation_filter is not None else [0, 1, 2, 3]
    
    n_artists_actual = None
    if dataset_info and 'n_artists_actual' in dataset_info:
        n_artists_actual = dataset_info['n_artists_actual']
    
    output_files = []
    
    for relation_type in relations_to_visualize:
        relation_name = relation_names.get(relation_type, f'relation_{relation_type}')
        
        print(f'Création de la visualisation du sous-graphe (relation: {relation_name}) depuis {len(start_nodes)} nœuds de départ...')
        
        G = nx.DiGraph()
        visited = set()
        queue = [(node, 0) for node in start_nodes]  # (node, hop_level)
        
        # BFS pour explorer le sous-graphe, mais seulement avec la relation spécifiée
        while queue:
            node, hop = queue.pop(0)
            
            if hop > max_hops or node in visited:
                continue
            
            visited.add(node)
            G.add_node(node)
            
            if node in kg:
                for tail, relation in kg[node]:
                    # Filtrer par relation type
                    if relation == relation_type:
                        G.add_edge(node, tail, relation=relation)
                        if tail not in visited and hop < max_hops:
                            queue.append((tail, hop + 1))
        
        if G.number_of_edges() == 0:
            print(f'  Aucune arête trouvée pour la relation {relation_name}, saut...')
            continue
        
        print(f'  Sous-graphe: {G.number_of_nodes()} nœuds, {G.number_of_edges()} arêtes')
        
        # Visualisation
        plt.figure(figsize=(14, 10))
        
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Colorier les nœuds selon leur type
        node_colors = []
        node_sizes = []
        for node in G.nodes():
            if node in start_nodes:
                # Nœuds de départ (artistes écoutés par l'utilisateur)
                node_colors.append('red')
                node_sizes.append(500)
            elif n_artists_actual and node >= n_artists_actual:
                # Utilisateurs
                node_colors.append('orange')
                node_sizes.append(350)
            else:
                # Autres artistes
                node_colors.append('lightblue')
                node_sizes.append(300)
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.8)
        nx.draw_networkx_edges(G, pos, edge_color='gray', 
                              arrows=True, arrowsize=15, alpha=0.6, width=1)
        
        # Labels
        labels = {node: str(node) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=9)
        
        # Compter les connexions
        total_connections = sum(len([(t, r) for t, r in kg.get(node, []) if r == relation_type]) 
                               for node in start_nodes)
        
        title = f'Vue MICRO - Relation: {relation_name} - Dataset {dataset_type}\n'
        title += f'{len(start_nodes)} artistes de départ → {G.number_of_nodes()} nœuds connectés, {G.number_of_edges()} arêtes'
        title += f'\nExploration: {max_hops} hops avec relation {relation_type} ({relation_name})'
        
        plt.title(title, fontsize=12, fontweight='bold')
        plt.axis('off')
        
        # Ajouter une légende détaillée
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='red', label='Nœud de départ = Artiste écouté par l\'utilisateur'),
        ]
        
        if n_artists_actual:
            if relation_type in [1]:  # listened_by: artist -> user
                legend_elements.append(Patch(facecolor='orange', label='Nœud = Utilisateur (via listened_by)'))
            elif relation_type in [2, 3]:  # similar_to/similar_from: artist -> artist
                legend_elements.append(Patch(facecolor='lightblue', label='Nœud = Autre Artiste (via similar_to)'))
            else:  # listened_to: user -> artist (ne devrait pas apparaître dans micro)
                legend_elements.append(Patch(facecolor='lightblue', label='Nœud = Artiste'))
        else:
            legend_elements.append(Patch(facecolor='lightblue', label='Nœud connecté'))
        
        legend_elements.append(Patch(facecolor='gray', alpha=0.6, 
                                    label=f'Relation = {relation_name} (type {relation_type})'))
        
        # Ajouter des explications
        legend_elements.append(Patch(facecolor='white', edgecolor='none', label='---'))
        if relation_type == 1:  # listened_by
            legend_elements.append(Patch(facecolor='white', edgecolor='none', 
                                        label=f'Cette relation montre: Artistes → Users'))
            legend_elements.append(Patch(facecolor='white', edgecolor='none', 
                                        label=f'Les users qui ont aussi écouté ces artistes'))
        elif relation_type in [2, 3]:  # similar_to/similar_from
            legend_elements.append(Patch(facecolor='white', edgecolor='none', 
                                        label=f'Cette relation montre: Artistes → Artistes'))
            legend_elements.append(Patch(facecolor='white', edgecolor='none', 
                                        label=f'Artistes similaires (co-listening)'))
        
        legend_elements.append(Patch(facecolor='white', edgecolor='none', 
                                    label=f'Total connexions: {total_connections}'))
        
        plt.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.95)
        
        plt.tight_layout()
        
        # Générer le nom de fichier avec le type de relation
        base_output = output_file.replace('.png', '')
        relation_output = f'{base_output}_{relation_name}.png'
        plt.savefig(relation_output, dpi=300, bbox_inches='tight')
        print(f'  Visualisation sauvegardée dans: {relation_output}')
        output_files.append(relation_output)
        plt.close()
    
    return output_files


def get_graph_statistics(kg):
    """
    Obtenir des statistiques sur le graphe
    
    Args:
        kg: Dictionnaire {head: [(tail, relation), ...]}
    
    Returns:
        Dictionnaire avec les statistiques
    """
    all_nodes = set()
    all_edges = []
    node_degrees = defaultdict(int)
    relation_counts = defaultdict(int)
    
    for head, tails in kg.items():
        all_nodes.add(head)
        for tail, relation in tails:
            all_nodes.add(tail)
            all_edges.append((head, tail, relation))
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
        dataset_info: Dictionnaire avec info sur le dataset (type, n_entity, n_relation)
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

