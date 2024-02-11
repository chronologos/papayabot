from flask import Flask, request, jsonify
import os
import logging
import chromadb
import time

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    db_id = request.form['db_id']
    chroma_client = chromadb.PersistentClient(path=f"dbs/{db_id}")
    collection = chroma_client.get_or_create_collection(name="my_collection")

    if 'uploaded_file' in request.files:
        uploaded_file = request.files['uploaded_file']
        contents = str(uploaded_file.read())
        collection.add(
            documents=[contents],
            metadatas=[{"source": "upload", "uploaded_time": time.time()}],
            ids=["uploaded_file"]
        )

        # For demonstration, we'll just print the file name
        # In a real application, you might save the file to a directory
        logging.info(
            f"Received file: {uploaded_file.filename} for DB ID: {db_id}")
  
        logging.info(f"file contents: {contents}")
        return jsonify({"message": "File uploaded successfully", "db_id": db_id, "filename": uploaded_file.filename})
    else:
        return jsonify({"error": "No file part"}), 400


@app.route('/askqn', methods=['POST'])
def ask_question():
    db_id = request.form['db_id']
    chroma_client = chromadb.PersistentClient(path=f"dbs/{db_id}")

    question_text = request.form['question_text']

    logging.info(f"Received question: {question_text} for DB ID: {db_id}")
    collection = chroma_client.get_collection(name="my_collection")
    results = collection.query(
        query_texts=[question_text],
        n_results=2
    )
    return jsonify({"message": "Question received", "db_id": db_id, "question": question_text, "results": results})


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Determine port number through environment variable, or use 8080 by default
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, port=port)
