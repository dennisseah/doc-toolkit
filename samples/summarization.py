import json
import logging

from openai.types.chat import ChatCompletionSystemMessageParam
from pydantic import BaseModel

import evaluators.rouge as rouge_eval
import services.ai.azure_openai as azure_openai
import services.azure_blob_storage as blob_storage
from common.settings import Settings
from extractors.azure_form_recognizer import ParagraphRole, extract

DISCARD_ROLES = [
    ParagraphRole(role="pageHeader"),
    ParagraphRole(role="pageFooter"),
    ParagraphRole(role="pageNumber"),
]

CONTAINER_NAME = "gpt-denz"
BLOB_NAME = "pdf_files/test1.pdf"
RESULT_BLOB_NAME = "result.txt"

PROMPT = """You are a medical expert, you are given a medical document, and you need to write a summary of it.

Instructions:
- Write a brief summary of the document.
- Provide key points in the document that support your summary.

Medical document:
{{document}}

Give your summary in this JSON format:
```
{
    "summary": "This is a summary of the document.",
    "points": ["point 1", "point 2"]
}
```
"""  # noqa E501


class RougeMetric(BaseModel):
    result: str
    scores: rouge_eval.RougeScores


class Result(BaseModel):
    summary: str
    points: list[str]
    metrics: list[RougeMetric] | None = None


async def fetch_sas_url(settings: Settings):
    return await blob_storage.create_sas_url(
        settings=settings,
        container_name=CONTAINER_NAME,
        blob_name=BLOB_NAME,
    )


async def get_textual_data(settings: Settings) -> str:
    sas_token = await fetch_sas_url(settings)
    return await extract(
        settings=settings,
        sas_url=sas_token,
        discard_roles=DISCARD_ROLES,
    )


async def save_textual_data(settings: Settings, data: str):
    await blob_storage.upload_blob(
        settings=settings,
        container_name=CONTAINER_NAME,
        blob_name=RESULT_BLOB_NAME,
        data=data,
        overwrite=True,
    )


async def main():
    settings = Settings.model_validate({})

    # get textual data from PDF with form recognizer. if it is already extracted, skip
    # this step and get it from blob storage
    if not await blob_storage.is_blob_exists(
        settings=settings, container_name=CONTAINER_NAME, blob_name=RESULT_BLOB_NAME
    ):
        logging.info("Extracting data from PDF...")
        data = await get_textual_data(settings)
        await save_textual_data(settings=settings, data=data)
    else:
        data = await blob_storage.download_blob_as_str(
            settings=settings, container_name=CONTAINER_NAME, blob_name=RESULT_BLOB_NAME
        )

    # get ChatGPT to summarize the document
    response = await azure_openai.get_completion(
        settings=settings,
        messages=[
            ChatCompletionSystemMessageParam(
                role="system", content=PROMPT.replace("{{document}}", data)
            )
        ],
        temperature=0,
    )

    if response is not None and response.choices:
        # TODO: check for valid JSON
        response_text = json.loads(response.choices[0].message.content)  # type: ignore
        result = Result(**response_text)
        result.metrics = [
            RougeMetric(
                result=point, scores=rouge_eval.evaluate(result=point, target=data)
            )
            for point in result.points
        ]
        print(json.dumps(result.model_dump(), indent=4))

    else:
        print("No response from GPT")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
