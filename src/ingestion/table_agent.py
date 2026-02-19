import ollama
from config import LLM_MODEL

def table_to_text(table):
    prompt=f""" Convert the following table into structured, clear natural language sentences. preserve all numerical values and years.
    Table:
    {table}
    Output:
    """
    response = ollama.chat(
        model =LLM_MODEL,
        messages=[{"role":"user","content":prompt}]
    )

    return response["message"]["content"]

def clean_and_structure_text(raw_text):

    prompt = f"""
The following text was extracted using OCR from a corporate ESG report.
It may contain broken formatting and table fragments.

Reconstruct:
- Proper paragraphs
- Structured data sentences
- Preserve all numbers, years, and units

Make it clean and semantically meaningful.

Text:
{raw_text}

Cleaned Output:
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    # print(response)

    return response["message"]["content"]
