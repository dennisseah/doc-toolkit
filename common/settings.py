from pydantic_settings import BaseSettings


class FormRecognizerSettings(BaseSettings):
    """Settings for Azure Form Recognizer."""

    azure_form_recognizer_endpoint: str
    azure_form_recognizer_key: str

    class Config:
        env_file = ".env"
        extra = "ignore"


class AzureBlobStorageSettings(BaseSettings):
    """Settings for Azure Blob Storage."""

    azure_storage_connection_string: str

    class Config:
        env_file = ".env"
        extra = "ignore"


class AzureOpenAISettings(BaseSettings):
    """Settings for Azure OpenAI service."""

    openai_azure_endpoint: str
    azure_openai_api_key: str
    openai_api_version: str
    deployment_model: str
    openai_embedding_model: str
    request_timeout: int = 30
    max_retry_time_secs: int = 32
    max_token_count: int | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


class AzurePostgreSQLSettings(BaseSettings):
    pghost: str
    pguser: str
    pgpassword: str
    pgport: str
    pgdatabase: str
    pgssl: str

    class Config:
        env_file = ".env"
        extra = "ignore"


class AzureCognitiveSearchSettings(BaseSettings):
    azure_cognitive_search_endpoint: str
    azure_cognitive_search_key: str

    class Config:
        env_file = ".env"
        extra = "ignore"


class Settings(FormRecognizerSettings, AzureBlobStorageSettings, AzureOpenAISettings):
    class Config:
        env_file = ".env"
