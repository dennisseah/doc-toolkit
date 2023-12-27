from azure.cognitiveservices.search.websearch import WebSearchClient
from msrest.authentication import CognitiveServicesCredentials

from common.settings import BingSearchSettings
from models.bing_search import BingSearchResponse


def get_client(settings: BingSearchSettings) -> WebSearchClient:
    """Get Azure Cognitive Search client.

    :param settings: Azure Cognitive Search settings.
    """
    client = WebSearchClient(
        endpoint=settings.azure_bing_search_endpoint,
        credentials=CognitiveServicesCredentials(settings.azure_bing_search_key),
    )
    client.config.base_url = "{Endpoint}/v7.0"  # workaround for a bug
    return client


def search(settings: BingSearchSettings, query: str) -> str:
    """Search Azure Cognitive Search.

    :param settings: Azure Cognitive Search settings.
    :param query: Query string.
    :return: Search results.
    """
    web_data = get_client(settings=settings).web.search(
        query=query, text_decorations=True, text_format="HTML"
    )
    results = BingSearchResponse(**web_data.as_dict())  # type: ignore
    if not results.web_pages or not results.web_pages.value:
        return ""

    # concatenate snippets into a single string
    return " ".join([v.snippet for v in results.web_pages.value if v.snippet])


if __name__ == "__main__":
    settings = BingSearchSettings.model_validate({})
    results = search(settings=settings, query="Python")
    print(results)
