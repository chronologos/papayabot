from flask import Flask, request, jsonify
import os
import logging
import chromadb
import time
import ml


from flask_cors import CORS, cross_origin

import getpass
import os

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    db_id = request.form['db_id']
    chroma_client = chromadb.PersistentClient(path=f"dbs/{db_id}")
    collection = chroma_client.get_or_create_collection(name="my_collection")

    if 'uploaded_file' in request.files:
        uploaded_file = request.files['uploaded_file']
        contents = str(uploaded_file.read())

        vector_store = ml.create_vector_store(contents)
        collection.add(
            documents=[contents],
            metadatas=[{"source": "upload", "uploaded_time": time.time()}],
            # find better ID. reusing ID results in no upload.
            ids=[str(time.time())]
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
@cross_origin()
def ask_question():
    # file_path = request.form['file_path']
    # contents = load_pdf(file_path)

    # vector_store = create_vector_store(contents)
    # # need to load vector store
    # retriever = vector_store.as_retriever()
    # prompt = hub.pull("rlm/rag-prompt")
    # llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # rag_chain = (
    # {"context": retriever | format_docs, "question": RunnablePassthrough()}
    # | prompt
    # | llm
    # | StrOutputParser()
    # )
    # question_text = request.form['question_text']
    # return rag_chain.invoke(question_text)
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

    # chroma_client = chromadb.PersistentClient(path=f"dbs/123")
    # chroma_client.delete_collection(name="my_collection").count()
    # logging.info(str(chroma_client.list_collections()),
    #  chroma_client.get_collection(name="my_collection").count())

    app.run(debug=True, port=port)
