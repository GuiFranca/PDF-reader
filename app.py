import streamlit as st
from pdf2image import convert_from_bytes
import cv2
import numpy as np
from google.cloud import vision
import pytesseract
import os

# Configuração inicial
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
    '/Users/guilh/OneDrive/Desenvolvimento/CREDENTIALS/GOOGLE CLOUD VISION/powerful-link-184817-43039c887712.json'


# Função para OCR usando Google Cloud Vision
def google_cloud_vision_ocr(image):
    client = vision.ImageAnnotatorClient()
    success, encoded_image = cv2.imencode('.png', image)
    content = encoded_image.tobytes()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f'{response.error.message}')

    return texts[0].description if texts else ""


# Função para OCR usando Tesseract
def tesseract_ocr(image):
    return pytesseract.image_to_string(image, lang='por')


st.title("OCR com Tesseract e Google Cloud Vision")

# Upload do arquivo PDF
uploaded_file = st.file_uploader("Envie o arquivo PDF", type="pdf")

if uploaded_file:
    # Converte o PDF em imagens
    pages = convert_from_bytes(uploaded_file.read(), dpi=300)
    all_text_tesseract = ""
    all_text_google = ""

    # Escolha do método de OCR
    ocr_option = st.selectbox("Escolha o método de OCR", ["Tesseract", "Google Cloud Vision"])

    for page_num, page in enumerate(pages):
        page_data = np.array(page)
        page_data = cv2.cvtColor(page_data, cv2.COLOR_RGB2BGR)

        if ocr_option == "Tesseract":
            # Extração de texto com Tesseract
            ocr_text = tesseract_ocr(page_data)
            all_text_tesseract += f"\n\nPágina {page_num + 1}:\n{ocr_text}"
        else:
            # Extração de texto com Google Cloud Vision
            ocr_text = google_cloud_vision_ocr(page_data)
            all_text_google += f"\n\nPágina {page_num + 1}:\n{ocr_text}"

        # Exibir imagem pós-processada
        st.image(page_data, caption=f'Página {page_num + 1}', use_column_width=True)

    # Exibir o texto extraído pelo métod escolhido
    if ocr_option == "Tesseract":
        st.text_area("Texto extraído pelo Tesseract:", all_text_tesseract, height=300)
        # Opção para baixar o texto extraído pelo Tesseract
        st.download_button("Baixar o texto extraído (Tesseract)", all_text_tesseract,
                           file_name="texto_extraido_tesseract.txt")
    else:
        st.text_area("Texto extraído pelo Google Cloud Vision:", all_text_google, height=300)
        # Opção para baixar o texto extraído pelo Google Cloud Vision
        st.download_button("Baixar o texto extraído (Google Cloud Vision)", all_text_google,
                           file_name="texto_extraido_google_vision.txt")
