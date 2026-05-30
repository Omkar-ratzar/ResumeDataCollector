import fitz
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

doc = fitz.open("ocr_test_input.pdf")

all_text = []

for page_num in range(len(doc)):
    page = doc[page_num]

    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))

    text = pytesseract.image_to_string(img, lang="eng")
    all_text.append(text)

print(all_text)
# with open("ocr.txt", "w", encoding="utf-8") as f:
#     f.write("\n".join(all_text))


#not very accurate.. lets try smthn else
