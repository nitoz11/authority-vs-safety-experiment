import json
import os
import time
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL = "qwen/qwen-2.5-7b-instruct"

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY was not found in .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


# --------------------------------------------------
# Load prompts
# --------------------------------------------------

with open("prompts.json", "r", encoding="utf-8") as f:
    prompts = json.load(f)


# --------------------------------------------------
# Create results directory
# --------------------------------------------------

os.makedirs("results", exist_ok=True)

results = []

print(f"Loaded {len(prompts)} prompts.")
print(f"Model: {MODEL}")
print("-" * 60)


# --------------------------------------------------
# Run experiment
# --------------------------------------------------

for i, item in enumerate(prompts, start=1):

    scenario = item["scenario"]
    cell = item["cell"]
    scope = item["scope"]
    user_prompt = item["user_prompt"]

    print(f"\nRunning {i}/{len(prompts)}")
    print(f"Scenario: {scenario}")
    print(f"Cell: {cell}")
    print(f"Prompt: {user_prompt}")

    try:

        # IMPORTANT:
        # Every request is a completely fresh conversation.
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": scope
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0
        )

        model_response = response.choices[0].message.content

        result = {
            "experiment_timestamp": datetime.now().isoformat(),
            "model": MODEL,
            "scenario": scenario,
            "cell": cell,
            "authority_condition": item["condition"]["authority"],
            "safety_condition": item["condition"]["safety"],
            "system_prompt": scope,
            "user_prompt": user_prompt,
            "response": model_response,

            # Manual coding fields.
            # We leave these blank initially.
            "behavior": "",
            "reason": "",
            "authority_mentioned": "",
            "harm_mentioned": "",
            "alternative_offered": "",
            "refusal_strength": "",
            "notes": ""
        }

        results.append(result)

        print("Response:")
        print(model_response)

    except Exception as e:

        print(f"ERROR: {e}")

        results.append({
            "experiment_timestamp": datetime.now().isoformat(),
            "model": MODEL,
            "scenario": scenario,
            "cell": cell,
            "authority_condition": item["condition"]["authority"],
            "safety_condition": item["condition"]["safety"],
            "system_prompt": scope,
            "user_prompt": user_prompt,
            "response": "",
            "error": str(e),

            "behavior": "",
            "reason": "",
            "authority_mentioned": "",
            "harm_mentioned": "",
            "alternative_offered": "",
            "refusal_strength": "",
            "notes": ""
        })

    # Small delay between requests.
    time.sleep(1)


# --------------------------------------------------
# Save results
# --------------------------------------------------

output_file = "results/results_primary.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)


print("\n" + "=" * 60)
print("EXPERIMENT COMPLETE")
print("=" * 60)
print(f"Results saved to: {output_file}")
print(f"Total prompts: {len(results)}")