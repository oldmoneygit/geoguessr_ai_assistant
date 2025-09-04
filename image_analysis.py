import cv2
from PIL import Image
import pytesseract
from ultralytics import YOLO
import torch
from torchvision import transforms
from transformers import AutoImageProcessor, AutoModel

def load_image(image_path):
    """Carrega uma imagem do caminho especificado."""
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Erro: Não foi possível carregar a imagem em {image_path}")
            return None
        print(f"Imagem {image_path} carregada com sucesso.")
        return img
    except Exception as e:
        print(f"Ocorreu um erro ao carregar a imagem: {e}")
        return None

def extract_text_from_image(image_path):
    """Extrai texto de uma imagem usando OCR."""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        print(f"Texto extraído da imagem {image_path}:\n{text}")
        return text
    except Exception as e:
        print(f"Ocorreu um erro ao extrair texto da imagem: {e}")
        return None

def detect_objects(image_path):
    """Detecta objetos em uma imagem usando YOLOv8."""
    try:
        model = YOLO("yolov8n.pt")  # Carrega o modelo YOLOv8 pré-treinado
        results = model(image_path)  # Executa a inferência
        
        detections = []
        for r in results:
            for c in r.boxes.cls:
                detections.append(model.names[int(c)])
        print(f"Objetos detectados em {image_path}: {detections}")
        return detections
    except Exception as e:
        print(f"Ocorreu um erro ao detectar objetos na imagem: {e}")
        return None

def generate_visual_embedding(image_path):
    """Gera embedding visual de uma imagem usando DINOv2."""
    try:
        # Carrega o processador e o modelo DINOv2
        processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base") # Changed to dinov2-base
        model = AutoModel.from_pretrained("facebook/dinov2-base") # Changed to dinov2-base

        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        # O embedding é a saída do pooler ou a média dos tokens do último hidden state
        # Para DINOv2, o embedding global é geralmente o token CLS ou a média dos patches.
        # O modelo dinov2-base tem hidden_size de 768.
        # outputs.last_hidden_state tem shape (batch_size, num_patches + 1, hidden_size)
        # O primeiro token (índice 0) é o token CLS, que representa o embedding global da imagem.
        embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
        print(f"Embedding visual gerado para {image_path}. Tamanho: {embedding.shape}")
        return embedding
    except Exception as e:
        print(f"Ocorreu um erro ao gerar o embedding visual: {e}")
        return None

if __name__ == '__main__':
    # Exemplo de uso
    test_image = 'test_image.png'
    cv2.imwrite(test_image, cv2.cvtColor(
        cv2.putText(cv2.UMat(200, 400, cv2.CV_8UC3), 'Hello World! 123', 
                    (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2),
        cv2.COLOR_BGR2RGB))
    
    loaded_image = load_image(test_image)
    if loaded_image is not None:
        print("Função de carregamento de imagem funcionando corretamente.")
        extracted_text = extract_text_from_image(test_image)
        if extracted_text:
            print("Função OCR funcionando corretamente.")
        
        detected_objects = detect_objects(test_image)
        if detected_objects:
            print("Função de detecção de objetos funcionando corretamente.")

        visual_embedding = generate_visual_embedding(test_image)
        if visual_embedding is not None:
            print("Função de embedding visual funcionando corretamente.")


