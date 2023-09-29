from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class NatType(int, Enum):
    EndpointIndependent = 1
    EndpointDependent = 2

class Peer(BaseModel):
    username: str = Field(...)
    ip: str = Field(...)
    ports: List[int] = Field(...)
    natType: NatType

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "username": "enrique",
                "ip": "111.111.111.111",
                "ports": [
                    5555,
                    6666,
                    7777
                ],
                "natType": 1
            }
        }

class PeerUpdate(BaseModel):
    ip: Optional[str] = Field(...)
    ports: Optional[List[int]] = Field(...)
    natType: Optional[NatType] = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "ip": "111.111.111.222",
                "ports": [
                    9999
                ],
                "natType": 2
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
                        "ports": [
                            5555,
                            6666,
                            7777
                        ],
                        "natType": 1
                    },
                    {
                        "username": "guille", 
                        "ip": "222.222.222.222",
                        "ports": [
                            8888,
                            9999
                        ],
                        "natType": 2
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
                        "ports": [
                            5555
                        ],
                        "natType": 1
                    }
                ]
            }
        }
