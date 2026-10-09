
# Task 1 — Upload findings.json
import json

with open("findings.json", "r") as f:
    findings = json.load(f)

print(json.dumps(findings, indent=4))

#Task 2 — generate_scr_narrative(findings: dict) -> dict

from google import genai
from google.colab import userdata
from google.colab import files
from google.genai import types, errors

key = userdata.get('sy_api_key')
client = genai.Client(api_key = key)


def generate_scr_narrative(findings: dict) -> dict:

    system_instruction = """
You are a senior data analyst writing for Mamaearth's regional ops and finance heads.

Write exactly three labeled sections:
Situation
Complication
Resolution

Every number in the narrative must come from the supplied findings.
Use the numbers exactly as provided.
Do not invent any statistics.
"""

    user_prompt = f"""
Create a concise business narrative from these findings:

{findings}
"""

    client = genai.Client(api_key=key)

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=user_prompt,
        config={
            "system_instruction": system_instruction
        }
    )

    return {
        "status": "success",
        "narrative": response.text.strip(),
        "tokens": response.usage_metadata.total_token_count
    }

print(generate_scr_narrative(findings))

#Task 3 — Parameter locking and error handling


def generate_scr_narrative(findings: dict) -> dict:

    system_instruction = """
You are a senior data analyst writing for Mamaearth's regional ops and finance heads.

Write exactly three labeled sections:
Situation
Complication
Resolution

Every number in the narrative must come from the supplied findings.
Use the numbers exactly as provided.
Do not invent any statistics.
"""

    user_prompt = f"""
Create a concise business narrative from these findings:

{findings}
"""

    try:
        client = genai.Client(api_key=key)

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                # Temperature 0.0 makes the output deterministic because this is a factual business report, not creative writing.
                temperature=0.0,

                # Explicitly limits the maximum number of output tokens.
                max_output_tokens=500,

                # 15 seconds timeout, which is greater than the required 10 seconds.
                http_options=types.HttpOptions(timeout=15000)
            )
        )

        return {
            "status": "success",
            "narrative": response.text.strip(),
            "tokens": response.usage_metadata.total_token_count
        }

    except Exception as err:

        return {
            "status": "error",
            "narrative": None,
            "message": str(err)
        }


result = generate_scr_narrative(findings)

print("Status:", result["status"])

if result["status"] == "success":
    print("\nNarrative:")
    print(result["narrative"])
    print("\nTokens:", result["tokens"])
else:
    print("\nError:", result["message"])

with open("sample_output.txt", "w") as file:
    file.write(result["narrative"])

# Task 4 — Offline fallback path

def generate_scr_narrative_offline(findings: dict) -> dict:

    narrative = f"""
]Situation

Cleaned revenue: ₹{findings['cleaned_total_revenue_inr']}
Raw revenue: ₹{findings['raw_total_revenue_inr']}
Duplicate reconciliation difference: ₹{findings['duplicate_reconciliation_delta_inr']}

Complication

COD return rate: {findings['return_rate_by_payment']['COD']}
Highest-risk segment: {findings['highest_risk_segment']['payment_method']}
City tier: {findings['highest_risk_segment']['city_tier']}
Return rate: {findings['highest_risk_segment']['return_rate_pct']}%

Resolution

True peak month: {findings['true_peak_month']['month']}
True peak revenue: ₹{findings['true_peak_month']['revenue_inr']}
Apparent peak month: {findings['outlier_inflated_month']['month']}
Apparent revenue: ₹{findings['outlier_inflated_month']['apparent_revenue_inr']}
Corrected revenue: ₹{findings['outlier_inflated_month']['corrected_revenue_inr']}
""".strip()

    return {
        "status": "success",
        "narrative": narrative,
        "tokens": 0
    }


result = generate_scr_narrative_offline(findings)
print(result["narrative"])

def check_narrative(narrative):

    text = narrative.replace(",", "")

    if "97358.3" in text:
        print("PASS: Cleaned total revenue")
    else:
        print("FAIL: Cleaned total revenue")

    if "44.4" in text:
        print("PASS: COD return rate")
    else:
        print("FAIL: COD return rate")

    if "54.5" in text:
        print("PASS: COD + Tier-2 highest-risk segment return rate")
    else:
        print("FAIL: COD + Tier-2 highest-risk segment return rate")

    if "2501.9" in text:
        print("PASS: Duplicate reconciliation delta")
    else:
        print("FAIL: Duplicate reconciliation delta")

    if ("march" in text.lower() or "2026-03" in text) and "20318.9" in text:
        print("PASS: March peak revenue")
    else:
        print("FAIL: March peak revenue")


with open("sample_output.txt", "r") as file:
    sample_output = file.read()

check_narrative(sample_output)
