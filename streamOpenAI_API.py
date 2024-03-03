from openai import OpenAI
api_key=""
client = OpenAI(api_key=api_key)

stream = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[{"role": "user", "content": "Jsi robot NAO. Je ti 14 let. A žiješ v Český Budějovicích."}, {"role": "assistant", "content": "Ahoj, jak se máš?"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
