import requests
from rich.console import Console
import datetime
import getpass
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Agent:
    system: str = "You are a helpful assistant named SpongeBob."
    model: str = "qwen3.5"
    base_url: str = "http://127.0.0.1:1234"
    api_key: str = field(default="NO_API_KEY", repr=False)
    contexts: dict[str, Callable[[], str]] = field(default_factory=dict)
    messages: list[dict[str, Any]] = field(default_factory=list)

    # remove trailing / from base_url
    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        # include system message if provided
        if getattr(self, "system", None):
            self.messages.insert(0, {"role": "system", "content": self.system})
    
    def context(self, func: Callable[[], str]) -> Callable[[], str]:
        self.contexts[func.__name__] = func
        return func


    def chat(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})

        context_content = "\n\n".join(
            f"{n}:\n<{n}>{fn()}</{n}>\n</context>"
            for n, fn in self.contexts.items()
        )

        prefix: list[dict[str, Any]] = [
            {"role": "system", "content": self.system},
            {"role": "system", "content": context_content},
        ]





        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        r = requests.post(
            url,
            headers=headers,
            json={"model": self.model, "messages": prefix + self.messages},
            timeout=300,
        )
        r.raise_for_status()
        data = r.json()
        choices = data.get("choices")
        if not choices:
            error_detail = data.get("error") or data.get("detail") or data
            raise RuntimeError(f"Model response missing choices: {error_detail}")
        
        message = choices[0].get("message")
        if message is None:
            raise RuntimeError("Model response missing message")
                
        response = message.get("content") or ""
        self.messages.append({"role": "assistant", "content": response})
        return response 
    

def main() -> None:
    agent = Agent(model="qwen3.5")
    system_prommpt = "End every message with @@@@@@"
    # apply system prompt to the agent
    agent.system = system_prommpt

    @agent.context
    def user_context() -> str:
        now = datetime.datetime.now()
        return (
            f"The current time is {datetime.datetime.now()}\n"
            f"The current user is {getpass.getuser()}\n"
        )

   
    
if __name__ == "__main__":
    main()


