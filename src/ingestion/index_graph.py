from langgraph.graph import StateGraph
from typing import TypedDict
from .extractor import extract_text_blocks, extract_tables,ocr_pdf
from .table_agent import table_to_text, clean_and_structure_text
from .chunker import chunk_text
from vector_store import add_documents

class IndexState(TypedDict):
    pdf_path: str
    text: str
    tables: list
    processed_tables: list
    chunks: list


# def extract_node(state):
#     # state["text"] = extract_text_blocks(state["pdf_path"])
#     # state["tables"] = extract_tables(state["pdf_path"])
#     print("Current state:extraction", state)
#     return state

def extract_node(state):
    from extractor import extract_structured_text

    structured_text = extract_structured_text(state["pdf_path"])
    state["text"] = structured_text
    return state


def extract_and_clean_node(state):

    raw_text = ocr_pdf(state["pdf_path"])

    # Split by pages (rough split)
    pages = raw_text.split("\n\n")

    cleaned_pages = []

    for page_text in pages:
        print("PAGE TEXT----------------------------------")
        print(page_text)
        cleaned = clean_and_structure_text(page_text)
        print("CLEANED PAGE TEXT----------------------------------")
        print(cleaned)
        cleaned_pages.append(cleaned)

    state["text"] = "\n".join(cleaned_pages)
    print("Current state:extraction & cleaning", state)
    return state

def process_tables_node(state):
    processed = []
    for table in state["tables"]:
        processed.append(table_to_text(table))
    state["processed_tables"] = processed
    print("Current state process tables:", state)
    return state


# def chunk_node(state):
#     combined_text = state["text"]
#     state["chunks"] = chunk_text(combined_text)
#     print("Current state chunking:", state)
#     return state

def chunk_node(state):
    state["chunks"] = chunk_text(state["text"])
    return state


def store_node(state):
    add_documents(state["chunks"])
    print("Current state adding docs:", state)
    return state


builder = StateGraph(IndexState)

builder.add_node("extract", extract_and_clean_node)
# builder.add_node("process_tables", process_tables_node)
builder.add_node("chunk", chunk_node)
builder.add_node("store", store_node)

builder.set_entry_point("extract")
# builder.add_edge("extract", "process_tables")
builder.add_edge("extract", "chunk")
builder.add_edge("chunk", "store")

index_graph = builder.compile()