import pandas as pd
import numpy as np
import networkx as nx
from operator import itemgetter
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from itertools import count
from collections import OrderedDict
from scripts.sentiment_analysis import add_candidate


def load_data(path, date_from='2020-03-01', date_to='2020-06-15'):
    dtype = {'in_reply_to_status_id_str': str, 'in_reply_to_user_id_str': str}
    df = pd.read_json(path, dtype=dtype)
    df['created_at'] = df['created_at'].apply(lambda x: x.tz_localize(None))
    df = df.loc[df['created_at'].between(date_from, date_to, inclusive=True)]
    return df


def prepare_data(df):
    columns = ['created_at', 'id', 'user_id', 'screen_name', 'followers_count', 'full_text', 'in_reply_to_status_id',
               'in_reply_to_user_id', 'in_reply_to_screen_name', 'mentioned_user_id', 'mentioned_screen_name',
               'retweeted_status_id', 'retweeted_user_id', 'retweeted_screen_name', 'quoted_status_id',
               'quoted_user_id',
               'quoted_screen_name']
    new_df = pd.DataFrame(columns=columns)
    get_user_information(df, new_df)
    get_replies(df, new_df)
    get_retweets(df, new_df)
    get_quotes(df, new_df)
    get_mentions(df, new_df)
    return new_df


def get_user_information(df, new_df):
    new_df[['created_at', 'id', 'full_text']] = df[['created_at', 'id', 'full_text']]
    new_df['user_id'] = df['user'].apply(lambda x: x['id_str'])
    new_df['screen_name'] = df['user'].apply(lambda x: x['screen_name'])
    new_df['followers_count'] = df['user'].apply(lambda x: x['followers_count'])
    new_df['candidate'] = new_df['screen_name'].apply(lambda x: add_candidate(x))


def get_replies(df, new_df):
    new_df['in_reply_to_status_id'] = df['in_reply_to_status_id_str'].apply(lambda x: x if not x == 'None' else None)
    new_df['in_reply_to_user_id'] = df['in_reply_to_user_id_str'].apply(lambda x: x if not x == 'None' else None)
    new_df['in_reply_to_screen_name'] = df['in_reply_to_screen_name'].apply(lambda x: x if x is not None else None)


def get_retweets(df, new_df):
    if 'retweeted_status' in df.columns:
        new_df['retweeted_status_id'] = df['retweeted_status'].apply(lambda x: x['id_str'] if x is not np.nan else None)
        new_df['retweeted_user_id'] = df['retweeted_status'].apply(
            lambda x: x['user']['id_str'] if x is not np.nan else None)
        new_df['retweeted_screen_name'] = df['retweeted_status'].apply(
            lambda x: x['user']['screen_name'] if x is not np.nan else None)
    else:
        new_df['retweeted_status_id'] = None
        new_df['retweeted_user_id'] = None
        new_df['retweeted_screen_name'] = None


def get_quotes(df, new_df):
    new_df['quoted_status_id'] = df['quoted_status'].apply(lambda x: x['id_str'] if x is not np.nan else None)
    new_df['quoted_user_id'] = df['quoted_status'].apply(lambda x: x['user']['id_str'] if x is not np.nan else None)
    new_df['quoted_screen_name'] = df['quoted_status'].apply(
        lambda x: x['user']['screen_name'] if x is not np.nan else None)


def get_mentions(df, new_df):
    new_df['mentioned_user_id'] = df['entities'].apply(
        lambda x: x['user_mentions'][0]['id_str'] if x['user_mentions'] else None)
    new_df['mentioned_screen_name'] = df['entities'].apply(
        lambda x: x['user_mentions'][0]['screen_name'] if x['user_mentions'] else None)


def create_graph(df):
    graph = nx.Graph()
    for ind, row in df.iterrows():
        user, relations = get_relations(row)
        user_id, user_name = user
        tweet_id = row['id']
        for relation in relations:
            rel_id, rel_name = relation
            graph.add_edge(user_name, rel_name, tweet_id=tweet_id)
            graph.nodes[user_name]['name'] = user_name
            graph.nodes[user_name]['candidate'] = add_candidate(user_name)
            graph.nodes[rel_name]['name'] = rel_name
    component = max(nx.connected_components(graph), key=len)
    subgraph = graph.subgraph(component).copy()
    return graph, subgraph


def get_relations(row):
    user = row['user_id'], row['screen_name']
    if user[0] is None:
        return (None, None), []
    relations = set()
    relations.add((row['in_reply_to_user_id'], row['in_reply_to_screen_name']))
    relations.add((row['retweeted_user_id'], row['retweeted_screen_name']))
    relations.add((row['quoted_user_id'], row['quoted_screen_name']))
    relations.add((row['mentioned_user_id'], row['mentioned_screen_name']))
    relations.discard((row['user_id'], row['screen_name']))
    relations.discard((None, None))
    return user, relations


def general_analysis(graph, subgraph, name):
    lines = []
    print_general_info(graph, lines)
    lines.append(f'Graph connected: {nx.is_connected(graph)}')
    lines.append(f'Number of connected components: {nx.number_connected_components(graph)}')
    if not nx.is_connected(graph):
        graph = subgraph
        lines.append('Largest connected component:')
        print_general_info(graph, lines)
    lines.append(f'Average clustering coefficient: {nx.average_clustering(graph)}')
    lines.append(f'Transitivity: {nx.transitivity(graph)}')
    lines.append(f'Diameter: {nx.diameter(graph)}')
    lines.append(f'Average distance between two nodes: {nx.average_shortest_path_length(graph):.2f}')
    info = '\n'.join(lines)
    fig = plt.figure()
    plt.axis([0, 15, 0, 16])
    plt.text(1, 15, info, fontsize=11, ha='left', va='top', wrap=True)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(f'graphs\\{name}_graph_info.png')
    plt.show()


def print_general_info(graph, lines):
    lines.append(f'Number of nodes: {graph.number_of_nodes()}')
    lines.append(f'Number of edges: {graph.number_of_edges()}')
    degrees = [val for (node, val) in graph.degree()]
    lines.append(f'Max degree: {np.max(degrees)}')
    lines.append(f'Min degree: {np.min(degrees)}')
    lines.append(f'Density: {nx.density(graph)}')


def centrality(graph, name):
    degree = nx.degree_centrality(graph)
    closeness = nx.closeness_centrality(graph)
    betweenness = nx.betweenness_centrality(graph, normalized=True, endpoints=False)
    eigenvector = nx.eigenvector_centrality(graph)
    pagerank = nx.pagerank(graph)
    max_degree = get_and_print_central_nodes(graph, degree, 'degree centrality', name)
    max_closeness = get_and_print_central_nodes(graph, closeness, 'closeness centrality', name)
    max_betweenness = get_and_print_central_nodes(graph, betweenness, 'betweenness centrality', name)
    max_eigenvector = get_and_print_central_nodes(graph, eigenvector, 'eigenvector centrality', name)
    max_pagerank = get_and_print_central_nodes(graph, pagerank, 'pagerank', name)
    return [max_degree, max_closeness, max_betweenness, max_eigenvector, max_pagerank], betweenness


def get_and_print_central_nodes(graph, central_dict, metric, name):
    sorted_list = sorted(central_dict.items(), key=itemgetter(1), reverse=True)
    lines = [f'Max {metric}:']
    for node, value in sorted_list[:10]:
        user = graph.nodes[node]['name']
        lines.append(f' user: {user}    value: {value}')
    lines.append("")
    values = [value for name, value in reversed(sorted_list)]
    desc = '\n'.join(lines)
    plt.hist(values, bins=100)
    plt.ylabel('number')
    plt.xlabel(metric)
    plt.title(desc, loc='left')
    plt.savefig(f'graphs\\{name}_graph_{metric}.png', bbox_inches='tight')
    plt.show()
    return sorted_list[0][0]


def draw_hashtags_graph(graph, central_list, name, path):
    k = 0.05
    colors = ['green', 'red', 'yellow', 'silver', 'orange']
    nodelist = list(OrderedDict.fromkeys(central_list))
    colors = colors[:len(nodelist)]
    positions = nx.spring_layout(graph, k=k)
    plt.figure(figsize=(60, 60))
    nx.draw_networkx_edges(graph, pos=positions, alpha=0.6)
    nx.draw_networkx_nodes(graph, pos=positions, node_color=range(graph.number_of_nodes()), cmap=plt.cm.cool,
                           node_size=100)
    nx.draw_networkx_nodes(graph, pos=positions, nodelist=nodelist, node_color=colors, node_size=2000)
    legend_elements = [Line2D([0], [0], marker='o', color=c, markersize=40) for c in colors]
    labels = [graph.nodes[node]['name'] for node in nodelist]
    plt.legend(handles=legend_elements, labels=labels, labelspacing=3, fontsize="30")
    plt.title(f'{name} hashtags', fontsize='40')
    plt.savefig(path)
    plt.show()


def draw_candidates_graph(graph, betweenness, path):
    node_color = [20000.0 * graph.degree(v) for v in graph]
    node_size = [v * 75000 for v in betweenness.values()]
    k = 0.05
    positions = nx.spring_layout(graph, k=k)
    plt.figure(figsize=(60, 60))
    nx.draw_networkx(graph, pos=positions, node_color=node_color, node_size=node_size, with_labels=True)
    plt.savefig(path)
    plt.show()


def draw_graph_with_cat_colors(graph, category, betweenness, path):
    categories = set(nx.get_node_attributes(graph, category).values())
    categories.add('undefined')
    mapping = dict(zip(sorted(categories), count()))
    nodes = graph.nodes()
    colors = [mapping[graph.nodes[n][category] if category in graph.nodes[n] else 'undefined'] for n in nodes]
    node_size = [v * 75000 for v in betweenness.values()]
    cmap = plt.cm.gist_rainbow
    positions = nx.spring_layout(graph)
    plt.figure(figsize=(60, 60))
    nx.draw_networkx(graph, positions, alpha=0.5, with_labels=True, node_color=colors, cmap=cmap, node_size=20)
    nc = nx.draw_networkx_nodes(graph, positions, nodelist=nodes, node_color=colors, with_labels=True,
                                node_size=node_size, cmap=cmap)
    cbar = plt.colorbar(nc, ticks=range(0, 6))
    cbar.set_ticklabels(list(sorted(categories)))
    cbar.ax.tick_params(labelsize=40)
    plt.savefig(path)
    plt.show()


def sna_hashtags(path, name, outfile, date_from='2020-03-01', date_to='2020-06-15'):
    df = load_data(path, date_from, date_to)
    df = prepare_data(df)
    graph, subgraph = create_graph(df)
    general_analysis(graph, subgraph, name)
    central_list, betweenness = centrality(subgraph, name)
    draw_hashtags_graph(subgraph, central_list, name, outfile)


def sna_candidates(path, outfile1, outfile2, date_from='2020-03-01', date_to='2020-06-15'):
    df = load_data(path, date_from, date_to)
    df = prepare_data(df)
    graph, subgraph = create_graph(df)
    general_analysis(graph, subgraph, 'candidates')
    central_list, betweenness = centrality(subgraph, 'candidates')
    draw_candidates_graph(subgraph, betweenness, outfile1)
    draw_graph_with_cat_colors(graph, 'candidate', betweenness, outfile2)
