import networkx as nx
import random


# Generates a list D of graphs with L elements, where each graph G_i is obtained by rewiring one link in G_{i-1}. The first graph in the list is  generated using ER(n, p), where n is the number of nodes and p is the probability that each pair of nodes has a connection betwen them. 
# Returns the list D and the list D_metric which is subdivides the interval [0,1] into equidistant subsections, such that each subsection is [k/L, (k+1)/L], k = 0,1, ..., L-1
def generate_dictionary(n, p, L, seed=0):
        
    random.seed(seed)
    # Use seed for reproducibility
    G1 = nx.erdos_renyi_graph(n, p, seed=seed)
    G_fully_connected = nx.complete_graph(n)


    D = [None]*L # Dictionary proper
    D_metric = [None]*(L+1) # metric space of intervals in [0, 1]
    D[0] = G1
    D_metric[0] = 0
    D_metric[-1] = 1

    # Defines the history of edge rewiring
    links_original = G1.edges
    links_fully_connected = G_fully_connected.edges
    links_net_yet_connected = list(links_fully_connected - links_original)


    links_original = [key for key in links_original.keys()]
    links_fully_connected = [key for key in links_fully_connected.keys()]

    for i in range(1, L):
        # New graph iteration
        D[i] = D[i-1].copy()
        D_metric[i] = i/L
        
        link_to_remove = random.choice(links_original)
        link_to_add = random.choice(links_net_yet_connected)

        # Rewire the new graph
        D[i].remove_edge(v=link_to_remove[0], u=link_to_remove[1]) 
        D[i].add_edge(link_to_add[0], link_to_add[1])

        links_original.remove(link_to_remove) # I can no longer remove this link
        links_net_yet_connected.remove(link_to_add) # I can no longer add this link
    return D, tuple(D_metric)



# Encodes a univariate time series into a sequence of graphs using the graph dictionary D and its associated metric space D_metric. 
# Returns a sequence of graphs tn, which are drawn from D
def encode_ts_into_tn(y, D, D_metric):
    tn = [None]*len(y)
    ks = [None]*len(y)
    for i in range(len(y)):
        managed_to_fit = False
        for k in range(len(D_metric)):
        
            if D_metric[k] <= y[i] and  y[i] < D_metric[k+1]:
                # y[i] fits into the [k/L, k+1/L] interval -> Map it into D[k]
                tn[i] = D[k].copy()
                ks[i] = k 
                managed_to_fit = True

        if not managed_to_fit:
            # Should not print anything
            print(y[i])
    return tn, ks