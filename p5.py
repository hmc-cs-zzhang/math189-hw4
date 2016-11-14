import os
import numpy as np
import matplotlib.pyplot as plt
import sklearn.feature_extraction.text as text

def NMF(V, r, max_iter=200, tolerance=1e-6, print_freq=20):
	n = V.shape[0]
	m = V.shape[1]
	obj = []

	def genW(row, col, W, VHt, WHHt):
		return W.item(row, col) * (VHt.item(row, col)) / (WHHt.item(row, col))

	def genH(row, col, H, WtV, WtWH):
		return H.item(row, col) * (WtV.item(row, col)) / (WtWH.item(row, col))

	# W: n x r, H: r x m
	W, H = np.mean(V) * np.matrix(np.random.rand(n, r)), np.mean(V) * np.matrix(np.random.rand(r, m))
	for iter in range(max_iter):

		if len(obj) > 0 and iter % print_freq == 0:
			print "[i={}] obj={}".format(iter, obj[-1])

		VHt = V * H.transpose()
		WHHt = W * H * H.transpose()
		W = np.matrix([[genW(row, col, W, VHt, WHHt) for col in range(r)] for row in range(n)])

		WtV = W.transpose() * V
		WtWH = W.transpose() * W * H
		H = np.matrix([[genH(row, col, H, WtV, WtWH) for col in range(m)] for row in range(r)])

		d = dist(V, W * H)
		if d <= tolerance:
			break
		obj.append(d)
	
	return W, H, obj

def dist(V, U):
	assert(V.shape == U.shape)
	return np.linalg.norm(V - U)

dirname = "samples"
min_df = 5
num_samples = 1000
num_topics = 20
num_top_words = 20
filenames = sorted([os.path.join(dirname, fn) for fn in os.listdir(dirname)])[:num_samples]

vectorizer = text.CountVectorizer(input='filename', stop_words='english', decode_error='ignore', min_df=min_df)
dtm = vectorizer.fit_transform(filenames).toarray()
print dtm.shape
vocab = np.array(vectorizer.get_feature_names())

W, H, obj = NMF(dtm, num_topics)
H = np.array(H)
topic_words = []
for topic in H:
	word_idx = np.argsort(topic)[::-1][0:num_top_words]
	topic_words.append([vocab[i] for i in word_idx])
for t in range(len(topic_words)):
	print("Topic {}: {}".format(t + 1, ' '.join(topic_words[t][:15])))

def genCvgPlot(obj):	
	plt.style.use('bmh')
	plt.figure(1)
	plt.title('NMF Convergence')
	plt.xlabel('Iteration')
	plt.ylabel('RMSE')
	plt.plot(obj, 'r')	
	plt.show()

genCvgPlot(obj)
