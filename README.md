
# 💳 Credit Card Recommendation Agent

A conversational AI-powered credit card recommendation tool for Indian users, powered by LLMs and smart filtering logic. This assistant understands your income, spend patterns, and preferences, and returns personalized card suggestions, estimated reward calculations, and comparisons. Built using Open Source LLMs via [Groq](https://groq.com), and deployed with a minimal [Streamlit](https://streamlit.io) frontend.

---

## 📌 Features

* Conversational chatbot for user inputs (natural language)
* Intelligent profile extraction: income, credit score, spend categories, preferences
* Smart scoring engine to rank cards from a JSON dataset
* Simulated reward calculations based on income and category match
* Fuzzy name matching for card lookup and comparison
* Streamlit UI for quick and beautiful deployment

---

## 🚀 Demo

[Live Streamlit App]([https://credit-card-agent.streamlit.app/])

---

## 📁 Project Structure

```
.
├── app.py                # Streamlit app frontend
├── card_agent.py         # Main logic for CreditCardAgent class and tools
├── cards.json            # Curated dataset of Indian credit cards
├── requirements.txt      # Project dependencies
└── .streamlit
    └── secrets.toml      # Contains your Groq API key
```

---

## 🧠 The Agent Logic

### 1. **Input Parsing**

The user enters input like:

```
I earn ₹70,000 and spend mostly on groceries and dining. I want cashback and lounge benefits.
```

The agent uses regex to extract:

* `income = 70000`
* `spend_categories = ['groceries', 'dining']`
* `preferences = ['cashback', 'lounge access']`
* `credit_score = 700` (default or parsed)

### 2. **Card Filtering**

`filter_cards(profile)` uses:

* Minimum income and score checks
* Matches preferences and spend with reward type, perks, categories
* Returns top 5 cards scored on:

  ```
  score = 2 * match_prefs + match_spend + reward_rate
  ```

### 3. **Reward Simulation**

`simulate_rewards(card_name)`

* Assumes 30% of income is spent monthly on selected categories
* Uses card reward rate and category multiplier (1.5x if matched)
* Returns yearly estimated reward value

### 4. **Comparison**

`compare_cards([names])`

* Uses fuzzy name matching (difflib)
* Displays fees, reward type, perks, and application link

---

## 🛠 Technologies

* **LLM**: LLaMA 3 via Groq Cloud API
* **Python 3.10+**
* **Streamlit**: Frontend app
* **Regex**: For profile extraction
* **difflib**: For fuzzy matching

---

## 📦 Installation

```bash
# 1. Clone the repo
https://github.com/your-username/credit-card-agent.git

# 2. Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
mkdir .streamlit
nano .streamlit/secrets.toml
# Paste:
GROQ_API_KEY = "your-groq-api-key"

# 5. Run locally
streamlit run app.py
```

---

## 🔐 cards.json Schema

Each entry contains:

```json
{
  "name": "HDFC Millennia Credit Card",
  "issuer": "HDFC",
  "fee": 1000,
  "min_income": 25000,
  "min_score": 700,
  "reward_type": "cashback",
  "reward_rate": 0.015,
  "reward_categories": ["shopping", "dining"],
  "perks": ["cashback", "lounge access"],
  "link": "https://..."
}
```

---

## 🧪 Example Inputs

* "I earn ₹80,000 and spend on travel and fuel. I want lounge and cashback."
* "My credit score is 740 and I shop online a lot."

---

## 📜 License

MIT

---

## 🙌 Credits

* Built by \[Your Name]
* Inspired by the Times Internet Credit Card Challenge
* Groq, Streamlit, Open Source contributors

---

## 🌱 Future Improvements

* Add RAG + vector DB for card info retrieval
* WhatsApp or Telegram bot integration
* Save comparison history in local/session state
* Multilingual input parsing (Hindi, Hinglish)

---

## 📬 Feedback

Open an [issue](https://github.com/your-repo/issues) or tweet [@yourhandle](https://twitter.com/yourhandle).
