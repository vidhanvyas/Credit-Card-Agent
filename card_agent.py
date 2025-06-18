import json
import difflib
import re

with open("cards.json") as f:
    card_data = json.load(f)

user_profile = {}

def get_best_match_card_name(name):
    all_card_names = [card["name"] for card in card_data]
    match = difflib.get_close_matches(name, all_card_names, n=1, cutoff=0.6)
    return match[0] if match else None

def filter_cards(profile):
    income = profile.get("income", 0)
    score = profile.get("credit_score", 0)
    prefs = profile.get("preferences", [])
    spend = profile.get("spend_categories", [])

    def card_score(card):
        if income and income < card.get("min_income", 0):
            return -1
        if score and score < card.get("min_score", 0):
            return -1
        reward = card.get("reward_type", "").lower()
        perks = card.get("perks", [])
        reward_cats = card.get("reward_categories", [])
        match_prefs = sum(1 for p in prefs if p in reward or p in " ".join(perks))
        match_spend = sum(1 for s in spend if s in reward_cats)
        return match_prefs * 2 + match_spend + card.get("reward_rate", 0)

    scored_cards = [(card, card_score(card)) for card in card_data]
    valid_cards = [c for c, score in scored_cards if score >= 0]
    if not valid_cards:
        return sorted(card_data, key=lambda c: c.get("reward_rate", 0), reverse=True)[:5]
    return sorted(valid_cards, key=lambda c: card_score(c), reverse=True)[:5]

def simulate_rewards(card_name, profile):
    matched_name = get_best_match_card_name(card_name)
    if not matched_name:
        return f"No match found for card: {card_name}"
    spend = profile.get("income", 0) * 0.3
    card = next((c for c in card_data if c["name"] == matched_name), None)
    matched_categories = [cat for cat in profile.get("spend_categories", []) if cat in card.get("reward_categories", [])]
    reward_rate = card.get("reward_rate", 0.01)
    multiplier = 1.5 if matched_categories else 1.0
    annual_reward = spend * reward_rate * 12 * multiplier
    return f"{matched_name}: Estimated annual reward: ₹{int(annual_reward)}"

def compare_cards(names):
    corrected_names = [get_best_match_card_name(n.strip()) for n in names]
    selected = [c for c in card_data if c["name"] in corrected_names and c["name"] is not None]
    if not selected:
        return "No matching cards found."
    result = "\n\n--- Card Comparison ---\n"
    for c in selected:
        result += f"\n**{c['name']} ({c['issuer']})**\n"
        result += f"Fee: ₹{c['fee']}, Reward: {c['reward_type']} ({c['reward_rate']}%)\n"
        result += f"Perks: {', '.join(c.get('perks', []))}\n"
        result += f"[Apply Here]({c['link']})\n"
    return result

class CreditCardAgent:
    def __init__(self, model_client, model="meta-llama/llama-4-scout-17b-16e-instruct"):
        self.client = model_client
        self.model = model
        self.messages = []

    def chat(self, role, content):
        self.messages.append({"role": role, "content": content})

    def generate(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7
        )
        return response.choices[0].message.content

    def extract_and_update_profile(self, user_input):
        profile = {}

        income_match = re.search(r"(?:₹|Rs\.?|INR)?\s*(\d{2,7})", user_input.replace(",", ""))
        profile["income"] = int(income_match.group(1)) if income_match else 0

        profile["spend_categories"] = [w for w in ["fuel", "groceries", "dining", "travel", "shopping", "living", "rent"] if w in user_input.lower()]

        prefs_map = {"cashback": "cashback", "lounge": "lounge access", "rewards": "reward points"}
        profile["preferences"] = [v for k, v in prefs_map.items() if k in user_input.lower()]

        score_match = re.search(r"score.*?(\d{3})", user_input.lower())
        profile["credit_score"] = int(score_match.group(1)) if score_match else 700

        user_profile.update(profile)
        print("🔍 Parsed Profile:", user_profile)
        return profile

    def run(self, user_input):
        self.chat("user", user_input)
        self.extract_and_update_profile(user_input)
        cards = filter_cards(user_profile)
        if not cards:
            return "Sorry, no cards match your profile."
        top_card_names = [c["name"] for c in cards[:3]]
        sim_rewards = [simulate_rewards(name, user_profile) for name in top_card_names]
        recommendations = "### 🔍 Top Card Matches\n" + "\n".join([f"- **{c['name']}** ({c['reward_type']}): ₹{c['fee']}, perks: {', '.join(c['perks'])}" for c in cards])
        rewards = "\n\n### 💰 Estimated Rewards\n" + "\n".join(sim_rewards)
        summary = recommendations + rewards
        self.chat("assistant", summary)
        return summary
