import numpy as np
import faiss
import pickle
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
import cv2

# Load precomputed index and paths
INDEX_PATH = "models/cbir_index.faiss"
PATHS_PATH = "models/paths.pkl"

index = faiss.read_index(INDEX_PATH)
image_paths = pickle.load(open(PATHS_PATH, 'rb'))

# Build model
base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)

def extract_features(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x, verbose=0)
    features = features / np.linalg.norm(features)
    return features.astype('float32')

def get_similar_images(query_path, top_k=6):
    query_vector = extract_features(query_path)
    distances, indices = index.search(query_vector.reshape(1, -1), top_k)
    results = [image_paths[i] for i in indices[0]]
    return results
