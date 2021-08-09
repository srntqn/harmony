from pydantic import BaseModel


class Image(BaseModel):
    name: str
    tag_in_cluster: str
    tag_in_vcs: str
