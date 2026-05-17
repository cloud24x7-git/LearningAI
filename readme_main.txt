# readme_main.txt

This project contains a simple console-based chat client built around `LocalAgent/main.py`.

## What it does

- Defines an `Agent` class that sends chat requests to a local AI server.
- Uses `requests` to call the model endpoint and `rich` for console output.
- Sends one initial message, displays the model response, then prompts the user for a single follow-up input.
- Prints the assistant response and exits after one user message.

## Key details from `LocalAgent/main.py`

- Model: `qwen3.5`
- Local server base URL: `http://127.0.0.1:1234`
- Chat endpoint: `/v1/chat/completions`
- Requires an API key set on the `Agent` instance via `api_key`.
- Uses a single message history list to track both user and assistant messages.

## Dependencies

- `requests`
- `rich`

Install with pip:

```bash
pip install requests rich
```

## How to run

From the repository root or the `LocalAgent` directory:

```bash
python LocalAgent/main.py
```

## Behavior

1. The script creates an `Agent` instance.
2. It sends a greeting: "Hello, how are you?".
3. Prints the assistant reply.
4. Prompts the user for input.
5. Sends the user input to the model and prints the assistant reply.

## Notes

- The script currently performs only one interactive user turn after the initial greeting.
- You may need to update `api_key` on the `Agent` instance or modify the script to read it from environment variables.
