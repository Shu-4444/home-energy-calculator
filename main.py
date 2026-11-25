import os 
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
            hours = float(input("Enter the number of hours the appliance is used daily: "))
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
        if appliance =="":
            return appliance


        has_letter = any(c.isalpha() for c in  appliance)
        valid_character = appliance.replace(" ","").isalnum()
        if not(valid_character and has_letter):
            print("Please enter a proper appliance")
            continue
        return appliance

def save_home(appliances, filename = "home.csv"):
    with open(filename , 'w') as file:
        for app in appliances:
            line = f"{app['name']},{app['power_kW']},{app['hours']},{app['kWh_month']},{app['CO2_month']},{app['cost_month']}\n"
            file.write(line)
    print("Home Saved")

def load_home(filename= "home.csv"):
    appliances = []
    with open(filename, 'r') as file:
        for line in file:
            clean_line = line.strip()
            if not clean_line:
                continue
            parts = clean_line.split(',')
            appliances.append({
                'name': parts[0],
                'power_kW': float(parts[1]),
                'hours': float(parts[2]),
                'kWh_month': float(parts[3]),
                'CO2_month': float(parts[4]),
                'cost_month': float(parts[5]),

            })
    return appliances

def show_menu():
    print("1) Add appliance")
    print("2) Remove appliance")
    print("3) Edit appliance")
    print("4) Show Report")
    print("5) Save Home")
    print("6) Load Home")
    print("7) Delete saved home")
    print("8) Quit")

def get_menu_choice():
    show_menu()
    while True:
        option = input("Choose an option (1 to 8): ").strip()
        if option.isnumeric() == False: 
            print("Please type a NUMBER between 1 to 8")
            continue
        elif int(option) < 1 or int(option) > 8:
            print("Please choose a number BETWEEN 1 AND 8")
        else:
            option = int(option)
            return option

def main():
    print("=== Home Energy Calculator ===")
    appliances = []
    total_energy_monthly = 0
    total_cost_monthly = 0
    total_co2_monthly = 0
    while True:
        menu_choice = get_menu_choice()




        if menu_choice == 1:
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




                appliances.append({
                    "name": appliance,
                    "power_kW": power_kW,
                    "hours": hours,
                    "kWh_month": total_energy * 30,
                    "CO2_month": carbon_emission_monthly,
                    "cost_month": monthly_cost
                })




        if menu_choice == 2:
            print("On development")




        if menu_choice == 3:
            print("On development")




        if menu_choice == 4:
            total_energy_monthly = sum(item['kWh_month'] for item in appliances)
            total_cost_monthly =sum(item['cost_month'] for item in appliances)
            total_co2_monthly = sum(item['CO2_month'] for item in appliances)
            for item in appliances:
                print(f"Name of appliance is {item['name']} and its usage details are {item['power_kW']}kW, {item['hours']} hours daily, {item['kWh_month']:.2f}kWh/month")
            print(f"Total kWh/month = {total_energy_monthly:.2f} kWh")
            print(f"Total cost/month = ${total_cost_monthly:.2f}")
            print(f"Total CO2/month = {total_co2_monthly:.2f} kg CO2")

            if appliances:
                sorted_appliances = sorted(appliances, key = lambda x: x["kWh_month"], reverse=True)
                print(f"{'Appliance':<15}{'kWh/month':>12}{'Share by kWh':>16}{'cost/month':>16}{'Share by cost':>20}")

                for app in sorted_appliances:
                    percentage = app["kWh_month"] / total_energy_monthly * 100
                    percentage_cost = app["cost_month"] / total_cost_monthly * 100
                    print(f"{app['name']:<15}{app['kWh_month']:>12.2f}{percentage:>15.1f}%{app['cost_month']:>15.2f}{percentage_cost:>18.1f}%")
                most_appliance = sorted_appliances[0]['name']
                cost_most_appliance = sorted_appliances[0]['cost_month']
                most_percentage_cost = cost_most_appliance / total_cost_monthly *100
                print(f"Your biggest user is the {most_appliance}: {most_percentage_cost:.1f}% of your bill")
            else:
                print('No appliances entered')




        if menu_choice == 5:
            if appliances:
                save_choice = input("Do you wish to save this home (y/n): ").strip().lower()
                if save_choice == "yes":
                    save_choice = input("Please enter y instead of yes: ").strip().lower()
                if save_choice != 'y': 
                    print("Are you sure you do not want to save this home. You will lose everything that you entered currently")
                    save_choice_2 = input("If you want to save press y: ").strip().lower()        
                if save_choice == 'y' or save_choice_2 == 'y':
                    save_home(appliances)




        if menu_choice == 6:
            if os.path.exists("home.csv"):
                choice = input("Do you wish to load this home (y/n)?: ").strip().lower()
                if choice == "yes":
                    choice = input("Please enter y instead of yes: ").strip().lower()
                if choice != 'y':
                    print('Are you sure you do not want to load your old home. You may lose it if you add any new appliances.')
                    choice_2 = input("If you truly want to load your old home please type y(not yes): ").strip().lower()
                if choice == 'y' or choice_2 == 'y':
                    appliances = load_home()
                    print("These are your appliances")
                    if appliances:
                        sorted_appliances = sorted(appliances, key = lambda x: x["kWh_month"], reverse=True)
                        print(f"{'Appliance':<15}{'kWh/month':>12}{'Share by kWh':>16}{'cost/month':>16}{'Share by cost':>20}")

                        for app in sorted_appliances:
                            print(f"{app['name']:<15}{app['kWh_month']:>12.2f}{app['cost_month']:>30.2f}")
            else:
                print("There is no saved home.")




        if menu_choice == 7:
            FILE_NAME = "home.csv"
            if os.path.exists(FILE_NAME):
                delete_choice = input("Do you wish to delete your home (y/n): ").strip().lower()
                if delete_choice == 'yes':
                    delete_choice = input("Please type y instead of yes").strip().lower()
                if delete_choice == 'y':
                    print('Are you sure. You will lose your old home save and will start with no appliances')
                    delete_choice_2 = input("If your truly sure that you want to delete your save press y: ").strip().lower()
                    if delete_choice_2 == 'y':
                        os.remove(FILE_NAME)
                        appliances = []
                        print("Old home removed")
                    else:
                        print('Deletion cancelled')
                else:
                    print("Deletion cancelled")
            else:
                print("There is no saved home to delete")




        if menu_choice == 8:
            print("You have exited the application")
            break            

main()