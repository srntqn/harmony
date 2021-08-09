from pydantic import BaseModel, HttpUrl


class Project(BaseModel):
    name: str
    vcs_url: HttpUrl
    app_name: str
    app_namespace: str
