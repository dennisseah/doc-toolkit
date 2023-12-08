from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_storage_connection_string: str
    azure_form_recognizer_endpoint: str
    azure_form_recognizer_key: str

    class Config:
        env_file = ".env"
