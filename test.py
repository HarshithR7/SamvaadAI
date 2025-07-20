from openai import OpenAI

client = OpenAI(api_key="your-api-key")

usage = client.api_usage.retrieve()
print(usage)