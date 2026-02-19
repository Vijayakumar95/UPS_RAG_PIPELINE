from langgraph.graph import StateGraph
from typing import TypedDict
import ollama
from vector_store import query_documents
from config import LLM_MODEL

class QAState(TypedDict):
    question: str
    context: list
    answer: str


def retrieve_node(state):
    docs = query_documents(state["question"])
    state["context"] = docs
    return state


def answer_node(state):

    context_text = "\n\n".join(state["context"])

    prompt = f"""
Answer ONLY using the provided context.
If not available say: Information not found in report.

Context:
{context_text}

Question:
{state["question"]}

Answer:
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    state["answer"] = response["message"]["content"]
    return state


builder = StateGraph(QAState)

builder.add_node("retrieve", retrieve_node)
builder.add_node("answer", answer_node)

builder.set_entry_point("retrieve")
builder.add_edge("retrieve", "answer")

qa_graph = builder.compile()