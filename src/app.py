from ingestion.index_graph import index_graph
from retrieval.qa_graph import qa_graph

PDF_PATH = "src\data\AI Enginner Use Case Document.pdf"

print("Indexing document...")
index_graph.invoke({"pdf_path": PDF_PATH})
print("Indexing complete.")

while True:
    q = input("\nAsk a question (or 'exit'): ")
    if q.lower() == "exit":
        break

    result = qa_graph.invoke({"question": q})
    print("\nAnswer:\n", result["answer"])