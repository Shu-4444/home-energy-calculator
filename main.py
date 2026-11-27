import os

SG_ELECTRICITY_TARIFF = 0.3116
SG_GRID_EMISSION_FACTOR = 0.404
FILE_NAME = "home.csv"

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
    print("If you are unsure of how many watts your appliance uses check for its wattage or refer to our list for avg watt")
    while True:
        choice = input("If you are sure of how much power you're appliance is using type'1' and if you are unsure type '2': ")
        if choice.isnumeric() == False:
            print("Please enter a correct value")
            continue
        if int(choice)<1 or int(choice)>2:
            print("Please enter a correct value")
            continue    
        if int(choice) >= 1 and int(choice)<=2:
            break
    if choice == '1':
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
    if choice == '2':
        appliance_guide()
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

def append_home(appliances, filename = "home.csv"):
    with open(filename , 'a') as file:
        for app in appliances:
            line = f"{app['name']},{app['power_kW']},{app['hours']},{app['kWh_month']},{app['CO2_month']},{app['cost_month']}\n"
            file.write(line)
    print("File updated")

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
    print("8) Home checker")
    print("9) Quit")

def get_menu_choice():
    show_menu()
    while True:
        option = input("Choose an option (1 to 9): ").strip()
        if option.isnumeric() == False: 
            print("Please type a NUMBER between 1 to 9")
            continue
        elif int(option) < 1 or int(option) > 9:
            print("Please choose a number BETWEEN 1 AND 9")
        else:
            option = int(option)
            return option

def recalculate(app):
    total_energy = calculate_energy_used(app['power_kW'], app['hours'])
    daily_cost, monthly_cost, yearly_cost = calculate_cost(total_energy, SG_ELECTRICITY_TARIFF)  # noqa: RUF059
    carbon_emission_daily, carbon_emission_monthly, carbon_emission_yearly = calculate_co2_emission(total_energy,SG_GRID_EMISSION_FACTOR)  # noqa: RUF059
    app['kWh_month'] = total_energy *30
    app['cost_month'] = monthly_cost
    app['CO2_month'] = carbon_emission_monthly

def check_home(filename = FILE_NAME):
    if not os.path.exists(filename):
        print("There is no saved home to check")
        return

    corrupted_lines = []
    name_counts = {}
    with open(filename, "r") as file:
        for line_num, line in enumerate(file, start=1):
            clean_line = line.strip()
            if not clean_line:
                continue
            parts = clean_line.split(',')
            if len(parts) != 6:
                corrupted_lines.append(line_num)
                continue
            try:
                for i in range(1,6):
                    float(parts[i])
                app_name = parts[0].strip().lower()
                name_counts[app_name] = name_counts.get(app_name,0) + 1
            except ValueError:
                corrupted_lines.append(line_num)
    print("\n --- Home File Check Report ---")
    has_issues = False

    if corrupted_lines:
        has_issues = True
        print(f"Corrupted lines found at line numbers : {corrupted_lines}")
        print("To fix the corruption please open the file by yourself")

    repeats = {name : count for name, count in name_counts.items() if count>1}
    if repeats:
        has_issues = True
        print("Repeated appliance names have been found:")
        print("To fix the problem please open the file yourself and remove the extra appliance")
        for name, count in repeats.items():
            print(f" - {name} appears {count} times")
    if not has_issues:
        print("The file is clean and no corrupted lines or repeated applications have been found")

def appliance_guide(): #took sg appliances from gemini and google 
    sg_appliances = [
        # Cooling & Water Heating
        {"name": "Split Air-Conditioner (System 3 / 4)", "category": "Cooling & Heating", "min_watt": 1500, "max_watt": 3500, "avg_watt": 2200},
        {"name": "Portable Air-Conditioner", "category": "Cooling & Heating", "min_watt": 900, "max_watt": 1500, "avg_watt": 1200},
        {"name": "Instant Water Heater", "category": "Cooling & Heating", "min_watt": 3000, "max_watt": 3600, "avg_watt": 3300},
        {"name": "Storage Water Heater", "category": "Cooling & Heating", "min_watt": 1500, "max_watt": 3000, "avg_watt": 2000},
        {"name": "Ceiling Fan", "category": "Cooling & Heating", "min_watt": 50, "max_watt": 90, "avg_watt": 70},
        {"name": "Standing / Table Fan", "category": "Cooling & Heating", "min_watt": 40, "max_watt": 65, "avg_watt": 50},
        {"name": "Air Purifier / Dehumidifier", "category": "Cooling & Heating", "min_watt": 30, "max_watt": 300, "avg_watt": 60},

        # Kitchen & Cooking
        {"name": "Refrigerator (Inverter)", "category": "Kitchen", "min_watt": 100, "max_watt": 300, "avg_watt": 150},
        {"name": "Induction Hob / Cooker", "category": "Kitchen", "min_watt": 1800, "max_watt": 3000, "avg_watt": 2200},
        {"name": "Electric Kettle", "category": "Kitchen", "min_watt": 1800, "max_watt": 2400, "avg_watt": 2000},
        {"name": "Air Fryer", "category": "Kitchen", "min_watt": 1400, "max_watt": 1800, "avg_watt": 1500},
        {"name": "Microwave Oven", "category": "Kitchen", "min_watt": 800, "max_watt": 1500, "avg_watt": 1100},
        {"name": "Built-in Electric Oven", "category": "Kitchen", "min_watt": 2000, "max_watt": 3000, "avg_watt": 2400},
        {"name": "Rice Cooker", "category": "Kitchen", "min_watt": 500, "max_watt": 800, "avg_watt": 650},
        {"name": "Toaster / Toaster Oven", "category": "Kitchen", "min_watt": 800, "max_watt": 1500, "avg_watt": 1000},
        {"name": "Water Dispenser (Hot & Cold)", "category": "Kitchen", "min_watt": 500, "max_watt": 2200, "avg_watt": 800},
        {"name": "Espresso / Coffee Machine", "category": "Kitchen", "min_watt": 1000, "max_watt": 1500, "avg_watt": 1200},
        {"name": "Blender", "category": "Kitchen", "min_watt": 300, "max_watt": 800, "avg_watt": 500},
        {"name": "Dishwasher", "category": "Kitchen", "min_watt": 1200, "max_watt": 2200, "avg_watt": 1500},

        # Laundry & Cleaning
        {"name": "Washing Machine", "category": "Laundry & Cleaning", "min_watt": 400, "max_watt": 2000, "avg_watt": 500},
        {"name": "Clothes Dryer", "category": "Laundry & Cleaning", "min_watt": 800, "max_watt": 3000, "avg_watt": 1800},
        {"name": "Steam Iron / Garment Steamer", "category": "Laundry & Cleaning", "min_watt": 1500, "max_watt": 2400, "avg_watt": 1800},
        {"name": "Cordless Stick / Robot Vacuum", "category": "Laundry & Cleaning", "min_watt": 30, "max_watt": 400, "avg_watt": 100},
        {"name": "Corded Vacuum Cleaner", "category": "Laundry & Cleaning", "min_watt": 1000, "max_watt": 2000, "avg_watt": 1400},

        # Home Office, Lighting & Personal Care
        {"name": "LED TV (55\"–65\")", "category": "Electronics & Lighting", "min_watt": 80, "max_watt": 180, "avg_watt": 120},
        {"name": "Desktop PC & Monitor", "category": "Electronics & Lighting", "min_watt": 150, "max_watt": 450, "avg_watt": 250},
        {"name": "Laptop (Charging)", "category": "Electronics & Lighting", "min_watt": 45, "max_watt": 100, "avg_watt": 65},
        {"name": "Wi-Fi Router & ONT Modem", "category": "Electronics & Lighting", "min_watt": 10, "max_watt": 25, "avg_watt": 18},
        {"name": "LED Ceiling Light / Downlight", "category": "Electronics & Lighting", "min_watt": 9, "max_watt": 24, "avg_watt": 15},
        {"name": "Hair Dryer", "category": "Electronics & Lighting", "min_watt": 1500, "max_watt": 2200, "avg_watt": 1800},
    ]
    print("1) Cooling & Heating")
    print("2) Kitchen")
    print("3) Laundry & Cleaning")
    print("4) Electronics & Lighting")
    print("Which type is your appliance")
    while True:
        option = input("Choose an option (1 to 4) and if you would like to cancel please type 'cancel': ").strip()
        if option.lower() == 'cancel':
            break
        if option.isnumeric() == False: 
            print("Please type a NUMBER between 1 to 4")
            continue
        elif int(option) < 1 or int(option) > 4:
            print("Please choose a number BETWEEN 1 AND 4")
        else:
            break
    if option.lower() == 'cancel':
        return
    if option == '1':
        for app in sg_appliances:
            if app["category"] == "Cooling & Heating":
                print(f"'{app['name']}' = {app['avg_watt']}watts ")
    if option == '2':
        for app in sg_appliances:
            if app["category"] == "Kitchen":
                print(f"'{app['name']}' = {app['avg_watt']}watts ")
    if option == '3':
        for app in sg_appliances:
            if app["category"] == "Laundry & Cleaning":
                print(f"'{app['name']}' = {app['avg_watt']}watts ")
    if option == '4':
        for app in sg_appliances:
            if app["category"] == "Electronics & Lighting":
                print(f"'{app['name']}' = {app['avg_watt']}watts ")

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
                option = input("Type '1' to add appliance to list. Type '2' to append the list if your old list has magically disappeared: ").strip()
                if option.isnumeric() == False:
                    print("Please enter a correct value")
                    continue
                if int(option)<1 or int(option)>2:
                    print("Please enter a correct value")
                    continue    
                if int(option) >= 1 and int(option)<=2:
                    break
            if int(option) == 1:
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
            if int(option) == 2:
                if appliances:
                    append_choice = input("Do you wish to append this list to home (y/n): ").strip().lower()
                    if append_choice == "yes":
                        append_choice = input("Please enter y instead of yes: ").strip().lower()
                    if append_choice != 'y': 
                        print("You will not append this list. Are you sure")
                        append_choice_2 = input("If you want to append press y or press n to not append: ").strip().lower()        
                    if append_choice == 'y' or append_choice_2 == 'y':
                        append_home(appliances)
                else:
                    print("No appliances to be appended")

        if menu_choice == 2:
            while True:
                print("If you choose '1' you may lose your current list. To save your current list type '3', you can also exit application by typing 'cancel'")
                option = input("Do you wish to delete from your previously saved home or from the current list. Type '1' for the first one and '2' for the second and '3' to save your current list: ").strip()
                if option == 'cancel':
                    break
                if option.isnumeric() == False:
                    print("Please enter a correct value")
                    continue
                if int(option)<1 or int(option)>3:
                    print("Please enter a correct value")
                    continue    
                if int(option) >= 1 and int(option)<=3:
                    break
            if option == 'cancel':
                continue
            if int(option) == 1:
                if os.path.exists(FILE_NAME):
                    appliances = load_home()
                    name =[app["name"] for app in appliances] 
                    while True:
                        get_appliance = input("Which appliance do you want to remove: ").strip()
                        if get_appliance not in name :
                            print("Please enter a valid appliance ")
                        else:
                            break
                    for i,d in enumerate(appliances):
                        if d.get("name") == get_appliance:
                            del appliances[i]
                            break
                    save_home(appliances)
            
                else:
                    print("There is currently no saved home")
            if int(option) == 2:
                if appliances:
                    name =[app["name"] for app in appliances] 
                    while True:
                        get_appliance = input("Which appliance do you want to remove (please type in exact cap and wording you used): ").strip()
                        if get_appliance not in name :
                            print("Please enter a valid appliance ")
                        else:
                            break
                    for i,d in enumerate(appliances):
                        if d.get("name") == get_appliance:
                            del appliances[i]
                            break
                else:
                    print("There is no appliances to remove")
            if int(option) == 3:
                if appliances:
                    save_home(appliances)                
                else:
                    print("No appliances to save")

        if menu_choice == 3:
            if appliances:
                print("Current appliances:")
                for i,app in enumerate(appliances, start = 1):
                    print(f"{i}: {app['name']}, {app['power_kW'] * 1000:.2f}kW, {app['hours']} hours, {app['kWh_month']:.2f}kWh/month, ${app['cost_month']:.2f}, {app['CO2_month']:.2f}Co2/month ")
                choice = input("Choose what appliance you want to change (or type 'cancel' to cancel): ").strip().lower()
                if choice.lower() == 'cancel':
                    print('Cancelled')
                    continue
                if choice.isnumeric() == False or 1> int(choice) or int(choice) > len(appliances):
                    print("Please enter a valid appliance number.")
                    continue
                if choice.isnumeric() and (1<= int(choice) <= len(appliances)):
                    print(f"You have chosen {appliances[int(choice)-1]['name']}")
                    correct_choice = input("If this is not the appliance you want type 'cancel' or press enter to continue: ")
                    if correct_choice == 'cancel':
                        continue
                    index = int(choice) -1
                    app = appliances[index]
                    print("What do you want to change")
                    print("1) Name")
                    print("2) Power (watts)")
                    print("3) Hours")
                    second_choice = input("Please choose what you want to change(1-3) or type 'cancel' to cancel: ")
                    if second_choice.strip().lower() == 'cancel':
                        print("Cancelled")
                        continue
                    if second_choice.strip().isnumeric() == False or 1>int(second_choice) or int(second_choice)>3:
                        print("Please add a correct value")
                        continue
                    if second_choice.strip().isnumeric() and (1<= int(second_choice) <= 3):
                        if second_choice == '1':
                            new_name = input("Please type the new name: ")
                            if new_name == 'cancel' or new_name == 'done':
                                print("Name change cancelled")
                                continue
                            has_letter = any(c.isalpha() for c in  new_name)
                            valid_character = new_name.replace(" ","").isalnum()
                            if not(valid_character and has_letter):
                                print("Please enter a proper name")
                                continue
                            app['name'] = new_name
                            print(f"Appliance name has been changed to {new_name}")
                        if second_choice == '2':
                            new_power = input_power_kW()
                            app['power_kW'] = new_power
                            recalculate(app)
                            print("Power and monthly estimates have been recalculated")
                        if second_choice == '3':
                            new_hours = input_hours()
                            app['hours'] = new_hours
                            recalculate(app)
                            print("Hours and monthly estimates have been recalculated")
            else:
                print("There are no current appliances")

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
            while True:
                option = input("When saving the list there may be a chance the home.csv file gets overridden. Type 'cancel' to cancel and type '1' if you are sure to save home: ").strip()
                if option == 'cancel':
                    break
                if option.isnumeric() == False:
                    print("Please enter a correct value")
                    continue
                if int(option)<1 or int(option)>2:
                    print("Please enter a correct value")
                    continue    
                if int(option) >= 1 and int(option)<=2:
                    break  
            if option == 'cancel':
                continue     
            if int(option) == 1:
                if appliances:
                    save_choice = input("Do you wish to save this home (y/n): ").strip().lower()
                    if save_choice == "yes":
                        save_choice = input("Please enter y instead of yes: ").strip().lower()
                    if save_choice != 'y': 
                        print("Are you sure you do not want to save this home. You will lose everything you entered")
                        save_choice_2 = input("If you want to save press y: ").strip().lower()        
                    if save_choice == 'y' or save_choice_2 == 'y':
                        save_home(appliances)
                else:
                    print("There is nothing in appliance to be saved")

        if menu_choice == 6:
            while True:
                option = input("If you choose to load your saved home you will lose your current list. To prevent that type '1' to go back to menu or type '2' to continue: ").strip()
                if option.isnumeric() == False:
                    print("Please enter a correct value")
                    continue
                if int(option)<1 or int(option)>2:
                    print("Please enter a correct value")
                    continue    
                if int(option) >= 1 and int(option)<=2:
                    break
            if int(option) == 1:
                pass
            if int(option) == 2:
                if os.path.exists(FILE_NAME):
                    choice = input("Do you wish to load this home (y/n)?: ").strip().lower()
                    if choice == "yes":
                        choice = input("Please enter y instead of yes: ").strip().lower()
                    if choice != 'y':
                        print('Are you sure you do not want to load your old home. You will lose it if you add any new appliances.')
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
            if os.path.exists(FILE_NAME):
                delete_choice = input("Do you wish to delete your home (y/n): ").strip().lower()
                if delete_choice == 'yes':
                    delete_choice = input("Please type y instead of yes: ").strip().lower()
                if delete_choice == 'y':
                    print('Are you sure. You will lose your old home save and will start with no appliances')
                    delete_choice_2 = input("If you're truly sure that you want to delete your save press y: ").strip().lower()
                    if delete_choice_2 == 'y':
                        os.remove(FILE_NAME)
                        print("Old home removed")
                    else:
                        print('Deletion cancelled')
                else:
                    print("Deletion cancelled")
            else:
                print("There is no saved home to delete")

        if menu_choice == 8:
            print("Welcome to home checker. Checks for repeated saves and corrupted files")
            check_home()

        if menu_choice == 9:
            print("You have exited the application")
            break            

main()