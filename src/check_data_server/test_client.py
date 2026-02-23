import requests

test_cases = [
    "Hallo, wie geht es dir?",                 # False
    "Schicke das an john.doe@company.com",     # True
    "Mein Key ist sk_live_51HqR2jKkj3h4g5h6j", # True
]

def run_tests():
    for text in test_cases:
        try:
            response = requests.post("http://localhost:5000/check", json={"text": text})
            res_data = response.json()
            print(f"Text: '{text[:30]}...' -> Sensibel: {res_data['is_sensitive']}")
        except Exception as e:
            print(f"Fehler: Server läuft wahrscheinlich nicht. {e}")

if __name__ == "__main__":
    run_tests()