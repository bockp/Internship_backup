import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import write_dot
# Dependency NetworkX + pydot


# opens complete.csv as seqInfo, so we can process it.
# the with XX as YY:
# is the most secure/preferred way to open files.


def seqInfoExtractor(seq):
    # function to extract team name, sequence length and
    # sequence name from the csv line
    # and fuse it into a valid NetworkX node
    rest,seqLen = seq.split("_length=")
    # joins with "-" the first two elements gained by splitting on "-"
    # little trickery needed since "-" is present in the team name XS
    seqTeam = "-".join(rest.split("-",2)[0:2])
    seqName = rest.split("-",2)[2]


    return seqName,int(seqLen),seqTeam




node_List = []



G0 = nx.Graph()

x = set()

with open("./graph/complete.csv","rb") as blastFile:
    for comparison in blastFile:
        # get the two node names, keeping the common stats separated
        # to be reused as edge information later on.
        seqAInfo, seqBInfo ,edge_info = comparison.split("\t",2)
        # get ind. sequence information from sequence identifiers:
        seqAName, seqALen,seqATeam = seqInfoExtractor(seqAInfo)
        seqBName, seqBLen,seqBTeam = seqInfoExtractor(seqBInfo)




        # add sequences as nodes by their names (W/O team and length)
        # nodes being a set, there's no need to check for repeat elements
        G0.add_node(seqAName)

        G0.add_node(seqBName)

        # Add associated data to each node
        G0.node[seqAName]["Team"]   = seqATeam
        G0.node[seqAName]["Length"] = seqALen

        G0.node[seqBName]["Team"]   = seqBTeam
        G0.node[seqBName]["Length"] = seqBLen

        # add edge information

        # extract edge info we want to keep (% ident, coverage, e-val, bitscore)
        edgeMetadata = edge_info.strip("\n").split("\t")
        id,cov = edgeMetadata[0:2]
        eval,bitsc =edgeMetadata[8:11]

        G0.add_edge(seqAName,seqBName,attr_dict={"Identity%":float(id),"Coverage": int(cov),"e-value": float(eval),"bitscore": float(bitsc)})




# Create subgraphs for each connected component, representing a set of sequences
# identified as equal.

graphs = list(nx.connected_component_subgraphs(G0, copy=True))


print("Writing Dot files for each Connected Components")

# Write each connected component in separate DOT files.


#for every graph in the connected components list:

for i in range(0,len(graphs)):
    print("processing connected component #" + str(i) + "\n")
    write_dot(graphs[i], "connectedComponents/ConnectedComponent%03d.dot" % i )
    #print("\nSet positions for graph#" + str(i) + "\n")
    ## !!! I need to study which layout is best !!!
    pos = nx.spring_layout(graphs[i])

    #print("Draw graph #"+str(i)+"\n")
    drawn = nx.draw(graphs[i], pos)
    #print("setting edge and node labels for graph #" + str(i) + "\n")
    node_labels = nx.get_node_attributes(graphs[i],'Team')
    nx.draw_networkx_labels(graphs[i], pos, labels = node_labels)
    #edge_labels = nx.get_edge_attributes(graphs[i],'Identity%')
    #nx.draw_networkx_edge_labels(graphs[i], pos, labels = edge_labels)

    plt.savefig("connectedComponents/ConnectedComponent%03d.png" % i)
    plt.close()



#print("\nSet positions for a graph\n")
## !!! I need to study which layout is best !!!
#pos = nx.spring_layout(graphs[i])
# draws graph using default method

#print("Draw a graph\n")
#A = nx.draw(graphs[i], pos)


#print("Add labels\n")

# uses Node and Edge data as labels for the graphic.
#node_labels = nx.get_node_attributes(graphs[5],'Team')
#nx.draw_networkx_labels(graphs[5], pos, labels = node_labels)
#edge_labels = nx.get_edge_attributes(graphs[5],'Identity%')
#nx.draw_networkx_edge_labels(graphs[5], pos, edge_labels)

#plt.savefig('GraphSharedElements.png')

# I think this is where I need to save it to dot format.


# displays graph.
# this destroys the graph object in the variable,
# so have a backup !
#print("Show one of the graphs\n")
#plt.show(A)