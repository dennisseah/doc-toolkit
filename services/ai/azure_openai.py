import asyncio
import logging
from typing import Any, Awaitable, Callable, TypeVar

from openai import (
    APIError,
    APITimeoutError,
    AsyncAzureOpenAI,
    AzureOpenAI,
    RateLimitError,
)
from openai.types import CreateEmbeddingResponse
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from common.settings import AzureOpenAISettings

T = TypeVar("T")


async def rate_limit(
    callable: Callable[..., Awaitable[T]], params: dict[str, Any], max_retry_time: int
) -> T | None:
    retry_time = 1
    while retry_time > 0:
        try:
            response = await callable(**params)
            return response
        except RateLimitError as rle:
            retry_time = retry_time * 2
            logging.warning(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
            logging.warning(str(response["usage"]))  # type: ignore

            if retry_time > max_retry_time:
                raise rle
            await asyncio.sleep(retry_time)
        except APITimeoutError:
            retry_time = retry_time * 2
            logging.warning(f"Timeout error. Retrying in {retry_time} seconds...")

            if retry_time > max_retry_time:
                logging.warning(
                    f"Timeout exceeded max_retry_time of {max_retry_time}. Returning an"
                    " empty response"
                )
                return None
            await asyncio.sleep(retry_time)
        except APIError as err:
            retry_time = retry_time * 2

            logging.warning(
                f"OpenAI APIError {err}. Retrying in {retry_time} seconds..."
            )

            if retry_time > max_retry_time:
                return None
            await asyncio.sleep(retry_time)


async def get_completion(
    settings: AzureOpenAISettings,
    messages: list[ChatCompletionMessageParam],
    temperature: float = 0.0,
) -> ChatCompletion | None:
    """Get a completion from the OpenAI API.

    :param settings: The settings to use for the API.
    :param messages: The messages to use for the completion.
    :param temperature: The temperature to use for the completion.
    """
    logging.info("begin completion")

    async with AsyncAzureOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.openai_azure_endpoint,
        api_version=settings.openai_api_version,
    ) as aclient:
        response = await rate_limit(
            callable=aclient.chat.completions.create,
            params={
                "model": settings.deployment_model,
                "temperature": temperature,
                "timeout": settings.request_timeout,
                "messages": messages,
            },
            max_retry_time=settings.max_retry_time_secs,
        )
    logging.info("completed completion")
    return response


def get_embedding(settings: AzureOpenAISettings, text: str) -> CreateEmbeddingResponse:
    """Get an embedding from the OpenAI API.

    :param settings: The settings to use for the API.
    :param text: The text to use for the embedding.
    """
    logging.info("begin get_embedding")

    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    client = AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.openai_azure_endpoint,
        api_version=settings.openai_api_version,
    )

    result = client.embeddings.create(input=text, model=settings.openai_embedding_model)
    logging.info("completed get_embedding")
    return result


# async def main():
#     from openai.types.chat import ChatCompletionSystemMessageParam

#     settings = AzureOpenAISettings.model_validate({})
#     response = await get_completion(
#         settings=settings,
#         messages=[
#             ChatCompletionSystemMessageParam(role="system", content="Write a poem")
#         ],
#     )
#     print(response)

#     print(get_embedding(settings, "This is a test"))


# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
