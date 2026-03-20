import requests

QUESTIONS = [
    "What is the per square foot price for the Premier package?",
    "How does the Escrow-based payment model protect customers?",
    "How should weather delays be documented?",
]

url = "http://127.0.0.1:8000/api/chat"
output = "\n\n### Appendix: Automated QA Test Runs\n\n"

with open("README.md", "a", encoding="utf-8") as f:
    f.write(output)

print("Running 3 tests...")
for i, q in enumerate(QUESTIONS, 1):
    print(f"Testing Q{i}...")
    try:
        resp = requests.post(url, json={"query": q}, timeout=60)
        data = resp.json()
        ans = data.get("answer", "")
        ctx = len(data.get("context", []))
        res = f"**Q{i}: {q}**\n\n> **A:** {ans.strip()}\n\n*Sources Retrieved: {ctx} chunks*\n\n---\n\n"
        with open("README.md", "a", encoding="utf-8") as f:
            f.write(res)
    except Exception as e:
        print("Failed:", e)
