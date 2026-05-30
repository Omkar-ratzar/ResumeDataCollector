from paddleocr import PaddleOCR
import fitz
import numpy as np
from PIL import Image
import io

ocr = PaddleOCR(
    use_textline_orientation=True,
    lang='en',
    device='gpu'

)

def ocr_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = []

    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        arr = np.array(img)

        result = ocr.predict(arr)

        print(result)  # debug once

        for res in result:
            rec_texts = res.get("rec_texts", [])
            all_text.extend(rec_texts)

    return "\n".join(all_text)

print(ocr_pdf("ocr_test_input.pdf"))
