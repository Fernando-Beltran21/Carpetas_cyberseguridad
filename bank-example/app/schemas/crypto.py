from pydantic import BaseModel, Field


class HashDemoRequest(BaseModel):
    data: str = Field(min_length=1)


class HashDemoResponse(BaseModel):
    input: str
    md5: str
    sha256: str
