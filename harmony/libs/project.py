from pydantic import BaseModel


class Project(BaseModel):
    name: str
    storage_url: str
    version_file_name: str
    app_name: str
    app_namespace: str
