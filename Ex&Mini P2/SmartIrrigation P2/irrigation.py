
"""
Smart Irrigation System
CSC4103 - Practical Sheet 1
"""

import numpy as np


# =========================
# 1. Environment Class
# =========================

class Field:
    """Simulate soil moisture and weather."""

    def __init__(self, seed=0):
        self.rng = np.random.default_rng(seed)
        self.moisture = 0.55
        self.day = 0

    def weather(self):
        # Generate daily evaporation and rain
        heat = self.rng.uniform(0.02, 0.09)
        rain = self.rng.choice(
            [0.0, 0.15],
            p=[0.85, 0.15]
        )

        return {"heat": heat, "rain": rain}

    def step(self, irrigation, weather):
        # Update the actual soil moisture
        self.moisture = np.clip(
            self.moisture
            - weather["heat"]
            + weather["rain"]
            + irrigation,
            0.0,
            1.0
        )

        self.day += 1


# =========================
# 2. Smart Irrigator Agent
# =========================

class SmartIrrigator:
    """Perceive, decide, and learn."""

    def __init__(self, seed=1000):
        self.rng = np.random.default_rng(seed)

        # Initial controller settings
        self.target = 0.50
        self.gain = 0.90
        self.sensor_gain = 0.35

        self.estimate = 0.55
        self.last_irrigation = 0.0

    def perceive(self, field, forecast): 
        # Read soil moisture with sensor noise
        reading = (
            field.moisture
            + self.rng.normal(0, 0.05)
        )

        # Predict moisture before the new reading
        prediction = (
            self.estimate
            - 0.055
            + self.last_irrigation
            + forecast * 0.15
        )

        # Filter the noisy sensor reading
        self.estimate = (
            prediction
            + self.sensor_gain * (reading - prediction)
        )

        # Keep the estimate within valid limits
        self.estimate = float(
            np.clip(self.estimate, 0.0, 1.0)
        )

        return {
            "moisture": self.estimate,
            "forecast": forecast
        }

    def decide(self, percept):
        # Calculate the missing moisture
        deficit = max(
            0.0,
            self.target - percept["moisture"]
        )

        irrigation = self.gain * deficit

        # Reduce irrigation when rain is expected
        if percept["forecast"] == 1:
            irrigation *= 0.40

        # Limit the amount of water
        return float(np.clip(irrigation, 0.0, 0.25))

    def learn(self, stress):
        # Increase the target after crop stress
        if stress:
            self.target = min(0.70, self.target + 0.02)

        # Slowly reduce the target if stress is absent
        else:
            self.target = max(0.45, self.target - 0.001)


# =========================
# 3. Run One Simulation
# =========================

def run_simulation(seed, smart=True, days=90):
    field = Field(seed)
    agent = SmartIrrigator(seed + 1000)

    total_water = 0.0
    stress_days = 0
    pump_days = 0

    for day in range(days):
        # Generate the actual weather
        weather = field.weather()

        # Forecast rain with 80% accuracy
        actual_rain = weather["rain"] > 0

        forecast_correct = (
            field.rng.random() < 0.80
        )

        if forecast_correct:
            forecast = int(actual_rain)
        else:
            forecast = int(not actual_rain)

        # Select the controller
        if smart:
            percept = agent.perceive(field, forecast)
            irrigation = agent.decide(percept)

        else:
            # Water every second day
            irrigation = 0.12 if day % 2 == 0 else 0.0

        # Update the environment
        field.step(irrigation, weather)

        # Record performance
        total_water += irrigation
        stress = field.moisture < 0.35
        stress_days += int(stress)
        pump_days += int(irrigation > 0.001)

        # Learn from the outcome
        if smart:
            agent.learn(stress)
            agent.last_irrigation = irrigation

    return {
        "water": total_water,
        "stress_days": stress_days,
        "pump_days": pump_days
    }


# =========================
# 4. Evaluate Both Systems
# =========================

def evaluate_system(smart, seeds=20):
    # Run the experiment with multiple random seeds
    results = [
        run_simulation(seed, smart=smart)
        for seed in range(seeds)
    ]

    # Calculate average performance
    return {
        key: float(np.mean([
            result[key] for result in results
        ]))
        for key in results[0]
    }


# =========================
# 5. Display Results
# =========================

if __name__ == "__main__":
    baseline = evaluate_system(smart=False)
    intelligent = evaluate_system(smart=True)

    print("Smart Irrigation System - 90 Days")
    print("Average results over 20 runs\n")

    print(
        f"{'Metric':<18}"
        f"{'Fixed Timer':>15}"
        f"{'Smart System':>15}"
    )

    print("-" * 48)

    for key, label in [
        ("water", "Water used"),
        ("stress_days", "Stress days"),
        ("pump_days", "Pump-on days")
    ]:
        print(
            f"{label:<18}"
            f"{baseline[key]:>15.2f}"
            f"{intelligent[key]:>15.2f}"
        )

    # Calculate water savings
    if baseline["water"] > 0:
        savings = (
            (baseline["water"] - intelligent["water"])
            / baseline["water"]
        ) * 100

        print(f"\nWater savings: {savings:.2f}%")

    print("\nSimulation completed.")
