from common.settings import Settings
from services.azure_blob_storage import get_sas_token
from services.azure_form_recognizer import analyze


async def extract(cfg: Settings, sas_url: str):
    await analyze(cfg, sas_url)


async def main():
    cfg = Settings.model_validate({})
    sas_token = await get_sas_token(
        settings=cfg,
        container_name="gpt-denz",
        blob_name="pdf_files/test1.pdf",
    )
    await extract(cfg, sas_token)


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
