import os
from deepface import DeepFace
import numpy as np
from tqdm.auto import tqdm
import faiss
from config import IMAGES_FOLDER, INDEX_PATH, EMBEDDINGS_PATH

MODEL_NAME = "Facenet"
DETECTOR_BACKEND = "retinaface"

image_paths = [
    f for f in os.listdir(IMAGES_FOLDER) if f.lower().endswith(("jpg", "jpeg", "png"))
]
image_paths.sort(key=lambda x: int(x.split(".")[0]))
image_paths = [f"{IMAGES_FOLDER}/{f}" for f in image_paths]

print("\n" * 100)

embeddings = []
error_exists = False

for img_path in tqdm(image_paths, desc="Generating embeddings", total=len(image_paths)):
    try:
        emb = DeepFace.represent(
            img_path=img_path,
            enforce_detection=True,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
        )
        embeddings.append(emb[0]["embedding"])
    except Exception:
        print(f"{img_path} was not processed because face wasn't detected, replace the image while maintaining the file name")
        print("Ensure that all the images are clear and proper")
        error_exists = True
        break

if not error_exists:
    embeddings_np = np.array(embeddings, dtype=np.float32)
    DIMENSIONS = embeddings_np.shape[1]
    index = faiss.IndexHNSWFlat(DIMENSIONS, 32)
    index.add(embeddings_np)
    faiss.write_index(index, INDEX_PATH)
    np.save(EMBEDDINGS_PATH, embeddings_np)