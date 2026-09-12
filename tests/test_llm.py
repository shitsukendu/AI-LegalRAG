from src.llm import ask_gemini


prompt = """
Explain in one sentence what a legal contract is.
"""


answer = ask_gemini(prompt)


print("\n" + "=" * 60)
print("GEMINI LLM TEST")
print("=" * 60)

print("\nAnswer:")
print(answer)