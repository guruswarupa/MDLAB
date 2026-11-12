import time 
import faiss
import numpy as np 
from sklearn.feature_extraction.text import HashingVectorizer

documents = [
'FAISS performs similarity search on vectors.',
'Flat index checks all vectors for exact search.',
'IVF divides vectors into clusters for searching.',
'HNSW uses a graph for fast similarity search.',
'Python is used to develop software applications.',
'Databases store and retrieve information.',
'Machine learning learns patterns from data.',
'An index can be saved and loaded from a file.'
]

query = ['graph similarity search'] 
DIM, K = 512, 3

vectorizer = HashingVectorizer(
n_features=DIM, alternate_sign=False, norm='l2'
)

x = vectorizer.transform(documents).toarray().astype('float32')
q = vectorizer.transform(query).toarray().astype('float32')
faiss.omp_set_num_threads(1) 

flat = faiss.IndexFlatL2(DIM)

ivf = faiss.IndexIVFFlat(faiss.IndexFlatL2(DIM), DIM, 2)
ivf.cp.min_points_per_centroid = 1
ivf.nprobe = 1

hnsw = faiss.IndexHNSWFlat(DIM, 16)
hnsw.hnsw.efConstruction = 40 
hnsw.hnsw.efSearch = 32 
indexes = {'Flat': flat, 'IVF': ivf, 'HNSW': hnsw}
print('Index Build(ms) Search(ms)')

for name, index in indexes.items():
    start = time.perf_counter()
    if not index.is_trained:
        index.train(x) 
    index.add(x) 
    build_ms = (time.perf_counter() - start) * 1000

    faiss.write_index(index, name + '.index')
    index = faiss.read_index(name + '.index')
    index.search(q, K) 
    start = time.perf_counter()

    for _ in range(100):
        distances, ids = index.search(q, K)
    search_ms = (time.perf_counter() - start) * 1000 / 100

    print(f'{name:8} {build_ms:9.3f} {search_ms:12.3f}')
print('Matching paragraphs:')

for i in ids[0]:
    if i >= 0:
        print(' -', documents[i])