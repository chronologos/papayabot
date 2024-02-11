# Papayabot

One-time Setup:
```sh
python3 -m venv papayabot  # create virtualenv
pip install -r requirements.txt  # install dependencies
```
Test commands:

1. start the server: `python main.py`
1. send a request: `curl -X POST -F "db_id=123" -F "uploaded_file=@test.txt" http://localhost:8080/upload`