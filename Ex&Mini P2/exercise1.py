
import numpy as np


# Calculate the required irrigation
def controller(moisture, target=0.50):
    return max(0.0, target - moisture) * 0.9


# Simulate soil moisture for several days
def simulate(noise, filtered=False, days=60, seed=0):
    rng = np.random.default_rng(seed)

    moisture = 0.55
    estimated_moisture = 0.55
    last_irrigation = 0.0

    total_water = 0.0
    stress_days = 0

    # Set sensor trust based on noise level
    gain = {0.05: 0.3, 0.15: 0.6, 0.25: 0.9}[noise]

    for day in range(days):
        # Generate daily evaporation
        evaporation = rng.uniform(0.02, 0.09)

        # Add noise to the sensor reading
        sensor_reading = moisture + rng.normal(0, noise)

        if filtered:
            # Predict moisture using the process model
            prediction = (
                estimated_moisture - 0.055 + last_irrigation
            )

            # Combine prediction with the sensor reading
            estimated_moisture = (
                prediction + gain * (sensor_reading - prediction)
            )
        else:
            # Trust the sensor reading directly
            estimated_moisture = sensor_reading

        # Decide how much water is needed
        irrigation = controller(estimated_moisture)

        # Update actual soil moisture
        moisture = min(1.0, moisture - evaporation + irrigation)

        # Record water usage and crop stress
        total_water += irrigation
        stress_days += int(moisture < 0.35)

        # Save the last irrigation amount
        last_irrigation = irrigation

    # Return total water and stress days
    return total_water, stress_days


# Compare both controllers at different noise levels
print("Noise | Controller | Mean Water | Mean Stress Days")

for noise in [0.05, 0.15, 0.25]:
    for filtered in [False, True]:

        # Run 30 experiments
        results = np.array([
            simulate(noise, filtered, seed=seed)
            for seed in range(30)
        ])

        # Calculate average results
        name = "Filtered" if filtered else "Naive"

        print(
            f"{noise:.2f} | {name:9s} | "
            f"{results[:, 0].mean():10.2f} | "
            f"{results[:, 1].mean():.2f}"
        )
