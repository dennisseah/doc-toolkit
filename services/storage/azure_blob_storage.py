import datetime

from azure.storage.blob import BlobSasPermissions, generate_blob_sas
from azure.storage.blob.aio import BlobServiceClient

from common.settings import Settings


async def is_blob_exists(
    settings: Settings, container_name: str, blob_name: str
) -> bool:
    """Checks if a blob exists in the storage account.

    :param conn_str: Connection string to the storage account.
    :param container_name: Name of the container.
    :param blob_name: Name of the blob.
    :return: True if the blob exists, False otherwise.
    """
    async with BlobServiceClient.from_connection_string(
        settings.azure_storage_connection_string
    ) as client:
        blob_client = client.get_blob_client(container=container_name, blob=blob_name)
        return await blob_client.exists()


async def download_blob_as_str(settings: Settings, container_name: str, blob_name: str):
    """Downloads a blob from the storage account.

    :param conn_str: Connection string to the storage account.
    :param container_name: Name of the container.
    :param blob_name: Name of the blob.
    :return: Blob contents.
    """
    async with BlobServiceClient.from_connection_string(
        settings.azure_storage_connection_string
    ) as client:
        blob_client = client.get_blob_client(container=container_name, blob=blob_name)
        downloader = await blob_client.download_blob(
            max_concurrency=1, encoding="UTF-8"
        )
        return await downloader.readall()


async def create_sas_url(
    settings: Settings,
    container_name: str,
    blob_name: str,
    permission: BlobSasPermissions = BlobSasPermissions(read=True),
    duration_seconds: int = 3600,
) -> str:
    """creates a sas URL for a blob

    :param conn_str: Connection string to the storage account.
    :param container_name: Name of the container.
    :param blob_name: Name of the blob.
    :param permission: Permission to grant.
    :param duration_seconds: SAS duration in seconds.
    :return: SAS URL
    """
    async with BlobServiceClient.from_connection_string(
        settings.azure_storage_connection_string
    ) as client:
        start_time = datetime.datetime.now(datetime.timezone.utc)
        expiry_time = start_time + datetime.timedelta(seconds=duration_seconds)

        token = generate_blob_sas(
            account_name=client.account_name,  # type: ignore
            account_key=client.credential.account_key,
            container_name=container_name,
            blob_name=blob_name,
            permission=permission,
            expiry=expiry_time,
            start=start_time,
        )

        account = str(client.account_name)

        return f"https://{account}.blob.core.windows.net/{container_name}/{blob_name}?{token}"


async def upload_blob(
    settings: Settings,
    container_name: str,
    blob_name: str,
    data: bytes | str,
    overwrite: bool = False,
):
    """
    Uploads a blob to the storage account.

    :param conn_str: Connection string to the storage account.
    :param container_name: Name of the container.
    :param blob_name: Name of the blob.
    :param data: Data to upload.
    :param overwrite: Overwrite the blob if it exists.
    """
    async with BlobServiceClient.from_connection_string(
        settings.azure_storage_connection_string
    ) as client:
        blob_client = client.get_blob_client(container=container_name, blob=blob_name)
        await blob_client.upload_blob(data, overwrite=overwrite)
