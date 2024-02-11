from flask import Flask, request, jsonify
import os
import logging
import chromadb
import ml
import tempfile

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    db_id = request.form['db_id']

    if 'uploaded_file' in request.files:
        uploaded_file = request.files['uploaded_file']
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(uploaded_file.read())
            ml.create_or_get_vector_store(
                collection_name=db_id, file_path=temp_file.name)
        return jsonify({"message": "File uploaded successfully", "db_id": db_id, "filename": uploaded_file.filename})
    else:
        return jsonify({"error": "No file part"}), 400


@app.route('/askqn', methods=['POST'])
@cross_origin()
def ask_question():
    db_id = request.form['db_id']
    question_text = request.form['question_text']
    logging.info(f"Received question: {question_text} for DB ID: {db_id}")

    chroma_client = chromadb.PersistentClient(path="dbs")
    logging.info(f"{chroma_client.list_collections()}")
    results = ml.handle_question(
        collection_name=db_id, question_text=question_text)

    return jsonify(results)


@app.route('/simplequery', methods=['POST'])
@cross_origin()
def simple_query():
    db_id = request.form['db_id']
    question_text = request.form['question_text']
    logging.info(f"Received question: {question_text} for DB ID: {db_id}")

    chroma_client = chromadb.PersistentClient(path="dbs")
    logging.info(f"{chroma_client.list_collections()}")
    logging.info(
        f"#embeddings in db: {chroma_client.get_collection(db_id).count()}")
    results = ml.simple_query(
        chroma_client=chroma_client, collection_name=db_id, query=question_text)
    return jsonify(results)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Determine port number through environment variable, or use 8080 by default
    port = int(os.environ.get('PORT', 8080))
    logging.info(f"running with OpenAI API Key: {ml.get_openai_api_key()}")
    app.run(debug=True, port=port)
