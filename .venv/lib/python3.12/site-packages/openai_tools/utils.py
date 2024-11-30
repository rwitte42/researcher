import json
import uuid
import hashlib
import tiktoken


_TOKEN_ENC = {
    "gpt-3.5-turbo": tiktoken.encoding_for_model("gpt-3.5-turbo"),
    "gpt-4": tiktoken.encoding_for_model("gpt-4"),
}


def get_tiktoken_model(model):
    global _TOKEN_ENC
    encoding = _TOKEN_ENC.get(model)

    if encoding is None:
        try:
            _TOKEN_ENC[model] = encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            _TOKEN_ENC[model] = encoding = tiktoken.get_encoding("cl100k_base")

    return encoding


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    # https://platform.openai.com/docs/guides/chat/introduction

    encoding = get_tiktoken_model(model)

    if model in ["gpt-3.5-turbo-0301", "gpt-3.5-turbo", "gpt-4"]:  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


def build_prompt_id(user_template: str = None, system_content: str = None, api_kwargs: dict = None):
    # Create a unique ID for this combination of prompt, API arguments.
    k_dict = {}

    if api_kwargs is not None:
        k_dict = {**api_kwargs}

    # Remove max_tokens from the key, since it could vary
    # depending on the length of the prompt.
    if "max_tokens" in k_dict:
        del k_dict["max_tokens"]

    k_dict["system_content"] = system_content
    k_dict["user_template"] = user_template

    jkey = json.dumps(k_dict, sort_keys=True)

    return f"{uuid.UUID(hashlib.md5(jkey.encode('utf-8')).hexdigest())}"
