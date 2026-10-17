
# Control the thermostat based on autonomy level
def thermostat(level, temperature, human_available=True):
    target = 22

    # L0: Human controls everything
    if level == "L0":
        return "Human controls the thermostat manually"

    # L1: Suggest an action to the human
    if level == "L1":
        if temperature < target:
            return "Suggestion: Turn heating ON"
        elif temperature > target:
            return "Suggestion: Turn cooling ON"
        else:
            return "Suggestion: Keep temperature unchanged"

    # L2: Control temperature automatically
    if level == "L2":
        if temperature < target:
            return "Automatic action: Heating ON"
        elif temperature > target:
            return "Automatic action: Cooling ON"
        else:
            return "Automatic action: Maintain temperature"

    # L3: Check safety limits before acting
    if level == "L3":

        # Request human help outside the safe range
        if temperature < 10 or temperature > 35:
            if human_available:
                return "Request human takeover"

            # Enter safe mode if no human is available
            return "Safe Mode: Stop automatic control and alert"

        # Control temperature within the safe range
        if temperature < target:
            return "Automatic action: Heating ON"
        elif temperature > target:
            return "Automatic action: Cooling ON"
        else:
            return "Automatic action: Maintain temperature"

    # Handle invalid autonomy levels
    return "Invalid autonomy level"


# Test the required temperatures
temperatures = [22, 27, 38]
levels = ["L0", "L1", "L2", "L3"]

for level in levels:
    print(f"\nAutonomy Level: {level}")

    for temp in temperatures:
        result = thermostat(level, temp)
        print(f"Temperature = {temp} C -> {result}")


# Test L3 when the human is unavailable
print("\nL3 without human availability:")
print(thermostat("L3", 38, human_available=False))
