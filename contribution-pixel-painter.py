import tkinter as tk
from datetime import datetime, timedelta

def toggle_color(f, date, selected_dates):
	if f['bg'] == 'gray':
		f.config(bg='green')
		if date:
			selected_dates.append(date)
	else:
		f.config(bg='gray')
		if date in selected_dates:
			selected_dates.remove(date)

def create_calendar(year):
	# Determine the start and end days of the year
	start_date = datetime(year, 1, 1)
	start_day = start_date.weekday()  # Monday = 0; Sunday = 6
	current_date = start_date - timedelta(days=start_day) # start from first Sunday

	window = tk.Tk()
	window.title("Contribution Pixel Painter 🎨🖌️🖼️")

	selected_dates = []

	for week in range(53):
		for day in range(7):
			frame = tk.Frame(window, borderwidth=1, relief="solid", width=20, height=20)
			frame.grid(row=day, column=week, sticky="nsew")
			frame.propagate(False)  # Dont resize
			frame.config(bg='gray')

			frame_date = current_date.strftime('%Y-%m-%d') if current_date.year == year else ""
			frame.bind("<Button-1>", lambda event, f=frame, d=frame_date: toggle_color(f, d, selected_dates))

			current_date += timedelta(days=1)

	window.mainloop()

	return selected_dates

# Ask for the year from the user
year_input = int(input("Kindly enter the year in which you wish to paint some custom contributions: "))
selected_dates = create_calendar(year_input)
print("Selected Dates:", selected_dates)
