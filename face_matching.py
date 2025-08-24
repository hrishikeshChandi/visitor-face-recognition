from deepface import DeepFace
from config import IMAGES_FOLDER, INDEX_PATH
import faiss
import numpy as np
import os
import time


def get_requisition_numbers(img_path, model_name="Facenet", detector_backend="retinaface"):
    image_paths = [f for f in os.listdir(IMAGES_FOLDER) if f.lower().endswith(("jpg", "jpeg", "png"))]
    image_paths.sort(key=lambda x: int(x.split(".")[0]))

    index = faiss.read_index(INDEX_PATH)

    start = time.time()
    embedding = DeepFace.represent(
        img_path=img_path,
        model_name=model_name,
        detector_backend=detector_backend,
        enforce_detection=True,
    )[0]["embedding"]
    print(f"Embeddings generation took: {time.time() - start:.2f} seconds")

    emb = np.array(embedding, dtype=np.float32).reshape(1, -1)

    start = time.time()
    distances, ids = index.search(emb, 1)
    print(f"Search took: {time.time() - start:.2f} seconds")

    matching_file = image_paths[ids[0][0]]
    requisition_number = os.path.splitext(matching_file)[0]

    start = time.time()
    verification = DeepFace.verify(
        img1_path=img_path,
        img2_path=os.path.join(IMAGES_FOLDER, matching_file),
        model_name=model_name,
        detector_backend=detector_backend,
        enforce_detection=True,
    )
    print(f"Verification took: {time.time() - start:.2f} seconds")

    return requisition_number if verification["verified"] else None