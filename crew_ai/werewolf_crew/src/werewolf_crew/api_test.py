from openai import OpenAI

client = OpenAI()
client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "Say hello"}]
)
