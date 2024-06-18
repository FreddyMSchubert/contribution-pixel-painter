import tkinter as tk
from datetime import datetime, timedelta
import subprocess
import os

def toggle_color(f, date, selected_dates, commit_count):
	colors = {1: '#1F432B', 2: '#2E6B38', 3: '#52A44E', 4: '#6CD064'}
	if date not in selected_dates or selected_dates[date] != commit_count:
		selected_dates[date] = commit_count
		f.config(bg=colors.get(commit_count, '#171B21'))
	else:
		selected_dates.pop(date, None)
		f.config(bg='#171B21')  # Off-color

def create_commit(date, count):
	for _ in range(count):
		with open(filename, 'a') as file:
			file.write(f"- Commit on {date}\n")
		# Stage the file
		subprocess.run(['git', 'add', filename], check=True)
		# Commit with the specified date
		env = os.environ.copy()
		env['GIT_COMMITTER_DATE'] = date + " 10:00:00"
		env['GIT_AUTHOR_DATE'] = date + " 10:00:00"
		subprocess.run(['git', 'commit', '-m', f'Contribution Art on {date}'], env=env, check=True)

def create_calendar(year, commit_count):
	start_date = datetime(year, 1, 1)
	start_day = start_date.weekday()  # Monday = 0; Sunday = 6
	if start_day != 6:
		start_date -= timedelta(days=start_day + 1)  # Adjust to prev Sunday
	end_date = datetime(year, 12, 31)
	end_day = end_date.weekday()
	if end_day != 6:
		end_date += timedelta(days=(5 - end_day))  # Lengthen to next Saturday

	current_date = start_date
	window = tk.Tk()
	window.title("🟩🟩🟩 Contribution Pixel Painter 🎨🖌️🖼️")
	window.configure(bg='black')

	selected_dates = {}

	# Calendar Frame
	calendar_frame = tk.Frame(window, bg='black')
	calendar_frame.grid(row=0, column=0, padx=10, )

	while current_date <= end_date:
		week = (current_date - start_date).days // 7
		day = current_date.weekday()
		frame = tk.Frame(calendar_frame, borderwidth=1, relief="solid", width=20, height=20)
		frame.grid(row=(day + 1) % 7, column=week, sticky="nsew")
		frame.propagate(False)  # Dont resize

		frame_date = current_date.strftime('%Y-%m-%d') if current_date.year == year else ""
		color = 'black' if current_date.year != year else '#171B21'
		frame.config(bg=color)

		if current_date.year == year:
			frame.bind("<Button-1>", lambda event, f=frame, d=frame_date: toggle_color(f, d, selected_dates, commit_count))

		current_date += timedelta(days=1)

	# Button Frame
	button_frame = tk.Frame(window, bg='black')
	button_frame.grid(row=1, column=0, padx=10, pady=10)

	colors = {1: '#1F432B', 2: '#2E6B38', 3: '#52A44E', 4: '#6CD064'}
	for i in range(1, 5):
		frame = tk.Frame(button_frame, bg=colors[i], bd=5, relief="raised")
		frame.grid(row=0, column=i-1, padx=5, pady=5, sticky="ew")
		button = tk.Button(frame, bg=colors[i], fg=colors[i], command=lambda i=i: update_commit_count(i))
		button.pack(fill="both", expand=True)
	
	def update_commit_count(i):
		nonlocal commit_count
		commit_count = i

	window.mainloop()
	return selected_dates

# Ask for the year from the user
year_input = int(input("Kindly enter the year in which you wish to paint some custom contributions: "))
commit_count = 1
selected_dates = create_calendar(year_input, commit_count)
print("Selected Dates:", selected_dates)

# Setup
if not selected_dates:
	print("No dates selected. Exiting.")
	exit()
filename = 'commit_log.md'
with open(filename, 'w') as file:
	file.write("# Git Contribution Art created using https://github.com/FreddyMSchubert/contribution-pixel-painter !\n")

for date in selected_dates:
	create_commit(date)

# Cleanup
os.remove(filename)
subprocess.run(['git', 'add', filename], check=True)
subprocess.run(['git', 'commit', '-m', 'Clean up after contribution art'], check=True)

print("Done! 🎨🖌️🖼️ Commits for Contribution art have been created.")