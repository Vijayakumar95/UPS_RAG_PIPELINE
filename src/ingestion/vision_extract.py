import ollama
import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def extract_text_from_image(image_path):

    image_b64 = image_to_base64(image_path)

    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "user",
                "content": """
Extract ALL text exactly as written in the image.
Do not summarize.
Do not paraphrase.
Preserve numbers and formatting as much as possible.
                """,
                "images": [image_b64],
            }
        ],
    )

    return response["message"]["content"]


if __name__ == "__main__":
    result = extract_text_from_image("temp_pages/page_0.png")
    print(result)