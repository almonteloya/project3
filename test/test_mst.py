# write tests for bfs
import pytest
import numpy as np
from mst import Graph
from sklearn.metrics import pairwise_distances


def check_mst(adj_mat: np.ndarray, 
              mst: np.ndarray, 
              expected_weight: int, 
              allowed_error: float = 0.0001):
    """ Helper function to check the correctness of the adjacency matrix encoding an MST.
        Note that because the MST of a graph is not guaranteed to be unique, we cannot 
        simply check for equality against a known MST of a graph. 

        Arguments:
            adj_mat: Adjacency matrix of full graph
            mst: Adjacency matrix of proposed minimum spanning tree
            expected_weight: weight of the minimum spanning tree of the full graph
            allowed_error: Allowed difference between proposed MST weight and `expected_weight`

        TODO: 
            Add additional assertions to ensure the correctness of your MST implementation
        For example, how many edges should a minimum spanning tree have? Are minimum spanning trees
        always connected? What else can you think of?
    """
    def approx_equal(a, b):
        return abs(a - b) < allowed_error

    total = 0
    for i in range(mst.shape[0]):
        for j in range(i+1):
            total += mst[i, j]
    assert approx_equal(total, expected_weight), 'Proposed MST has incorrect expected weight' 
    assert mst.T.all() == mst.all() ## checking if is symetrical using the transpose
    ## checking that we have n-1 edges 
    assert (np.argwhere(mst).shape[0]/2) == mst.shape[0]-1 ## counting the no-zero edges, then divide by 2 since its symetrical
    assert set(mst.flatten()).issubset(set(adj_mat.flatten())) ## check if the mst values are a subset of the adjency matrix

    
def test_mst_small():
    """ Unit test for the construction of a minimum spanning tree on a small graph """
    file_path = './data/small.csv'
    g = Graph(file_path)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 8)



def test_mst_single_cell_data():
    """ Unit test for the construction of a minimum spanning tree using 
    single cell data, taken from the Slingshot R package 
    (https://bioconductor.org/packages/release/bioc/html/slingshot.html)
    """
    file_path = './data/slingshot_example.txt'
    # load coordinates of single cells in low-dimensional subspace
    coords = np.loadtxt(file_path)
    # compute pairwise distances for all 140 cells to form an undirected weighted graph
    dist_mat = pairwise_distances(coords)
    g = Graph(dist_mat)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 57.263561605571695)


def test_mst_student():
    """ 
    I manually created a numoy array with dimessions 7x7 and
    I previousl know the shortest path is 7. 
    """
    x=np.array([[0., 2., 3., 0., 0., 0., 0.],
     [2., 0., 1. ,1., 4., 0. ,0.],
     [3., 1. ,0., 0., 0., 5. ,0.],
     [1., 0., 0., 0., 1., 0. ,0.],
     [0. ,4., 0., 1., 0., 1., 0.],
     [0. ,0., 5., 0., 1., 0., 1.],
     [0., 0., 0., 0., 0., 1., 0.]])
    g=Graph(x)
    g.construct_mst()
    check_mst(g.adj_mat, g.mst, 7)