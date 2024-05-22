
from ollama import Client
# rich
from rich import pretty
from rich import print,print_json
from rich.console import Console

pretty.install()
console = Console()

client = Client(host='http://localhost:11434')



response = client.chat(model='llama3', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

console.print_json(response)