# AI Test Case Generator

Automatically generates functional test cases and Playwright automation scripts from mobile app screenshots using Claude AI (Anthropic). Exports structured test cases to Excel.

---

## What It Does

1. Upload app screenshots (PNG / JPG)
2. Claude AI analyses each screen
3. Generates 10–15 functional test cases per screen
4. Exports test cases to **Excel** (`TestCases.xlsx`)
5. Exports **Playwright JS scripts** (`.spec.js`) per screen

---

## Requirements

| Tool | Purpose |
|---|---|
| Google Colab | Run the script (free, no setup) |
| Anthropic API Key | Claude AI access |
| App Screenshots | Input images (PNG/JPG/JPEG) |

---

## Configuration

```python
# ── CONFIG ──────────────────────────────
ANTHROPIC_API_KEY = "sk-ant-api03-xxxxxxxxxx"   # Your API key
MODEL             = "claude-opus-5"              # Claude model
MAX_TOKENS        = 4096                         # Max output tokens
IMAGE_FOLDER      = "/content"                   # Colab upload folder
IMAGE_FORMATS     = ('.png', '.jpg', '.jpeg')    # Accepted formats
APP_URL           = "https://connle.telecmi.com/" # App URL for Playwright
LOGIN_EMAIL       = "test@mail.com"              # Test login email
LOGIN_PASSWORD    = "Password123"                # Test login password
EXCEL_OUTPUT      = "TestCases.xlsx"             # Output Excel filename
# ────────────────────────────────────────
```

---

## Setup — Step by Step

### Step 1 — Get Anthropic API Key
1. Go to **console.anthropic.com**
2. Sign Up / Sign In
3. Go to **Settings → API Keys**
4. Click **Create Key** → copy it (`sk-ant-api03-...`)
5. Go to **Billing** → add minimum **$5 credit**

### Step 2 — Open Google Colab
- Go to **colab.research.google.com**
- Click **New Notebook**

### Step 3 — Paste the script
- Copy the full script from `ai_test_generator.py`
- Paste into the first Colab cell
- Replace `ANTHROPIC_API_KEY` with your real key

### Step 4 — Run
- Press **Shift + Enter**
- A file picker appears → select your screenshots
- Wait for processing

### Step 5 — Download outputs
- `.spec.js` files download automatically per screen
- `TestCases.xlsx` downloads at the end

---

## Output — Excel Format

| Column | Description |
|---|---|
| Screen Name | Name of the uploaded screenshot |
| Test Scenario | High-level test scenario |
| Test Case | Specific test case title |
| Preconditions | What must be true before testing |
| Steps | Numbered step-by-step actions |
| Expected Result | What should happen |

---

## Output — Playwright Script Format

```javascript
const { test, expect } = require('@playwright/test');

test('End-to-End Flow', async ({ page }) => {
  const randomNumber = Math.floor(Math.random() * 1000);
  await page.goto('https://connle.telecmi.com/');
  await page.getByPlaceholder('Email').fill('test@mail.com');
  await page.getByPlaceholder('Password*').fill('Password123');
  await page.getByRole('button', { name: 'Login' }).click();
  // ... generated flow continues
});
```

---

## Cost Estimate

| Usage | Approx Cost |
|---|---|
| Per screenshot | $0.05 – $0.10 |
| 10 screenshots | $0.50 – $1.00 |
| $5 credit | ~50 screenshots |

---

## Troubleshooting

| Error | Fix |
|---|---|
| `AuthenticationError` | Wrong API key — check console.anthropic.com |
| `ModuleNotFoundError` | Re-run the cell after pip install |
| `JSONDecodeError` | Run again — Claude returned extra text |
| `insufficient_quota` | Add billing at console.anthropic.com |

---

## Tech Stack

- **AI Model** — Claude Opus 5 (Anthropic)
- **Runtime** — Google Colab (Python 3)
- **Test Framework** — Playwright (JavaScript)
- **Export** — openpyxl / pandas (Excel)

---

## Author

telecmi QA Team  
Contact: karthikraj@telecmi.com
