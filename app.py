from google.cloud import vision
import io
import streamlit as st
from pdf2image import convert_from_bytes
import os
import numpy as np  # Adicionando a importação do numpy
import cv2

# Configuração inicial
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
    '/Users/guilh/OneDrive/Desenvolvimento/CREDENTIALS/GOOGLE CLOUD VISION/powerful-link-184817-43039c887712.json'


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


st.title("OCR com Google Cloud Vision")
uploaded_file = st.file_uploader("Envie o arquivo PDF", type="pdf")

if uploaded_file:
    pages = convert_from_bytes(uploaded_file.read(), dpi=300)
    all_text = ""

    for page_num, page in enumerate(pages):
        page_data = np.array(page)
        page_data = cv2.cvtColor(page_data, cv2.COLOR_RGB2BGR)

        # Extração com Google Cloud Vision OCR
        ocr_text = google_cloud_vision_ocr(page_data)
        all_text += f"\n\nPágina {page_num + 1}:\n{ocr_text}"

        # Exibir imagem pós-processada e download da imagem
        st.image(page_data, caption=f'Página {page_num + 1}', use_column_width=True)

    # Exibir o texto completo extraído
    st.text_area("Texto extraído:", all_text, height=300)

    # Opção para baixar o texto extraído
    st.download_button("Baixar o texto extraído", all_text, file_name="texto_extraido.txt")
