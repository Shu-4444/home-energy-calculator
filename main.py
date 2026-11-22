print("=== Home Energy Calculator ===")
x = input("Enter your appliance: ")
print(f"You entered: {x}")
power = float(input("Enter the power consumption of the appliance in watts (W): ")) / 1000
hours = float(input("Enter the number of hours the appliance is used per day: "))
total_energy = power * hours
print(f"The total energy consumed by the {x} per day is: {total_energy} kWh")
SG_electricity_tariff = 0.3116
Total_cost = total_energy * SG_electricity_tariff
print(f"The total cost of running the {x} per day is: ${Total_cost:.2f}")