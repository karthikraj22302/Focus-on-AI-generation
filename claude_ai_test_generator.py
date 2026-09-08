!pip install -q anthropic openpyxl

from google.colab import files
import anthropic
import pandas as pd
import json
import re
import base64
import os

# ── PUT YOUR KEY HERE ──
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-PASTE-YOUR-KEY-HERE"
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Upload Screenshots
uploaded = files.upload()
image_folder = "/content"
image_files = sorted([f for f in uploaded.keys() if f.lower().endswith(('.png','.jpg','.jpeg'))])

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def build_prompt(image):
    return f"""
Generate 10-15 UNIQUE mobile functional test cases.
Return JSON format:
{{
 "test_cases":[
  {{
   "test_scenario":"",
   "test_case":"",
   "preconditions":"",
   "steps":["","","",""],
   "expected_result":""
  }}
 ]
}}
Screen: {image}
"""

def generate_test_cases(image_path, prompt):
    ext = image_path.lower().split('.')[-1]
    media_type = {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg'}.get(ext,'image/png')
    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": encode_image(image_path)
                    }
                },
                {"type": "text", "text": prompt}
            ]
        }]
    )
    text = response.content[0].text.strip()
    text = re.sub(r'^```json\s*|```\s*$', '', text, flags=re.MULTILINE).strip()
    return json.loads(text)["test_cases"]

def to_dataframe(test_cases, screen):
    rows = []
    for tc in test_cases:
        steps = tc.get("steps", [])
        rows.append({
            "Screen Name": screen,
            "Test Scenario": tc.get("test_scenario", ""),
            "Test Case": tc.get("test_case", ""),
            "Preconditions": tc.get("preconditions", ""),
            "Steps": "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)]),
            "Expected Result": tc.get("expected_result", "")
        })
    return pd.DataFrame(rows)

def generate_playwright_script(test_cases, screen_name):
    prompt = f"""
You are a Senior QA Automation Engineer.
Generate ONE Playwright JavaScript test function based on the given test cases.

STRICT RULES:
- Generate ONLY ONE test()
- Do NOT create multiple tests
- Do NOT use test.describe
- Follow real user flow (end-to-end)
- Use only these locators: getByText, getByPlaceholder, getByAltText, getByRole
- Do NOT use data-testid or CSS selectors
- Use randomNumber variable for dynamic data

Use this format EXACTLY:

const {{ test, expect }} = require('@playwright/test');

test('End-to-End Flow', async ({{ page }}) => {{
  const randomNumber = Math.floor(Math.random() * 1000);
  await page.goto('https://connle.telecmi.com/');
  await page.getByPlaceholder('Email').fill('test@mail.com');
  await page.getByPlaceholder('Password*').fill('Password123');
  await page.getByRole('button', {{ name: 'Login' }}).click();
}});

Test Cases:
{json.dumps(test_cases, indent=2)}
Return ONLY JavaScript code.
"""
    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def save_script(code, screen_name):
    file_name = screen_name.replace(".png","").replace(".jpg","") + ".spec.js"
    with open(file_name, "w") as f:
        f.write(code)
    return file_name

# ── MAIN ──
all_df = pd.DataFrame()
for image in image_files:
    print(f"Processing {image}...")
    path = os.path.join(image_folder, image)
    prompt = build_prompt(image)
    test_cases = generate_test_cases(path, prompt)
    df = to_dataframe(test_cases, image)
    all_df = pd.concat([all_df, df], ignore_index=True)
    script = generate_playwright_script(test_cases, image)
    file_name = save_script(script, image)
    files.download(file_name)
    print(f"Done: {file_name}")

excel_name = "TestCases.xlsx"
all_df.to_excel(excel_name, index=False)
files.download(excel_name)
print("All done!")
