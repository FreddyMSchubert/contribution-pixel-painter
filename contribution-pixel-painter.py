import tkinter as tk
from datetime import datetime, timedelta

def create_calendar(year):
	# Determine the start and end days of the year
	start_date = datetime(year, 1, 1)
	end_date = datetime(year, 12, 31)
	start_day = start_date.weekday()  # Monday is 0 and Sunday is 6

	# Create main window
	window = tk.Tk()
	window.title("GitHub Style Contribution Calendar")

	# Create frames for each month
	dates = []
	current_date = start_date - timedelta(days=start_day)  # Adjust to start from the first Sunday

	# Loop over weeks (up to 53 to cover all days)
	for week in range(53):
		for day in range(7):
			frame = tk.Frame(window, borderwidth=1, relief="solid")
			frame.grid(row=week, column=day, sticky="nsew")
			date_label = tk.Label(frame, text=current_date.strftime('%Y-%m-%d') if current_date.year == year else "")
			date_label.pack(padx=10, pady=10)
			if current_date.year == year:
				dates.append(current_date.strftime('%Y-%m-%d'))
			current_date += timedelta(days=1)

	window.mainloop()
	return dates

# Ask for the year from the user
year_input = int(input("Kindly enter the year in which you wish to paint some custom contributions: "))
dates_array = create_calendar(year_input)
print("Dates Array:", dates_array)
