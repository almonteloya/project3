import numpy as np
import heapq as hp
from typing import Union

class Graph:
    def __init__(self, adjacency_mat: Union[np.ndarray, str]):
        """ Unlike project 2, this Graph class takes an adjacency matrix as input. `adjacency_mat` 
        can either be a 2D numpy array of floats or the path to a CSV file containing a 2D numpy array of floats.

        In this project, we will assume `adjacency_mat` corresponds to the adjacency matrix of an undirected graph
        """
        if type(adjacency_mat) == str:
            self.adj_mat = self._load_adjacency_matrix_from_csv(adjacency_mat)
        elif type(adjacency_mat) == np.ndarray:
            self.adj_mat = adjacency_mat
        else: 
            raise TypeError('Input must be a valid path or an adjacency matrix')
        self.mst = None

    def _load_adjacency_matrix_from_csv(self, path: str) -> np.ndarray:
        with open(path) as f:
            return np.loadtxt(f, delimiter=',')

    def construct_mst(self : np.array): 
        """
        This method will implement a Prim algorithm to construct an adjacency 
        matrix to produce a minimum spanning tree. 
        
        `self.adj_mat` is a 2D numpy array of floats.
        Note that because we assume our input graph is undirected, `self.adj_mat` is symmetric.        
        
        """
        self.__convert_matrix__()
        ## create a matrix of zeros shaped like the adj matrix
        mst = np.zeros(self.adj_mat.shape)
        ## Choose the first starting vertex
        first = next(iter(self.adjacent_list))
        ## create a list to keep track of the visited nodes, add the first one
        visited = [first]
        ## priority queue to add the edges and path
        priority_q = []
        for node, weight in self.adjacent_list[first].items():
            priority_q.append((weight, first, node))
            ## add a tupple with the edge, the first vertex and the vertex connected to them
        #use heapq to keep track of the min value
        hp.heapify(priority_q)
        while priority_q:
            weight, prev, node = hp.heappop(priority_q)
            ## if we haven't visit the node explore it
            if node not in visited:
                ## add to the visited nodes
                visited.append(node)
                ##return the min edge weight to the according positions
                mst[prev,node] = weight
                ## since is a symetrical matrix do the same for the other position
                mst[node,prev] = weight
                #for each of the neighbors of the selected node if we haven't visit
                for to_next, weight in self.adjacent_list[node].items():
                    if to_next not in visited:
                        ## add them weight into the priority queue
                        hp.heappush(priority_q, (weight, node, to_next))
        self.mst = mst

        return self
    
    def __convert_matrix__(self):
        """
        Converts the adjency matrix to a adjency list using dictionaries, 
        keeping only the edges with no zero values so it's easier to traverse
        Returns a self.adjency list to be used in Prim MST
        -------

        """
        self.adjacent_list={}
        for i in range(len(self.adj_mat)):
            ##create a nested disctionary for every column
            self.adjacent_list[i] = {}
            for j in range(len(self.adj_mat[i])):
                        ## only add no zero values
                       if self.adj_mat[i][j]!= 0:
                           # add the wight of the edjes as values associated with a key (node is connecting) 
                            self.adjacent_list[i][j] = (self.adj_mat[i][j])
                    
        return self


