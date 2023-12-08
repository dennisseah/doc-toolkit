from common.settings import Settings
from extractors.azure_form_recognizer import ParagraphRole, extract
from openai.token_count import num_tokens_from_string
from services.azure_blob_storage import get_sas_token, upload_blob


async def main():
    cfg = Settings.model_validate({})
    sas_token = await get_sas_token(
        settings=cfg,
        container_name="gpt-denz",
        blob_name="pdf_files/test.pdf",
    )
    result = await extract(
        cfg,
        sas_token,
        discard_roles=[
            ParagraphRole(role="pageHeader"),
            ParagraphRole(role="pageFooter"),
            ParagraphRole(role="pageNumber"),
        ],
    )

    print(num_tokens_from_string(result))

    await upload_blob(
        settings=cfg,
        container_name="gpt-denz",
        blob_name="result.txt",
        data=result,
        overwrite=True,
    )


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
