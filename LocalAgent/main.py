import requests
from rich.console import Console
from dataclasses import dataclass, field
from typing import Any
@dataclass
class Agent:
    model: str = "qwen3.5"
    base_url: str = "http://127.0.0.1:1234"
    api_key: str = field(default="NO_API_KEY", repr=False)
    messages: list[dict[str, Any]] = field(default_factory=list)
    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
    
    
    def chat(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})
        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        r = requests.post(
            url,
            headers=headers,
            json={"model": self.model, "messages": self.messages},
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
    console = Console()
    with console.status("[dim]Thinking...[/dim]", spinner="arc"):
        response = agent.chat("Hello, how are you?")
   
    console.print(f"[bold green]Assistant:[/bold green] {response}")
    console.print("\n[bold blue]YOU:[/bold blue]")
    user_input = console.input()
    if user_input.strip().lower() in {"quit", "exit"}:
        console.print("[bold red]Good Bye...[/bold red]")
        return
    with console.status("[dim]Thinking...[/dim]", spinner="arc"):
        response = agent.chat(user_input).strip()
    console.print(f"[bold green]SpongeBob:[/bold green] {response}")
if __name__ == "__main__":
    main()


