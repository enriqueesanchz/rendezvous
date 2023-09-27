from typing import List, Optional
from pydantic import BaseModel, Field

class Peer(BaseModel):
    username: str = Field(...)
    ip: str = Field(...)
    port: List[int] = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "username": "enrique",
                "ip": "111.111.111.111",
                "port": [
                    5555,
                    6666,
                    7777
                ]
            }
        }

class PeerUpdate(BaseModel):
    ip: Optional[str] = Field(...)
    port: Optional[List[int]] = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "ip": "111.111.111.222",
                "port": [
                    9999
                ]
            }
        }

class Namespace(BaseModel):
    name: str = Field(...)
    peers: List[Peer] = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "namespace1",
                "peers": [
                    {   "username": "enrique", 
                        "ip": "111.111.111.111",
                        "port": [
                            5555,
                            6666,
                            7777
                        ]
                    },
                    {
                        "username": "guille", 
                        "ip": "222.222.222.222",
                        "port": [
                            8888,
                            9999
                        ]
                    }
                ]
            }
        }

class NamespaceUpdate(BaseModel):
    peers: List[Peer]

    class Config:
        json_schema_extra = {
            "example": {
                "peers": [
                    {   "username": "enrique", 
                        "ip": "111.111.111.111",
                        "port": [
                            5555
                        ]
                    }
                ]
            }
        }
