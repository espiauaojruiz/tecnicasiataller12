from PyPDF2 import PdfReader

class Document:
  # Funcion que permite leer un ODF y devolver el texto contenido
  def read_pdf(pdf):
    text = ""
    if pdf is not None:
      reader = PdfReader(pdf)
      for page in reader.pages:
        text += page.extract_text()
    return text

  # Funcion que permite unir lochunks recuperados de un PDF
  def format_docs(chunks):
    return " ".join(doc for doc in chunks)
