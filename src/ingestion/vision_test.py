from pdf2image import convert_from_path
import os

POPPLER_PATH = r"C:\Users\MJ665GV\poppler\poppler-25.12.0\Library\bin"

def convert_pages(pdf_path, start=0, end=2, output_dir="temp_pages"):
    os.makedirs(output_dir, exist_ok=True)

    pages = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=POPPLER_PATH
    )

    selected_pages = pages[start:end]

    image_paths = []

    for i, page in enumerate(selected_pages):
        path = os.path.join(output_dir, f"page_{start+i}.png")
        page.save(path, "PNG")
        image_paths.append(path)

    return image_paths


if __name__ == "__main__":
    paths = convert_pages("src\data\AI Enginner Use Case Document_p7.pdf", 0, 3)
    print(paths)