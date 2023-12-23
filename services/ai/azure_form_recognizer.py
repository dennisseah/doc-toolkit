import azure.ai.formrecognizer as fr
import azure.ai.formrecognizer.aio as fr_aio
from azure.core.credentials import AzureKeyCredential

from common.settings import Settings


async def analyze(
    settings: Settings, sas_url: str, model="prebuilt-layout"
) -> fr.AnalyzeResult:
    """Analyze a document.

    :param settings: Settings object.
    :param sas_url: SAS URL to the document.
    :model: form recognizer model.
    """
    credential = AzureKeyCredential(settings.azure_form_recognizer_key)

    async with fr_aio.DocumentAnalysisClient(
        endpoint=settings.azure_form_recognizer_endpoint, credential=credential
    ) as client:
        poller = await client.begin_analyze_document_from_url(
            model_id=model, document_url=sas_url
        )
        return await poller.result()
