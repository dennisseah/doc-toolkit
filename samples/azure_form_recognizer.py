from common.settings import Settings
from extractors.azure_form_recognizer import extract
from services.azure_blob_storage import get_sas_token, upload_blob


async def main():
    cfg = Settings.model_validate({})
    sas_token = await get_sas_token(
        settings=cfg,
        container_name="sample",
        blob_name="pdf_files/test1.pdf",
    )
    result = await extract(cfg, sas_token)
    await upload_blob(
        settings=cfg,
        container_name="sample",
        blob_name="result.txt",
        data=result,
        overwrite=True,
    )


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
