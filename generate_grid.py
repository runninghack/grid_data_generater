import os
import random
import copy

def get_sec1(numNodes, numEdges):
    lines = []
    lines.append("#################################################################")
    lines.append("#APDM Input Graph, this input graph includes 3 sections:")
    lines.append("#section1 : general information")
    lines.append("#section2 : nodes")
    lines.append("#section3 : edges")
    lines.append("#section4 : trueSubGraph (Optional)")
    lines.append("#")
    lines.append("#if nodes haven't information set weight to null")
    lines.append("#if nodes haven't information set weight to null")
    lines.append("#################################################################")
    lines.append("SECTION1 (General Information)")
    lines.append("numNodes = " + str(numNodes))
    lines.append("numEdges = " + str(numEdges))
    lines.append("usedAlgorithm = NULL")
    lines.append("dataSource = GridDataset")
    lines.append("END")
    return lines


def get_sec2(nodes):
    lines = []
    lines.append("#################################################################")
    lines.append("SECTION2 (Nodes Information)")

    lines.append("NodeID Weight")
    for i in range(len(nodes)):
        lines.append(str(i) + " " + str(nodes[i]))
    lines.append("END")
    return lines


def get_sec3(edges):
    lines = []
    lines.append("#################################################################")
    lines.append("SECTION3 (Edges Information)")
    lines.append("EndPoint0 EndPoint1 Weight")
    for item in edges:
        lines.append(str(item[0]) + " " + str(item[1]) + " 1.000000")
    lines.append("END")
    return lines


def get_sec4(edges):
    lines = []
    lines.append("#################################################################")
    lines.append("SECTION4 (TrueSubGraph Information)")
    lines.append("EndPoint0 EndPoint1 Weight")
    for item in edges:
        lines.append(str(item[0]) + " " + str(item[1]) + " 1.000000")
    lines.append("END")
    lines.append("#################################################################")
    return lines


def generate_weights(num):
    nodes = []
    for i in range(num):
        nodes.append(int(random.random() * 1000))
    return nodes


def generate_grid_edges(nodes):
    pairs= []
    inrange = lambda x: (x > -1) and (x < len(nodes))
    for i in range(len(nodes)):
        if inrange(i - 1):
            pairs.append([i - 1, i])
        if inrange(i - 10):
            pairs.append([i - 10, i])
    return pairs


def run(num, sparsity, noise, q):
    if noise:
        noise_str = "noise"
    else:
        noise_str = "clean"
    fout = "grid_data/grid_" + str(num) + "_"+ str(q)+ "_"+ str(sparsity) + "_" + str(noise_str)
    for f in range(10):
        _fout = fout + "_" + str(f)
        lambdas = generate_weights(num)
        weights = copy.copy(lambdas)
        edges = generate_grid_edges(weights)
        numNodes = len(weights)
        numEdges = len(edges)
        true_nodes = range(int(num * sparsity))
        for i in true_nodes:
            weights[i] = weights[i] * q

        if noise:
            weights = [a + random.random() * (0.1 * a) for a in weights]
            lambdas = [a + random.random() * (0.1 * a) for a in lambdas]

        with open(_fout+".txt",'w') as f:
            true_edges = [e for e in edges if e[0] in true_nodes and e[1] in true_nodes]
            lines = get_sec1(numNodes,numEdges) + get_sec2(weights) + get_sec3(edges) + get_sec4(true_edges)
            for l in lines:
                f.write(l + '\n')

        with open(_fout+"_lambdas"+".txt",'w') as f:
            for l in lambdas:
                f.write(str(l) + "\n")

sec_node_num = [100,400,900]
#sec_sparsity = [0.05, 0.1, 0.2]
q_value = [0.01,0.05,0.1,0.3,0.5,0.7]
sec_noise = [True,False]

for i in sec_node_num:
    for j in [2.0/i, 0.05, 0.1, 0.2]:
        for k in sec_noise:
	    for q in q_value:
                run(i, j, k, q)
