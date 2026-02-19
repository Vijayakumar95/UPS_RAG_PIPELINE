import pdfplumber
import fitz
from pdf2image import convert_from_path
import pytesseract 
from pytesseract import Output
from collections import defaultdict
from PIL import Image
import os

# pdf_path = "src\data\AI Enginner Use Case Document_1_7.pdf"


def extract_text_blocks(pdf_path):
    text_blocks =[]
    doc = fitz.open(pdf_path)
    print(len(doc))
    for page in doc:
        blocks = page.get_text()
        print(blocks)
        for b in blocks:
            text_blocks.append(b[4])
    return "\n".join(text_blocks)

def extract_tables(pdf_path):
    tables=[]
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            print(len(page_tables))
            for table in page_tables:
                print(table)
                tables.append(table)
    return tables

# extract_text_blocks(pdf_path)
# extract_tables(pdf_path)


# Set path if not in PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\MJ665GV\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\Users\MJ665GV\poppler\poppler-25.12.0\Library\bin"

# C:\Users\MJ665GV\AppData\Local\Programs\Tesseract-OCR


def ocr_pdf(pdf_path):
    pages = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=POPPLER_PATH
    )

    full_text = ""

    for i, page in enumerate(pages):
        print(f"OCR processing page {i+1}/{len(pages)}")

        text = pytesseract.image_to_string(
            page,
            config="--psm 6"
        )

        full_text += text + "\n"
    # print(full_text)
    return full_text

# text = ocr_pdf(pdf_path)
# print(text)


# -------------------------------
# 1️⃣ Convert PDF → Images
# -------------------------------
def pdf_to_images(pdf_path, dpi=300):
    return convert_from_path(
        pdf_path,
        dpi=dpi,
        poppler_path=POPPLER_PATH
    )

# -------------------------------
# 2️⃣ Extract word-level data
# -------------------------------
def extract_page_words(image):

    data = pytesseract.image_to_data(
        image,
        config="--oem 3 --psm 4",
        output_type=Output.DICT
    )

    words = []

    for i in range(len(data["text"])):
        word = data["text"][i].strip()
        if word != "":
            words.append({
                "text": word,
                "left": data["left"][i],
                "top": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i],
                "conf": int(data["conf"][i])
            })

    return words


# -------------------------------
# 3️⃣ Group words into rows
# -------------------------------
def group_words_by_rows(words, y_threshold=10):

    rows = defaultdict(list)

    for word in words:
        y_key = round(word["top"] / y_threshold)
        rows[y_key].append(word)

    structured_rows = []

    for _, row_words in sorted(rows.items()):
        sorted_row = sorted(row_words, key=lambda x: x["left"])
        structured_rows.append(sorted_row)

    return structured_rows


# -------------------------------
# 4️⃣ Convert rows → structured text
# -------------------------------
def rows_to_text(rows):

    text_blocks = []

    for row in rows:
        line = " ".join([w["text"] for w in row])
        text_blocks.append(line)

    return "\n".join(text_blocks)


# -------------------------------
# 5️⃣ Detect table-like rows
# -------------------------------
def detect_table_blocks(rows):

    table_blocks = []
    text_blocks = []

    for row in rows:
        words = [w["text"] for w in row]

        numeric_count = sum(any(char.isdigit() for char in w) for w in words)

        # Heuristic: numeric-heavy rows likely tables
        if numeric_count >= 2:
            table_blocks.append(words)
        else:
            text_blocks.append(" ".join(words))

    return table_blocks, text_blocks


# -------------------------------
# 6️⃣ Convert table rows → sentences (deterministic)
# -------------------------------
def table_rows_to_sentences(table_rows):

    sentences = []

    for row in table_rows:
        if len(row) >= 2:
            metric = row[0]
            values = ", ".join(row[1:])
            sentence = f"{metric} has reported values: {values}."
            sentences.append(sentence)

    return sentences


# -------------------------------
# 7️⃣ Full Extraction Pipeline
# -------------------------------
def extract_structured_text(pdf_path):

    images = pdf_to_images(pdf_path)

    full_text = []

    for page_number, image in enumerate(images):
        print(f"Processing page {page_number + 1}/{len(images)}")

        words = extract_page_words(image)
        rows = group_words_by_rows(words)

        table_rows, text_rows = detect_table_blocks(rows)

        # Convert tables deterministically
        table_sentences = table_rows_to_sentences(table_rows)

        page_text = "\n".join(text_rows + table_sentences)

        full_text.append(page_text)

    return "\n\n".join(full_text)