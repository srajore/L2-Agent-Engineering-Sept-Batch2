from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="gpt-oss:120b-cloud"
)

response = llm.invoke("How do I learn Agnetic AI quickly?")

print(response.content)
