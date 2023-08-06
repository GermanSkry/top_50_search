# top_50_search
Algorithm for finding the 50 most frequently occurring strings by condition

The goal of the algorithm is to process a large log file containing song data and calculate the top 50 songs for each country based on the number of streams.

The algorithm takes as input a log file named listen-{current_date}.log, where {current_date} is the current date in the format "YYYYMMDD". The log file contains records of songs played, each row following the format: <song_id> | <user_id> | <country>. The algorithm processes the file in chunks using a generator, which significantly reduces memory consumption for large datasets. My log file was in the C:/Users/skrge/ directory, modify the log_file_path variable in the main() function to point to the correct file location.

'read_log_file': This function reads the log file in chunks and filters out invalid rows using a generator. It reads a portion of the file, processes it, and then moves to the next chunk. This reduces the memory overhead significantly when dealing with large datasets.

'calculate_all_songs_per_country': This function processes the filtered rows and calculates the number of streams for each song in each country. It uses a dictionary to store the song IDs and their play counts for each country. To avoid unnecessary data duplication, it directly uses a numpy array to store the play counts, reducing memory usage. Intermediate Files: After calculating the play counts for each song in each country, the function writes the intermediate results to disk for each country using JSON serialization. Intermediate files are named all_songs_intermediate_{country}.json, where {country} is the country code

'calculate_top_50_songs_from_files': This function reads the intermediate files for each country and calculates the top 50 songs based on the play counts. It uses numpy arrays to efficiently perform the sorting and selection of the top 50 songs.

'write_top_50_songs_to_files': After calculating the top 50 songs for each country, this function writes the results to separate text files. The file name includes the country code and the current date.

'main': The main function orchestrates the entire process. It calls the other functions in the correct order to read the log file, calculate the play counts, calculate the top 50 songs, and write the results to files.

Run the script using the Python interpreter:
python song_analysis.py

The script will start processing the log file, and you will see the progress on the console. It will calculate the play counts for each song in each country, create intermediate files, calculate the top 50 songs for each country, and save the results in separate text files. The script provides information about the time taken to execute the algorithm and the memory usage during the process, allowing you to monitor the performance and resource utilization.

After the script finishes executing, you will see the execution time and memory usage on the console. The top 50 songs for each country will be saved in the files named country_top50_{country}_{current_date}.txt.

Throughout the algorithm, we used various optimization techniques, such as chunking, using numpy arrays, creating intermediate files and deleting the unnecessary variable, to reduce memory usage and improve the efficiency of the code. These optimizations are crucial when dealing with large datasets to avoid running out of memory and improve overall performance.



The following Python libraries are used in the algorithm:
os: This library provides a way to interact with the operating system, allowing the script to handle file paths and operations.
re: The regular expression library is used for pattern matching in the log file to filter out valid rows.
numpy (np): Numpy is a powerful library for numerical computing in Python. It is used to efficiently store and manipulate arrays, which helps optimize memory usage.
heapq: The heapq module provides heap queue algorithms, which are used to find the top 50 songs based on their play counts efficiently.
json: The json library is used for serialization and deserialization of data. It is used to save and load intermediate results to/from files.
datetime: The datetime module provides functions to work with dates and times. It is used to get the current date in the required format for file naming.
time: This module is used to measure the execution time of the algorithm.
psutil: The psutil library allows the script to monitor system resource usage. It is used to get memory usage information during the execution of the algorithm.
