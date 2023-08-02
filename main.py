import os
import re
import random
import string
import heapq
import pickle
import datetime

def read_log_file(file_path):
    rows = []
    with open(file_path, 'r') as file:
        for line in file:
            row = line.strip()
            # Use regex to check if the row follows the correct format
            if re.match(r'^\d+\s*\|\s*\d+\s*\|\s*[A-Z]{2}$', row):
                rows.append(row)
    return rows

def calculate_top_50_songs(filtered_rows):
    top_50_songs_per_country = {}
    # Loop through the filtered rows and extract song IDs, user IDs, and the number of streams
    for row in filtered_rows:
        song_id, user_id, country = map(str.strip, row.split('|'))  # Extract song_id, user_id, and country from the row

        # Create a dictionary for each country if it doesn't exist
        top_50_songs_per_country.setdefault(country, {})

        # Increment the streams count for the current song in the corresponding country
        top_50_songs_per_country[country][song_id] = top_50_songs_per_country[country].get(song_id, 0) + 1

    # Write intermediate results to disk and free up memory
    for country in top_50_songs_per_country:
        # Convert the country dictionary to a list of tuples and use a heap to find the top 50 songs
        top_50_songs = heapq.nlargest(50, top_50_songs_per_country[country].items(), key=lambda x: x[1])
        top_50_songs_per_country[country] = top_50_songs
        # Write the intermediate result to disk for each country using pickle serialization
        with open(f"top50_intermediate_{country}.pkl", 'wb') as file:
            pickle.dump(top_50_songs, file)

    # Select the top 50 songs for each country by loading the intermediate results from disk
    for country in top_50_songs_per_country:
        with open(f"top50_intermediate_{country}.pkl", 'rb') as file:
            top_50_songs_per_country[country] = pickle.load(file)

    return top_50_songs_per_country

def write_top_50_songs_to_files(top_50_songs_per_country):
    current_date = datetime.date.today().strftime("%Y%m%d")
    for country, top_50_songs in top_50_songs_per_country.items():
        filename = f"country_top50_{country}_{current_date}.txt"
        with open(filename, 'w') as file:
            file.write(f"{country}|")
            song_data = ','.join([f"{song_id}:{streams}" for song_id, streams in top_50_songs])
            file.write(song_data)

def main():
    file_name = 'generated_data.txt'  # Replace YYYYMMDD with the specific date
    log_file_path = os.path.join('C:/Users/skrge/', file_name)
    filtered_rows = read_log_file(log_file_path)
    top_50_songs_per_country = calculate_top_50_songs(filtered_rows)
    write_top_50_songs_to_files(top_50_songs_per_country)

if __name__ == "__main__":
    main()