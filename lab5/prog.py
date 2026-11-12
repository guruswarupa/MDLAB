import chromadb

print("Program started")
client = chromadb.Client()
print("Client created")
collection = client.create_collection(name="student_collection")
print("Collection created successfully")

print("\n--- Adding Data ---")
collection.add(
    ids=["1", "2", "3", "4"],
    documents=[
        "Python is a programming language",
        "Java is an object oriented language",
        "SQL is used to manage databases",
        "Machine Learning is a branch of Artificial Intelligence"
    ]
)
print("Data added successfully")

print("\n--- Displaying Data ---")
data = collection.get()
print(data)

print("\n--- Querying Collection ---")
result = collection.query(
    query_texts=["programming language"],
    n_results=2
)
print(result)

print("\n--- Deleting Data ---")
collection.delete(ids=["2"])
print("Data with ID 2 deleted successfully")

print("\n--- Data After Deletion ---")
data = collection.get()
print(data)