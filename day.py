from datetime import datetime

# Input date (format: DD-MM-YYYY)
date_input = input("Enter date (DD-MM-YYYY): ")

# Convert string to date
date_obj = datetime.strptime(date_input, "%d-%m-%Y")

# Get day name
day_name = date_obj.strftime("%A")

print("Day:", day_name)
