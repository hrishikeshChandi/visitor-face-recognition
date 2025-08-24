import os
from config import IMAGES_FOLDER, INDEX_PATH, EMBEDDINGS_PATH
import numpy as np
from deepface import DeepFace
import faiss


def process_uploaded_files(
    uploaded_files,
    mode_name="Facenet",
    detector_backend="retinaface",
):
    if not uploaded_files:
        return

    embeddings_np = np.load(EMBEDDINGS_PATH)
    embeddings = embeddings_np.tolist()
    index = faiss.read_index(INDEX_PATH)

    new_embeddings = []
    new_image_paths = []

    images_files = [
        f
        for f in os.listdir(IMAGES_FOLDER)
        if f.lower().endswith(("jpg", "jpeg", "png"))
    ]
    images_files.sort(key=lambda x: int(x.split(".")[0]))
    file_number = len(images_files) + 1

    saved_images = {}

    for file in uploaded_files:
        extension = file.name.split(".")[-1].lower()
        path = f"{IMAGES_FOLDER}/{file_number}.{extension}"
        with open(path, "wb") as f:
            f.write(file.read())
        saved_images[f"{file_number}.{extension}"] = file.name

        try:
            emb = DeepFace.represent(
                img_path=path,
                model_name=mode_name,
                detector_backend=detector_backend,
                enforce_detection=True,
            )
            vec = emb[0]["embedding"]
            embeddings.append(vec)
            new_embeddings.append(vec)
            new_image_paths.append(path)
            file_number += 1

        except:
            if os.path.exists(path):
                os.remove(path)

            raise Exception(
                f"Face not found in the uploaded file: {file.name}. "
                "Processing stopped. No further files were added."
            )

    embeddings_np = np.array(embeddings, dtype=np.float32)
    np.save(EMBEDDINGS_PATH, embeddings_np)

    if new_embeddings:
        index.add(np.array(new_embeddings, dtype=np.float32))
        faiss.write_index(index, INDEX_PATH)