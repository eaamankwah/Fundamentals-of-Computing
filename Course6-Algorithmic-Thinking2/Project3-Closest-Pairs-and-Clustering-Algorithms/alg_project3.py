"""
Student template code for Project 3
Student will implement five functions:
slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)
where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster

######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list
    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)
    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    closest_pair = (float('inf'), -1, -1)
    for cluster in range(len(cluster_list)):
        for added_cluster in range(cluster, len(cluster_list)):
            if cluster == added_cluster:
                continue
            pair = pair_distance(cluster_list, cluster, added_cluster)
            closest_pair = min(closest_pair, pair, key = lambda val: val[0])
    return closest_pair


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)
    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """

    size = len(cluster_list)
    if size <= 3:
        closest_pair = slow_closest_pair(cluster_list)

    else:
        #cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        mid = size // 2

        left_pair = fast_closest_pair(cluster_list[:mid])
        right_pair = fast_closest_pair(cluster_list[mid:])

        closest_pair = min(left_pair, (right_pair[0], right_pair[1]+mid, right_pair[2]+mid), key = lambda val: val[0])
        mid = 1.0 / 2 * (cluster_list[mid-1].horiz_center()+cluster_list[mid].horiz_center())

        closest_pair = min(closest_pair, closest_pair_strip(cluster_list, mid, closest_pair[0]), key = lambda val: val[0])

    return closest_pair


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.
    """
    updated_list = list()
    for cluster in cluster_list:
        if math.fabs(cluster.horiz_center() - horiz_center) < half_width:
            updated_list.append(cluster)
    updated_list.sort(key = lambda cluster: cluster.vert_center())
    cluster_size = len(updated_list)
    closest_pair = (float('inf'), -1, -1)

    for cluster in range(cluster_size - 2 + 1):
        for added_cluster in range(cluster + 1, min(cluster + 4, cluster_size)):
            pair = pair_distance(updated_list, cluster, added_cluster)
            pair = pair_distance(cluster_list, cluster_list.index(updated_list[pair[1]]),cluster_list.index(updated_list[pair[2]]))
            closest_pair = min(closest_pair, pair, key = lambda val: val[0])

    return closest_pair



######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    while len(cluster_list) > num_clusters:
        print ('cluster count:', len(cluster_list))

        closest_pair = fast_closest_pair(cluster_list)
        cluster1_pos = closest_pair[1]
        cluster2_pos = closest_pair[2]
        cluster_list[cluster1_pos].merge_clusters(cluster_list[cluster2_pos])
        del cluster_list[cluster2_pos]
    return cluster_list


######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations

    updated_list = list(cluster_list)
    updated_list.sort(key = lambda val:val.total_population(), reverse = True)
    old_clusters = updated_list[:num_clusters]

    for dummy in range(num_iterations):
            new_clusters = [alg_cluster.Cluster(set(),0,0,0,0) for dummy in range(num_clusters)]
            for cluster in updated_list:
                closest_pair = (float('inf'), -1)

                for index in range(num_clusters):
                    dist = cluster.distance(old_clusters[index])
                    pair = (dist, index)
                    closest_pair = min(closest_pair, pair, key = lambda val: val[0])

                new_clusters[closest_pair[1]].merge_clusters(cluster)
            old_clusters = new_clusters

    return old_clusters
