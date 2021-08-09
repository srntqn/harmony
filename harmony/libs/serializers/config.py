from pydantic import BaseModel, HttpUrl


class Config(BaseModel):
    config_location: str
    verify_ssl: bool
    k8s_api_server: HttpUrl
    k8s_api_key: str
