from datetime import datetime
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Namespace, NamespaceUpdate, Peer, PeerUpdate

router = APIRouter()

@router.post("/", response_description="Create a new namespace", status_code=status.HTTP_201_CREATED, response_model=Namespace)
def create_namespace(request: Request, namespace: Namespace = Body(...)):
    namespace = jsonable_encoder(namespace)
    namespace["lastModifiedDate"] = datetime.utcnow()
    
    existing_namespace = request.app.database["namespaces"].find_one(
        {"name": namespace["name"]}
    )
    if(existing_namespace == None):
        new_namespace = request.app.database["namespaces"].insert_one(namespace)
        created_namespace = request.app.database["namespaces"].find_one(
            {"_id": new_namespace.inserted_id}
        )

        return created_namespace
    
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Namespace with name {namespace['name']} already exists")

@router.get("/", response_description="List all namespaces", response_model=List[Namespace])
def list_namespaces(request: Request):
    namespaces = list(request.app.database["namespaces"].find(limit=100))
    return namespaces

@router.get("/{name}", response_description="Get a single namespace by name", response_model=Namespace)
def find_namespace(name: str, request: Request):
    if (namespace := request.app.database["namespaces"].find_one({"name": name})) is not None:
        return namespace
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} not found")

@router.put("/{name}", response_description="Update a namespace", response_model=Namespace)
def update_namespace(name: str, request: Request, namespace: NamespaceUpdate = Body(...)):
    namespace = {k: v for k, v in namespace.dict().items() if v is not None}
    namespace["lastModifiedDate"] = datetime.utcnow()
    
    if len(namespace) >= 1:
        update_result = request.app.database["namespaces"].update_one(
            {"name": name}, {"$set": namespace}
        )

    if (
        existing_namespace := request.app.database["namespaces"].find_one({"name": name})
    ) is not None:
        return existing_namespace

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} not found")

@router.put("/{name}/{username}", response_description="Update a peer", response_model=Namespace)
def update_peer(name: str, username: str, request: Request, peer: PeerUpdate = Body(...)):
    peer = {k: v for k, v in peer.dict().items() if v is not None}

    existing_peer = request.app.database["namespaces"].find_one(
        {"peers": { "$elemMatch": { "username": username } } }
    )
    
    if(existing_peer == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} and user {username} not found")

    if len(peer) >= 1 and existing_peer != None:
        if ("ports" in peer.keys()):
            update_result = request.app.database["namespaces"].update_one(
                {"name": name, "peers.username": username}, {"$set": {"peers.$.ports":  peer["ports"]}}
            )
            print(update_result)
        
        if ("ip" in peer.keys()):
            update_result = request.app.database["namespaces"].update_one(
                {"name": name, "peers.username": username}, {"$set": {"peers.$.ip":  peer["ip"]}}
            )

        if ("natType" in peer.keys()):
            update_result = request.app.database["namespaces"].update_one(
                {"name": name, "peers.username": username}, {"$set": {"peers.$.natType":  peer["natType"]}}
            )

        update_result = request.app.database["namespaces"].update_one(
            {"name": name}, {"$set": {"lastModifiedDate": datetime.utcnow()}}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} was not found")

    if (
        existing_namespace := request.app.database["namespaces"].find_one({"name": name, "peers.username": username})
    ) is not None:
        return existing_namespace

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} and user {username} not found")

@router.delete("/{name}", response_description="Delete a namespace")
def delete_namespace(name: str, request: Request, response: Response):
    delete_result = request.app.database["namespaces"].delete_one({"name": name})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} not found")

@router.post("/{name}", response_description="Create a new peer", status_code=status.HTTP_201_CREATED, response_model=Namespace)
def create_peer(name: str, request: Request, peer: Peer = Body(...)):
    peer = jsonable_encoder(peer)
    
    existing_peer = request.app.database["namespaces"].find_one(
        {"name": name, "peers.username": peer["username"]}
    )
    if(existing_peer == None):
        update_result = request.app.database["namespaces"].update_one(
            {"name": name}, {"$push": {"peers": peer}}
        )
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} was not found")
        
        update_result = request.app.database["namespaces"].update_one(
            {"name": name}, {"$set": {"lastModifiedDate": datetime.utcnow()}}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} was not found")

        if (
            existing_namespace := request.app.database["namespaces"].find_one({"name": name})
        ) is not None:
            return existing_namespace
    
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Peer with name {peer['username']} already exists in {name}")
