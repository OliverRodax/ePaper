import os
import openai

# Get API key from environment
key = os.getenv("DASHBOARD_KEY")
if not key:
    raise SystemExit("DASHBOARD_KEY environment variable not set")

# Configure OpenAI client
client = openai.OpenAI(api_key=key)

def get_ai_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_tokens=150,
        )
        full_response = response.choices[0].message.content
        print(full_response)
        print()
        return full_response

    except openai.OpenAIError as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    test_prompt = "hab ich dich programmiert?"
    result = get_ai_response(test_prompt)
    
    if result:
        print("\nFull response received successfully!")