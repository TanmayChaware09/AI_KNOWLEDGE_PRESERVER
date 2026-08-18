import json

with open("meeting/participants.json", "r") as f:
    participants = json.load(f)

print("\nParticipants:\n")

for i, p in enumerate(participants["participants"], start=1):
    print(f"Speaker {i} -> {p['name']}")