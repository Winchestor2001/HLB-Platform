import fitz


def calculate_reading_time(pdf_path, words_per_minute=100):
    doc = fitz.open(pdf_path)
    total_words = 0

    for page_number in range(doc.page_count):
        page = doc[page_number]
        total_words += len(page.get_text("text").split())

    total_reading_time_minutes = total_words / words_per_minute
    return total_reading_time_minutes
