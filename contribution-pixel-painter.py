import tkinter as tk
from datetime import datetime, timedelta
import subprocess
import os

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
	# Calculate the start day of the year and adjust to the first Sunday
	start_date = datetime(year, 1, 1)
	start_day = start_date.weekday()  # Monday = 0; Sunday = 6
	if start_day != 6:
		start_date -= timedelta(days=start_day + 1)  # Adjust to the previous Sunday

	# Calculate the end date for the calendar grid
	end_date = datetime(year, 12, 31)
	end_day = end_date.weekday()
	if end_day != 6:
		end_date += timedelta(days=(5 - end_day))  # Extend to the next Saturday

	current_date = start_date
	window = tk.Tk()
	window.title("Contribution Pixel Painter 🎨🖌️🖼️")
	window.configure(bg='black')

	selected_dates = []

	while current_date <= end_date:
		week = (current_date - start_date).days // 7
		day = current_date.weekday()
		frame = tk.Frame(window, borderwidth=1, relief="solid", width=20, height=20)
		frame.grid(row=(day + 1) % 7, column=week, sticky="nsew")
		frame.propagate(False)  # Don't resize

		frame_date = current_date.strftime('%Y-%m-%d') if current_date.year == year else ""
		color = 'black' if current_date.year != year else 'gray'
		frame.config(bg=color)

		if current_date.year == year:
			frame.bind("<Button-1>", lambda event, f=frame, d=frame_date: toggle_color(f, d, selected_dates))

		current_date += timedelta(days=1)

	window.mainloop()

	return selected_dates

# Ask for the year from the user
year_input = int(input("Kindly enter the year in which you wish to paint some custom contributions: "))
selected_dates = create_calendar(year_input)
print("Selected Dates:", selected_dates)

# Setup
filename = 'commit_log.md'
with open(filename, 'w') as file:
	file.write("# Git Contribution Art created using https://github.com/FreddyMSchubert/contribution-pixel-painter !\n")

def create_commit(date):
	with open(filename, 'a') as file:
		file.write(f"- Commit on {date}\n")
	# Stage the file
	subprocess.run(['git', 'add', filename], check=True)
	# Commit with the specified date
	env = os.environ.copy()
	env['GIT_COMMITTER_DATE'] = date + " 10:00:00"
	env['GIT_AUTHOR_DATE'] = date + " 10:00:00"
	subprocess.run(['git', 'commit', '-m', f'Contribution Art on {date}'], env=env, check=True)

for date in selected_dates:
	create_commit(date)

# Cleanup
os.remove(filename)
subprocess.run(['git', 'add', filename], check=True)
subprocess.run(['git', 'commit', '-m', 'Clean up after contribution art'], check=True)

print("Done! 🎨🖌️🖼️ Contribution art has been created.")