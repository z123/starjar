from app import app

@app.template_filter()
def dashify(text):
    """Convert spaces to dashes."""
    return text.replace(' ', '-').lower()
