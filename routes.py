from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Namespace, NamespaceUpdate, PeerUpdate

router = APIRouter()

@router.post("/", response_description="Create a new namespace", status_code=status.HTTP_201_CREATED, response_model=Namespace)
def create_namespace(request: Request, namespace: Namespace = Body(...)):
    namespace = jsonable_encoder(namespace)
    
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
    if len(namespace) >= 1:
        update_result = request.app.database["namespaces"].update_one(
            {"name": name}, {"$set": namespace}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} not found")

    if (
        existing_namespace := request.app.database["namespaces"].find_one({"name": name})
    ) is not None:
        return existing_namespace

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} not found")

@router.put("/{name}/{username}", response_description="Update a peer", response_model=Namespace)
def update_peer(name: str, username: str, request: Request, peer: PeerUpdate = Body(...)):
    peer = {k: v for k, v in peer.dict().items() if v is not None}

    existing_peer = request.app.database["namespaces"].find_one(
        { "peers.username": username }, {"peers": { "$elemMatch": { "username": username } } }
    )

    if len(peer) >= 1:
        if ("port" in peer.keys()):
            update_result = request.app.database["namespaces"].update_one(
                {"name": name, "peers.username": username}, {"$set": {"peers.$.port":  peer["port"]}}
            )

            if update_result.modified_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} and user {username} not found")
        
        if ("ip" in peer.keys()):
            update_result = request.app.database["namespaces"].update_one(
                    {"name": name, "peers.username": username}, {"$set": {"peers.$.ip":  peer["ip"]}}
            )

            if update_result.modified_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Namespace with name {name} and user {username} not found")

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
