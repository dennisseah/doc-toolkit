import tiktoken


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Return the number of tokens in a string.

    :param string: The string to count tokens in.
    :param encoding_name: The name of the encoding to use.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))
