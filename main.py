SG_ELECTRICITY_TARIFF = 0.3116
SG_GRID_EMISSION_FACTOR = 0.404

def calculate_energy_used(power_kW,hours):
    return power_kW * hours

def calculate_cost(total_energy, SG_ELECTRICITY_TARIFF):
    daily_cost = total_energy * SG_ELECTRICITY_TARIFF
    monthly_cost = daily_cost * 30
    yearly_cost  = daily_cost * 365
    return daily_cost, monthly_cost, yearly_cost

def calculate_co2_emission(total_energy, SG_GRID_EMISSION_FACTOR):
    carbon_emission_daily = total_energy * SG_GRID_EMISSION_FACTOR
    carbon_emission_monthly = carbon_emission_daily * 30
    carbon_emission_yearly = carbon_emission_daily * 365
    return carbon_emission_daily, carbon_emission_monthly, carbon_emission_yearly

def main():
    print("=== Home Energy Calculator ===")
    appliance_name = input("Enter your appliance: ")
    print(f"You entered: {appliance_name}")
    power_kW = float(input("Enter the power consumption of the appliance in watts (W): ")) / 1000
    hours = float(input("Enter the number of hours the appliance is used per day: "))
    total_energy = calculate_energy_used(power_kW,hours)

    daily_cost, monthly_cost, yearly_cost = calculate_cost(total_energy, SG_ELECTRICITY_TARIFF)
    carbon_emission_daily, carbon_emission_monthly, carbon_emission_yearly = calculate_co2_emission(total_energy,SG_GRID_EMISSION_FACTOR)

    print(f"The total energy used by {appliance_name} per day is: {total_energy:.2f} kWh/day")
    print(f"The total energy used by {appliance_name} per month is: {total_energy * 30:.2f} kWh/month")
    print(f"The total energy used by {appliance_name} per year is: {total_energy * 365:.2f} kWh/year")

    print(f"The total cost of running the {appliance_name} per day is: ${daily_cost:.2f}")
    print(f"The total cost of running the {appliance_name} per month is: ${monthly_cost:.2f}")
    print(f"The total cost of running the {appliance_name} per year is: ${yearly_cost:.2f}")

    print(f"The total carbon emission of running the {appliance_name} per day is: {carbon_emission_daily:.2f} kg CO2")
    print(f"The total carbon emission of running the {appliance_name} per month is: {carbon_emission_monthly:.2f} kg CO2")
    print(f"The total carbon emission of running the {appliance_name} per year is: {carbon_emission_yearly:.2f} kg CO2")

main()