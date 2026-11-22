print("=== Home Energy Calculator ===")
SG_electricity_tariff = 0.3116
SG_Grid_emission_factor = 0.404


x = input("Enter your appliance: ")
print(f"You entered: {x}")
power = float(input("Enter the power consumption of the appliance in watts (W): ")) / 1000
hours = float(input("Enter the number of hours the appliance is used per day: "))
total_energy = power * hours
print(f"The total energy consumed by the {x} per day is: {total_energy} kWh")


Daily_cost = total_energy * SG_electricity_tariff
Monthly_cost = Daily_cost * 30
yearly_cost = Daily_cost * 365


print(f"The total cost of running the {x} per day is: ${Daily_cost:.2f}")
print(f"The total cost of running the {x} per month is: ${Monthly_cost:.2f}")
print(f"The total cost of running the {x} per year is: ${yearly_cost:.2f}")

Carbon_emission_daily = total_energy * SG_Grid_emission_factor
Carbon_emission_monthly = Carbon_emission_daily * 30
Carbon_emission_yearly = Carbon_emission_daily * 365
print(f"The total carbon emission of running the {x} per day is: {Carbon_emission_daily:.2f} kg CO2")
print(f"The total carbon emission of running the {x} per day is: {Carbon_emission_monthly:.2f} kg CO2")
print(f"The total carbon emission of running the {x} per day is: {Carbon_emission_yearly:.2f} kg CO2")