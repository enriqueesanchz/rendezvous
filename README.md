# Simple HTTP rendezvous server for p2p apps
This REST API is used by p2p app's peers to meet each other.

## Requirements
```
pip install -r requirements.txt
```
- Python >= 3.8
- fastapi[all]
- pymongo[srv]
- python-dotenv
- Mongodb database

## How to run the server
```
python3 -m uvicorn main:app
```
REST API docs will be in http://127.0.0.1:8000/docs

## Methods
![REST API methods](https://github.com/enriqueesanchz/rendezvous/blob/main/methods.png?raw=true)

Mongodb will remove namespaces not modified in 10 minutes

## TODO:
- [ ] Unit tests
- [ ] Improve security
- [ ] Datetime
- [ ] Refactor mongodb db
- [ ] Refactor routes.py methods

## Disclaimer
This is a sample app for educational purposes, you can read my blog post: https://enriqueesanchz.github.io/posts/Nat-traversal/

This app is not for real use, it doesn't check some security issues.
