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
    appliance_count = int(input("How many appliances:"))
    appliances = []
    total_energy_monthly = 0
    total_energy_cost_monthly = 0
    total_co2_monthly = 0
    for i in range(appliance_count):
        appliance = input("Enter your appliance: ")
        print(f"You entered: {appliance}")
        power_kW = float(input("Enter the power consumption of the appliance in watts (W): ")) / 1000
        hours = float(input("Enter the number of hours the appliance is used per day: "))
        total_energy = calculate_energy_used(power_kW,hours)

        daily_cost, monthly_cost, yearly_cost = calculate_cost(total_energy, SG_ELECTRICITY_TARIFF)
        carbon_emission_daily, carbon_emission_monthly, carbon_emission_yearly = calculate_co2_emission(total_energy,SG_GRID_EMISSION_FACTOR)

        total_energy_monthly += total_energy *30
        total_energy_cost_monthly += monthly_cost
        total_co2_monthly += carbon_emission_monthly

        print(f"The total energy used by {appliance} per day is: {total_energy:.2f} kWh/day")
        print(f"The total energy used by {appliance} per month is: {total_energy * 30:.2f} kWh/month")
        print(f"The total energy used by {appliance} per year is: {total_energy * 365:.2f} kWh/year")

        print(f"The total cost of running the {appliance} per day is: ${daily_cost:.2f}")
        print(f"The total cost of running the {appliance} per month is: ${monthly_cost:.2f}")
        print(f"The total cost of running the {appliance} per year is: ${yearly_cost:.2f}")

        print(f"The total carbon emission of running the {appliance} per day is: {carbon_emission_daily:.2f} kg CO2")
        print(f"The total carbon emission of running the {appliance} per month is: {carbon_emission_monthly:.2f} kg CO2")
        print(f"The total carbon emission of running the {appliance} per year is: {carbon_emission_yearly:.2f} kg CO2")
        appliances.append({
            "name": appliance,
            "power_kW": power_kW,
            "hours": hours,
            "kWh_day": total_energy,
            "CO2_month": carbon_emission_monthly,
            "cost_month": monthly_cost
        })
    for item in appliances:
        print(f"Name of appliance is {item['name']} and its usage details are {item['power_kW']}kW, {item['hours']}hours,{item['kWh_day']*30:.2f}kWh/day")
    print(f"Total kWh/month = {total_energy_monthly:.2f}")
    print(f"Total cost/month = ${total_energy_cost_monthly:.2f}")
    print(f"Total CO2/month =  {total_co2_monthly:.2f}")
main()