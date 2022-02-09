from pydantic import BaseSettings, Field, HttpUrl


class Config(BaseSettings):
    config_location: str = Field (..., env = 'CONFIG_LOCATION')
    verify_ssl: bool = Field (..., env = 'VERIFY_SSL')
    k8s_api_server: HttpUrl = Field(..., env = 'K8S_API_SERVER_HOST')
    k8s_api_key: str = Field(..., env = 'K8S_API_KEY')
    log_level: str = Field(..., env = 'LOG_LEVEL')
