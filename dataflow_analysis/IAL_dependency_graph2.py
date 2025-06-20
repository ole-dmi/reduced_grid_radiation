import glob
import os
import chardet
import json
import networkx as nx
import matplotlib.pyplot as plt

import sys

#------------------------------------------------------------------------------
# Recursive function to extract connected keys and values from a dictionary
#------------------------------------------------------------------------------
def extract_connected_keys_values(dictionary, start_key):
    results = {}

    print(start_key, dictionary[start_key])
    list = dictionary[start_key]
    results[start_key] = list
    for item in list:
        if item in dictionary and item not in results:
            results[item] = dictionary[item]
            results.update(extract_connected_keys_values(dictionary, item))

    return results

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
if len(sys.argv) != 2:
    print('Usage: python IAL_dependency_graph.py <root_subroutine>')
    sys.exit(1)

root_subroutine = sys.argv[1]
    

print(f'Root subroutine: {root_subroutine}')

file_path = 'subroutine_connections.json'
with open(file_path, 'r') as file:
    graph_dict = json.load(file)
print(f'Loaded {len(graph_dict)} nodes from {file_path}')

# Remove newline characters from the dictionary keys
graph_dict = {key.replace('\n', ''): value for key, value in graph_dict.items()}
for key, value in graph_dict.items():
    graph_dict[key] = [v.replace('\n', '') for v in value]

#for key, value in graph_dict.items():
#    print(key, value)

print(graph_dict[root_subroutine])

start_key = root_subroutine
extracted_data = extract_connected_keys_values(graph_dict, start_key)

# Print the extracted data
print(f"Extracted data starting from '{start_key}':")
for path, value in extracted_data.items():
    print(f"{path}, {value}")

print('Creating a graph from the dictionary...')
#G = nx.Graph()
G = nx.DiGraph()

# Add nodes from the dictionary keys
G.add_nodes_from(extracted_data.keys())

# Add edges from the dictionary values
for node, neighbors in extracted_data.items():
    for neighbor in neighbors:
        G.add_edge(node, neighbor)


A = nx.nx_agraph.to_agraph(G)  # convert to a graphviz graph
A.write(f'{root_subroutine}.dot')  # write to simple.dot
os.system(f"dot -Tpdf {root_subroutine}.dot -o {root_subroutine}.pdf")  # convert to png