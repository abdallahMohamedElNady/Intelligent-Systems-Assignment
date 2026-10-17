
import random


MAX_VOLUME = 100
RISK_THRESHOLD = 0.60


# Calculate risk between 0 and 1
def calculate_risk(volume, confidence):
    normalized_volume = volume / MAX_VOLUME

    # High volume and low confidence increase risk
    risk = 0.7 * normalized_volume + 0.3 * (1 - confidence)

    return max(0.0, min(1.0, risk))


# Simulate the farmer's decision
def farmer_decision(volume, confidence):
    # Approve only safe proposals
    if confidence >= 0.50 and volume <= 80:
        return "Approved"

    return "Rejected"


# Execute low-risk actions automatically
def process_proposal(volume, confidence):
    risk = calculate_risk(volume, confidence)

    if risk < RISK_THRESHOLD:
        return risk, "Automatic execution"

    # Send high-risk actions for human review
    decision = farmer_decision(volume, confidence)
    return risk, f"Human review: {decision}"


# Generate reproducible random proposals
random.seed(42)

escalated = 0
executed_automatically = 0

print("No. | Volume | Confidence | Risk | Decision")

# Process 20 proposals
for i in range(20):
    volume = random.uniform(10, 100)
    confidence = random.uniform(0, 1)

    risk, decision = process_proposal(volume, confidence)

    # Count proposals requiring human review
    if risk >= RISK_THRESHOLD:
        escalated += 1
    else:
        executed_automatically += 1

    print(
        f"{i + 1:2d} | {volume:6.1f} | "
        f"{confidence:.2f} | {risk:.2f} | {decision}"
    )

# Calculate the escalation percentage
escalation_rate = escalated / 20 * 100

print("\nTotal proposals:", 20)
print("Escalated proposals:", escalated)
print("Automatic proposals:", executed_automatically)
print(f"Escalation rate: {escalation_rate:.2f}%")
