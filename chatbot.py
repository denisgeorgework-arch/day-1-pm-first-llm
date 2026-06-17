import os, getpass
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)
print("LiteLLM client ready | base_url:", base_url, "| model:", MODEL)
def ask(prompt, system="You are a concise and friendly assistant.",
        temperature=0.7, model=MODEL):
    r = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    return r.choices[0].message.content, (r.usage.prompt_tokens, r.usage.completion_tokens)
reply, usage = ask("What's the capital of France?")
print(reply)
print("tokens (in, out):", usage)
promptheader="These are the previous prompt memories that you must refer to if relevant to the question with just the reply. All the questions i ask will start with the keyword ME. For reference the replies in the memory liststarts with the keyword AI If no memories then just respond to the prompt as usual in plain string: "
promptlist=""

while True:
    prompt=input("Enter prompt: ")
    temp=float(input("Enter temperature:"))
    totalprompt=promptheader+promptlist+"\n THE QUESTION IS :\n"+prompt
    reply, usage = ask(totalprompt, temperature=temp)
    print(reply)
    print("tokens (in, out):", usage)
    promptlist+="\nME: "+prompt+"\n"+"AI:"+reply