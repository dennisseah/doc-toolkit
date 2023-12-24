from azure.cognitiveservices.search.websearch import WebSearchClient
from msrest.authentication import CognitiveServicesCredentials

from common.settings import AzureCognitiveSearchSettings
from models.cognitive_search import CognitiveSearchResponse


def get_client(settings: AzureCognitiveSearchSettings) -> WebSearchClient:
    """Get Azure Cognitive Search client.

    :param settings: Azure Cognitive Search settings.
    """
    client = WebSearchClient(
        endpoint=settings.azure_cognitive_search_endpoint,
        credentials=CognitiveServicesCredentials(settings.azure_cognitive_search_key),
    )
    client.config.base_url = "{Endpoint}/v7.0"
    return client


def search(settings: AzureCognitiveSearchSettings, query: str) -> str:
    """Search Azure Cognitive Search.

    :param settings: Azure Cognitive Search settings.
    :param query: Query string.
    :return: Search results.
    """
    web_data = get_client(settings=settings).web.search(
        query=query, text_decorations=True, text_format="HTML"
    )
    results = CognitiveSearchResponse(**web_data.as_dict())  # type: ignore
    if not results.web_pages or not results.web_pages.value:
        return ""

    return " ".join([v.snippet for v in results.web_pages.value if v.snippet])


# if __name__ == "__main__":
#     settings = AzureCognitiveSearchSettings.model_validate({})
#     results = search(settings=settings, query="Python")
#     print(results)
