import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes

st.title('Extração de Texto de Matrículas PDF')

# Upload do arquivo PDF
uploaded_file = st.file_uploader("Envie um arquivo PDF", type="pdf")

# Se um arquivo foi enviado, comece o processamento
if uploaded_file is not None:
    st.write("Processando o arquivo...")

    # Converter PDF para uma lista de imagens
    pages = convert_from_bytes(uploaded_file.read(), dpi=300)
    texto_extraido = ""

    # Processar cada página com OCR
    for page_number, page_data in enumerate(pages):
        texto = pytesseract.image_to_string(page_data, lang='por')  # OCR com suporte ao português
        texto_extraido += f'\n--- Página {page_number + 1} ---\n'
        texto_extraido += texto

    # Exibir o texto extraído
    st.subheader("Texto Extraído")
    st.text_area("Texto do PDF", value=texto_extraido, height=300)

    # Botão para baixar o texto extraído
    st.download_button(
        label="Baixar texto extraído",
        data=texto_extraido,
        file_name="texto_extraido.txt",
        mime="text/plain"
    )
