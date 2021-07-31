from pydantic import BaseModel


class Config(BaseModel):
    config_location: str
    verify_ssl: bool
    k8s_api_server: str
    k8s_api_key: str
