from agent import ReactAgent
from llm import call_llm


agent = ReactAgent(call_llm)

result = agent.run("Who is the CEO of OpenAI?")
print("\nFINAL RESULT:\n", result)