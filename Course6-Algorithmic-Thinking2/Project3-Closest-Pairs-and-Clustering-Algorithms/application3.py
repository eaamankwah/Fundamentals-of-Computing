import alg_project3
import alg_cluster
import alg_project3_viz as viz
import alg_clusters_matplotlib
import matplotlib.pyplot as plt
import random
import time

def gen_random_clusters(num_clusters):
	random_clusters = list()
	for cluster in range(num_clusters):
		x = random.random() * 2 - 1
		y = random.random() * 2 -1
		random_clusters.append(alg_cluster.Cluster(set([]), x, y, 0, 0))
	return random_clusters

def q1():

	num_clusters_list = range(2, 200 + 1)
	slow_time_list = list()
	fast_time_list = list()

	for num_clusters in num_clusters_list:

		clusters = gen_random_clusters(num_clusters)
		start = time.time()
		alg_project3.slow_closest_pair(clusters)
		end = time.time()
		slow_time_list.append(end - start)


		start = time.time()
		alg_project3.fast_closest_pair(clusters)
		end = time.time()
		fast_time_list.append(end - start)
	plt.xlabel('Number of initial clusters')
	plt.ylabel('Running time in seconds')
	line1, = plt.plot(num_clusters_list, slow_time_list,'g')
	line2, = plt.plot(num_clusters_list, fast_time_list,'b')
	plt.legend((line1, line2), ('slow_time_list', 'fast_time_list'))
	plt.show()

def q2():
	data_table = viz.load_data_table(viz.DATA_3108_URL)
	singleton_list = []
	for line in data_table:
		singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
	cluster_list = alg_project3.hierarchical_clustering(singleton_list, 15)
	alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)

def q3():
	data_table = viz.load_data_table(viz.DATA_3108_URL)
	singleton_list = []
	for line in data_table:
		singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
	cluster_list = alg_project3.kmeans_clustering(singleton_list, 15, 5)
	alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)


def q5():
	data_table = viz.load_data_table(viz.DATA_111_URL)
	singleton_list=[]

	for line in data_table:
		singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
	cluster_list = alg_project3.hierarchical_clustering(singleton_list, 9)
	alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)

def q6():
	data_table = viz.load_data_table(viz.DATA_111_URL)
	singleton_list=[]
	for line in data_table:
		singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
	cluster_list = alg_project3.kmeans_clustering(singleton_list, 9, 5)
	alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)


def compute_distortion(cluster_list, data_table):
	error = 0
	for cluster in cluster_list:
		error += cluster.cluster_error(data_table)
	return error


def q7():

	data_table = viz.load_data_table(viz.DATA_111_URL)
	singleton_list = []
	for line in data_table:
		singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

	cluster_list = alg_project3.kmeans_clustering(singleton_list, 9, 5)
	error2 = compute_distortion(cluster_list, data_table)

	cluster_list = alg_project3.hierarchical_clustering(singleton_list, 9)
	error1 = compute_distortion(cluster_list, data_table)

	print ('hierarchical clustering',error1)
	print ('kmeans clustering', error2)


def q10():
	nodes_list = {viz.DATA_111_URL:111, viz.DATA_290_URL:290, viz.DATA_896_URL:896}
	url_list = [viz.DATA_111_URL, viz.DATA_290_URL, viz.DATA_896_URL]

	kmeans_dict = dict()
	hierarchical_dict = dict()


	for url in url_list:
		data_table = viz.load_data_table(url)
		singleton_list = []
		for line in data_table:
			singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))


		kmeans_dict[url] = list()
		hierarchical_dict[url] = list()

		cluster_range = range(6, 20 + 1)
		for cluster_count in cluster_range:
			#kmeans
			cluster_list = alg_project3.kmeans_clustering(singleton_list, cluster_count, 5)
			kmeans_error = compute_distortion(cluster_list, data_table)
			kmeans_dict[url].append(kmeans_error)

		#hierarchical
		count = 20
		while count >= 6:
			alg_project3.hierarchical_clustering(singleton_list, count)
			hierarchical_error = compute_distortion(singleton_list, data_table)
			hierarchical_dict[url].insert(0, hierarchical_error)
			count -= 1

	for url in url_list:
		plt.title('Distortion for hierarchical and k-means clustering for '+str(nodes_list[url])+' points')
		plt.xlabel('Number of clusters')
		plt.ylabel('Distortion')
		line1, = plt.plot(cluster_range, kmeans_dict[url],'g')
		line2, = plt.plot(cluster_range, hierarchical_dict[url],'b')
		plt.legend((line1, line2), ('kmeans clustering', 'hierarchical clustering'))
		plt.show()




q1()
#q2()
#q3()
#q5()
#q6()
#q7()
#q10()
