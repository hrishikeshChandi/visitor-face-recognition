# Visitor Face Recognition System

## Overview

This is a face recognition system designed to identify visitors and fetch their records from a database. It uses pre-trained deep learning models (RetinaFace for detection and Facenet for embeddings) alongside FAISS for efficient similarity search.

> **Important Note:** The system assumes a specific database structure and image naming convention by default. The default setup expects images to be numbered sequentially (1.jpg, 2.jpg, etc.) and matches them to database records using the filename as a key. These can be modified for your use case, but corresponding changes must be made in the code (primarily in `files_handler.py`, `face_matching.py`, and `database.py`).

> **Critical Dependency:** The application **requires** the `embeddings.npy` and `index.faiss` files to function. You must generate them using the `generate_embeddings.py` script before running the main application.

## Features

- **Face Detection & Embedding Generation:** Utilizes RetinaFace for face detection and a pre-trained Facenet model to generate facial embeddings. Runs on CPU, but GPU is recommended for significantly faster performance.
- **Scalable Search:** Implements FAISS HNSW index for fast and efficient similarity searches, capable of handling large datasets (tested with simulated data up to 1M embeddings using NumPy).
- **Incremental Updates:** After initial setup, new visitor images can be uploaded through the app, and their embeddings are added to the existing FAISS index dynamically.
- **Database Integration:** Fetches visitor records from a MySQL database. The database table must include at least the following columns:
  - `VISITORNAME`
  - `DEPARTMENT`
  - `EMPLOYEEID`
  - `REQUISITIONNO`
- **Interactive Web Interface:** Built with Streamlit for easy image uploads and result display.
- **Performance Logging:** Key operations log approximate execution times for embedding generation, verification, and search.

## Project Structure

```
visitor-face-recognition/
├── main.py                 # Streamlit application
├── generate_embeddings.py  # Initial embeddings generation
├── config.py               # Configuration loader
├── database.py             # Database connection and queries
├── face_matching.py        # Face recognition logic
├── files_handler.py        # File processing utilities
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── dataset/                # Directory for known visitor images
└── uploads/                # Directory for temporary uploads
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- MySQL Server

### 2. Clone and Install

```bash
git clone https://github.com/hrishikeshChandi/visitor-face-recognition.git
cd visitor-face-recognition
pip install -r requirements.txt
```

### 3. Environment Configuration

The project includes a `.env` file in the root directory. You must edit this file and fill in your specific configuration values. Here's a complete example:

```ini
# Database Configuration
HOST=localhost
USERNAME=root
PASSWORD=your_secure_mysql_password_here
DATABASE_NAME=visitors_db

# File Path Configuration
IMAGES_FOLDER=./dataset
UPLOADS_FOLDER=./uploads
INDEX_PATH=./index.faiss
EMBEDDINGS_PATH=./embeddings.npy
```

### 4. Database Setup

1.  Create a MySQL database (matching the name you specified in the `.env` file)
2.  Create a `visitors` table with the required columns. Example SQL:

```sql
CREATE TABLE visitors (
    REQUISITIONNO PRIMARY KEY VARCHAR(100),
    VISITORNAME VARCHAR(255) NOT NULL,
    DEPARTMENT VARCHAR(255),
    EMPLOYEEID VARCHAR(100),
);
```

### 5. Initial Setup with Images

1.  Place your initial visitor images in the `./dataset` folder
2.  **⚠️ Crucial:** Ensure your image filenames match the corresponding REQUISITIONNO values in your database (e.g., if a record has REQUISITIONNO="1001", the image should be named "1001.jpg")
3.  Generate the initial embeddings and FAISS index:
    ```bash
    python generate_embeddings.py
    ```
    This will create the essential `embeddings.npy` and `index.faiss` files

### 6. Run the Application

After completing the above steps, start the application:

```bash
streamlit run main.py
```

## Usage

1.  Open the provided URL in your browser after starting the application
2.  Use the interface to upload new visitor images for recognition
3.  The system will display recognition results and fetch visitor records from the database
4.  **Upload New Images**: Use the sidebar to upload new visitor images (batch processing)
5.  **Identify Visitors**: Upload a single image in the main area to identify a visitor
6.  **View Results**: The system will display visitor records from the database

## Key Components

1. `config.py`: Loads environment variables and provides configuration to all modules
2. `database.py`: Manages MySQL database connections and queries
3. `face_matching.py`: Handles face detection, embedding generation, and similarity search
4. `files_handler.py`: Processes uploaded files and updates the FAISS index incrementally
5. `generate_embeddings.py`: Initial script to create facial embeddings from the image dataset
6. `main.py` - The main Streamlit application that provides the web interface for uploading images, performing recognition, and displaying visitor records from the database.

## Limitations

- **Initial Setup Requirement:** You must start with images in the dataset folder and run `generate_embeddings.py` before the app will function
- **Concurrency:** The current implementation is not designed for high concurrency. Multiple users can interact with the Streamlit app simultaneously, but performance may degrade significantly under load, and there is a potential for race conditions when updating the shared FAISS index and embeddings files.
- **Performance:** The first query will be slower as models are loaded into memory. CPU-only inference will be significantly slower than GPU
- **File Naming Dependency**: The system relies on specific file naming conventions to map images to database records

## Troubleshooting

- If you encounter connection errors, verify your MySQL server is running and the credentials in `.env` are correct
- If face recognition fails, ensure images are clear and contain front-facing faces
- If the app can't find embeddings, run `generate_embeddings.py` again

## Notes

- The file naming convention is critical for correctly mapping embeddings to database records
- The required database columns are a minimum. You can add more columns by updating the SQL query in `database.py` and the display logic in `main.py`
- After the initial setup, new uploads through the app will be processed incrementally

---

### Customization

1. To adapt this system for your specific use case:
2. Modify database schema in database.py (update queries)
3. Adjust file naming convention in files_handler.py and face_matching.py
4. Change recognition thresholds in face_matching.py if needed
5. Update UI elements in main.py to match your requirements

---

### License

This project is provided under the MIT License.

---
