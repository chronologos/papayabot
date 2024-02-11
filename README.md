# Papayabot

One-time Setup:
```sh
python3 -m venv papayabot  # create virtualenv
pip install -r requirements.txt  # install dependencies

cd frontend
npm install
```
Test commands:

1. start the backend: `python main.py`
2. run the frontend: `cd frontend && npm run dev`
3. send an upload request: `curl -X POST -F "db_id=123" -F "uploaded_file=@test.txt" http://localhost:8080/upload`
4. send a question request: `curl -X POST -F "db_id=123" -F "question_text=another document" http://localhost:8080/askqn`

curl -X POST -F "db_id=123" -F "uploaded_file=@test.txt" "question_text=hello that are some texts" http://localhost:8080/askqn