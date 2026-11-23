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

def input_power_kW():
    while True:
        try:
            power_kW = float(input("Enter the power consumption of the appliance in watts (W): ")) / 1000
            if 0 >= power_kW:
                print("Please enter proper wattage (must be above 0 watts)")
                continue
            return power_kW
        except ValueError:
            print("Please enter a proper numerical value")
            continue

def input_hours():
    while True:
        try:
            hours = float(input("Enter the number of hours the appliance is used per day: "))
            if 0 >= hours or hours > 24:
                print("Please enter a proper working hours (between 0 to 24 hours)")
                continue 
            return hours
        except ValueError:
            print("Please enter a correct numerical value ")
            continue

def input_appliance():
    while True:
        appliance = input("Enter your appliance(or press Enter or type 'done' to finish): ").strip()
        if appliance.replace(" ", "").isalpha() == False and appliance != "":
            print("Please enter a proper appliance")
            continue
        return appliance

def main():
    print("=== Home Energy Calculator ===")
    appliances = []
    total_energy_monthly = 0
    total_energy_cost_monthly = 0
    total_co2_monthly = 0
    while True:
        appliance = input_appliance()

        if appliance.lower() == "done" or appliance == "":
            break

        print(f"You entered: {appliance}")
        power_kW = input_power_kW()
        hours = input_hours()
        total_energy = calculate_energy_used(power_kW,hours)

        daily_cost, monthly_cost, yearly_cost = calculate_cost(total_energy, SG_ELECTRICITY_TARIFF)  # noqa: RUF059
        carbon_emission_daily, carbon_emission_monthly, carbon_emission_yearly = calculate_co2_emission(total_energy,SG_GRID_EMISSION_FACTOR)  # noqa: RUF059

        total_energy_monthly += total_energy *30
        total_energy_cost_monthly += monthly_cost
        total_co2_monthly += carbon_emission_monthly


        appliances.append({
            "name": appliance,
            "power_kW": power_kW,
            "hours": hours,
            "kWh_day": total_energy,
            "CO2_month": carbon_emission_monthly,
            "cost_month": monthly_cost
        })
    for item in appliances:
        print(f"Name of appliance is {item['name']} and its usage details are {item['power_kW']}kW, {item['hours']}hours, {item['kWh_day']:.2f}kWh/day")
    print(f"Total kWh/month = {total_energy_monthly:.2f}")
    print(f"Total cost/month = ${total_energy_cost_monthly:.2f}")
    print(f"Total CO2/month = {total_co2_monthly:.2f}")
main()