import os
import datetime

# Define the directory where the log files are stored
log_directory = "C:/Users/skrge/"

# Number of days to merge
num_days_to_merge = 7

def merge_log_files(log_dir, num_days):
    current_date = datetime.date.today()
    merged_rows = []

    for i in range(num_days):
        date_to_merge = current_date - datetime.timedelta(days=i)
        file_name = f"listen-{date_to_merge.strftime('%Y%m%d')}.txt"
        file_path = os.path.join(log_dir, file_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                merged_rows.extend(file.readlines())

    with open("listen-last_7days.log", 'w') as merged_file:
        merged_file.writelines(merged_rows)

    return "listen-last_7days.log"

if __name__ == "__main__":
    merged_file_name = merge_log_files(log_directory, num_days_to_merge)
    print(f"Log files merged into: {merged_file_name}")
