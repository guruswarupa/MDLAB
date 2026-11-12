import time
from pathlib import Path
import faiss
import numpy as np

N = 2000 
DIM = 32 
N_QUERIES = 100
K = 5 
NLIST = 32 
NPROBE = 4 
M = 16 
EF_CONSTRUCTION = 40 
EF_SEARCH = 32 

faiss.omp_set_num_threads (1)
rng = np.random.default_rng(42)
vectors = rng.random((N, DIM), dtype=np.float32)
queries = rng.random((N_QUERIES, DIM), dtype=np.float32)

def make_index(kind):
    if kind == "Flat":
        return faiss.IndexFlatL2(DIM)
    if kind == "IVF":
        quantizer = faiss.IndexFlatL2(DIM)
        index = faiss.IndexIVFFlat(quantizer, DIM, NLIST)
        index.nprobe = NPROBE
        return index
    index = faiss.IndexHNSWFlat(DIM, M)
    index.hnsw.efConstruction = EF_CONSTRUCTION
    index.hnsw.efSearch = EF_SEARCH
    return index

results = []
flat_ids = None

for kind in ("Flat", "IVF", "HNSW"):
    index = make_index(kind)
    start = time.perf_counter()
    if not index.is_trained:
        index.train(vectors)
    index.add(vectors)
    build_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    distances, ids = index.search(queries, K)
    search_ms = (time.perf_counter() - start) * 1000
    if kind == "Flat":
        flat_ids = ids.copy()
    recall = sum(
        len(set(ids[i]) & set(flat_ids[i]))
        for i in range(N_QUERIES)
    ) / (N_QUERIES * K)
    filename = Path(kind.lower() + ".index")
    faiss.write_index(index, str(filename))
    loaded = faiss.read_index(str(filename))
    if kind == "IVF":
        loaded.nprobe = NPROBE
    if kind == "HNSW":
        loaded.hnsw.efSearch = EF_SEARCH
    _, loaded_ids = loaded.search(queries[:1], K)
    size_kb = filename.stat().st_size / 1024
    results.append((kind, build_ms, search_ms, size_kb,
        recall, loaded.ntotal, loaded_ids[0]))

print("Index | Build ms | Search ms | File KB | Recall | Loaded")
for name, build, search, size, recall, count, ids in results:
    print(f"{name:5} | {build:8.2f} | {search:9.2f} | "
        f"{size:7.1f} | {recall:6.2%} | {count}")
    print(" First query IDs after load:", ids)