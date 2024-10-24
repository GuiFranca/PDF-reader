import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import cv2
import numpy as np
import tempfile


# Função de pré-processamento da imagem
def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)  # Converte para escala de cinza
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # Binariza a imagem
    return Image.fromarray(binary)


st.title("PDF OCR com Pré-processamento")

# Upload do PDF
uploaded_file = st.file_uploader("Envie um arquivo PDF", type="pdf")

if uploaded_file is not None:
    # Convertendo o PDF para imagens (uma por página)
    pages = convert_from_bytes(uploaded_file.read(), dpi=300)

    # Inicializa o texto transcrito
    all_text = ""

    # Processando página por página
    for i, page in enumerate(pages):
        st.write(f"Página {i + 1}")

        # Pré-processamento da imagem
        processed_image = preprocess_image(page)

        # Mostrando a imagem pré-processada
        st.image(processed_image, caption=f"Imagem pré-processada da Página {i + 1}")

        # Extraindo texto da imagem pré-processada
        page_text = pytesseract.image_to_string(processed_image, lang='por')

        # Adicionando o texto ao resultado final
        all_text += f"\n\n--- Página {i + 1} ---\n\n" + page_text

    # Mostrando o texto extraído
    st.text_area("Texto Extraído", all_text, height=300)

    # Opção para baixar o texto como arquivo .txt
    st.download_button(
        label="Baixar texto extraído",
        data=all_text,
        file_name="texto_extraido.pdf",
        mime="text/plain"
    )
