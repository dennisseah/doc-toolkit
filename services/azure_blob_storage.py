import datetime

from azure.storage.blob import BlobSasPermissions, generate_blob_sas
from azure.storage.blob.aio import BlobServiceClient

from common.settings import Settings


async def get_sas_token(
    settings: Settings,
    container_name: str,
    blob_name: str,
    permission: BlobSasPermissions = BlobSasPermissions(read=True),
    duration_seconds: int = 3600,
):
    """Get a blob from a container.

    :param conn_str: Connection string to the storage account.
    :param container_name: Name of the container.
    :param blob_name: Name of the blob.
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
