from pypdf import PdfReader
from datetime import datetime

def parse_pdf_date(pdf_date):
    if not pdf_date:
        return None

    pdf_date = str(pdf_date)

    if pdf_date.startswith("D:"):
        pdf_date = pdf_date[2:]

    try:
        return datetime.strptime(pdf_date[:14], "%Y%m%d%H%M%S").isoformat()
    except ValueError:
        return pdf_date


KNOWN_KEYS = {
    "/Title": "title",
    "/Author": "author",
    "/Subject": "subject",
    "/Creator": "creator",
    "/Producer": "producer",
    "/CreationDate": "creation_date",
    "/ModDate": "modification_date",
    "/Keywords": "keywords",
    "/Trapped": "trapped"
}

def extract_pdf_metadata(path):
    reader = PdfReader(path)
    metadata = reader.metadata or {}

    result = {v: None for v in KNOWN_KEYS.values()}
    extra = {}

    for key, value in metadata.items():
        if key in KNOWN_KEYS:
            if key == "/CreationDate":
                result["creation_date"] = parse_pdf_date(value)
            elif key == "/ModDate":
                result["modification_date"] = parse_pdf_date(value)
            else:
                result[KNOWN_KEYS[key]] = str(value) if value else None
        else:
            extra[key] = str(value) if value else None

    result["extra_metadata"] = extra
    return result
