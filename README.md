# Simple HTTP rendezvous server for p2p apps
This REST API is used by p2p app's peers to meet each other

## Requirements
- fastapi[all]
- pymongo[srv]
- python-dotenv

## How to run the server
```
python3 -m uvicorn main:app
```
REST API docs will be in http://127.0.0.1:8000/docs

## Methods
![REST API methods](https://github.com/enriqueesanchz/rendezvous/blob/main/methods.png?raw=true)