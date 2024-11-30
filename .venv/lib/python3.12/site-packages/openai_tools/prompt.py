"""This module contains the class that wraps the prompt to the OpenAI API.
The prompt classes are used to create a prompt for the GPT-3 model.
The `LoggedPrompt` class is the base class for all prompts.
"""
import os
import json
from pathlib import Path
import openai
import backoff

from jinja2 import Template
from .utils import num_tokens_from_messages, build_prompt_id


# Load the OpenAI API key from the environment variable.
openai.api_key = os.environ.get('OPENAI_API_KEY')


class OpenAIException(BaseException):
    pass


@backoff.on_exception(backoff.expo, OpenAIException, max_tries=10)
def chat_completion_with_backoff(**kwargs):
    try:
        # # https://platform.openai.com/docs/api-reference/chat/create
        # response = openai.ChatCompletion.create(
        #     messages=message,
        #     **api_kwargs
        # )
        return openai.ChatCompletion.create(**kwargs)
    except openai.error.RateLimitError as e:
        raise OpenAIException(e)
    except openai.error.APIError as e:
        raise OpenAIException(e)


class LoggedPrompt:
    """Class for logging the prompts and responses from the GPT-3 model."""
    def __init__(self, payloads_dir: Path, task_label: str, model: str = "gpt-3.5-turbo", total_tokens: int = 4050, api_kwargs: dict = None) -> None:
        """Initialize the LoggedPrompt class.
        Args:
            payloads_dir (Path): The directory to store the payloads.
            task_label (str): The label for the task.
            model (str, optional): The GPT-3 model to use. Defaults to "gpt-3.5-turbo".
            total_tokens (int, optional): The total number of tokens to use. Defaults to 4050.
        """
        assert payloads_dir.exists(), f"The payloads directory does not exist: {payloads_dir}"

        self.payloads_dir = payloads_dir
        self.task_label = task_label

        self.model = model
        self.total_tokens = total_tokens

        # Initialize the prompt_label as None. This can be set specific to the
        # prompt when saving the response from the OpenAI endpoint.
        self.prompt_label = None

        self.default_api_kwargs = dict(
            model=self.model,
            temperature=0.7,
            top_p=1,
            n=1,
            stream=False,
            frequency_penalty=0,
            presence_penalty=0,
        )

        if api_kwargs is not None:
            self.default_api_kwargs.update(api_kwargs)

    def __str__(self) -> str:
        return self.__repr__()

    def _clean_message(self, message):
        """Clean the message to remove the tokens key."""
        if "tokens" in message:
            del message["tokens"]

        return message

    def calculate_prompt_tokens(self, message: dict) -> int:
        """Calculate the number of tokens in the prompt.
        Args:
            message (dict): The message to measure.
        Returns:
            int: The number of tokens in the prompt.
        """
        prompt_tokens = num_tokens_from_messages(message, self.model)

        return prompt_tokens

    @staticmethod
    def build_message(user_content: str, user_template: str = None, system_content: str = None):
        """Build the message to send to the GPT-3 model.
        Args:
            user_content (str): The user content to send to the GPT-3 model.
            user_template (str, optional): The template to use for the user content. Defaults to None.
            system_content (str, optional): The system content to send to the GPT-3 model. Defaults to None.
        Returns:
            dict: The message to send to the GPT-3 model.
        """
        if system_content is None:
            system_content = ""

        if user_template is None:
            user_template = "{{user_content}}"

        user_content = user_content.strip()
        user_template = user_template.strip()
        system_content = system_content.strip()

        content = Template(user_template).render(user_content=user_content)

        # Create the message to send to the GPT-3 model.
        message = [
            dict(role="system", content=system_content),
            dict(role="user", content=content),
        ]

        return message

    def send_prompt(self, user_content: str, user_template: str = None, system_content: str = None, metadata: dict = None, api_kwargs: dict = None, return_data: bool = False):
        """Send the prompt to the GPT-3 model.
        Args:
            variables (dict): The variables to classify.
        """
        if api_kwargs:
            api_kwargs = {**self.default_api_kwargs, **api_kwargs}
        else:
            api_kwargs = self.default_api_kwargs

        message = self.build_message(
            user_content=user_content,
            user_template=user_template,
            system_content=system_content,
        )

        # Apply cleaning to the message.
        message = self._clean_message(message)

        max_tokens = self.total_tokens -  self.calculate_prompt_tokens(message=message)
        api_kwargs["max_tokens"] = max_tokens

        response = chat_completion_with_backoff(messages=message, **api_kwargs)

        data = dict(
            message=message,
            response=response,
            content=response["choices"][0]["message"]["content"],
            api_kwargs=api_kwargs,
            metadata=metadata or {},
        )

        fid = f't{response["created"]}_{response["id"]}.json'

        if self.prompt_label is not None:
            fid = f'{self.prompt_label}_{fid}'

        # Create the directory for the prompt.
        prompt_id = build_prompt_id(user_template, system_content, api_kwargs)
        data_type_dir = self.payloads_dir / self.task_label / prompt_id
        data_type_dir.mkdir(parents=True, exist_ok=True)

        # Save the data to the file.
        (data_type_dir / fid).write_text(json.dumps(data, indent=2))

        if return_data:
            return data


class PromptZeros(LoggedPrompt):
    """Class for logging the prompts and responses from the GPT-3 model."""
    def __init__(self, payloads_dir: Path, task_label: str, model: str = "gpt-3.5-turbo", total_tokens: int = 4050, api_kwargs: dict = None) -> None:
        """Initialize the LoggedPrompt class.
        Args:
            payloads_dir (Path): The directory to store the payloads.
            task_label (str): The label for the task.
            model (str, optional): The GPT-3 model to use. Defaults to "gpt-3.5-turbo".
            total_tokens (int, optional): The total number of tokens to use. Defaults to 4050.
        """

        zero_kwargs = dict(
            temperature=0,
            top_p=0,
            frequency_penalty=0,
            presence_penalty=0,
        )

        if api_kwargs is not None:
            zero_kwargs.update(api_kwargs)

        super().__init__(payloads_dir=payloads_dir, task_label=task_label, model=model, total_tokens=total_tokens, api_kwargs=zero_kwargs)
