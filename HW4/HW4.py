import argparse
import csv

parser = argparse.ArgumentParser(description="These function will show TOP n HRR and percent of available beds.")

parser.add_argument("-path", type=str, help="Path where file lies",)

parser.add_argument("-bed", type=int, help="Enter a number of HRR what will be shown")

arguments = parser.parse_args()


def percent_of_available_beds(path: str, bed: int):
    """"
    :param path: шлях за яким можна знайти файл
    :param bed: кількість HRR що буде виведена
    """
    all_hrr = {}
    i = 0

    with open(f"{path}\HRR Scorecard_ 20 _ 40 _ 60 - 20 Population.csv") as file:
        content = csv.reader(file)
        headers = next(content)
        next(content)

        for row in content:
            # вичитує з стрічки колонку Total Hospital Beds
            total_beds = float(row[headers.index('Total Hospital Beds')].replace(",", ""))
            # вичитує з стрічки колонку Available Hospital Beds
            available_beds = float(row[headers.index('Available Hospital Beds')].replace(",", ""))
            # вичитує з стрічки колонку hrr
            hrr = row[headers.index('HRR')]
            all_hrr[hrr] = available_beds/total_beds

    hrr_sorted = sorted(all_hrr.items(), key=lambda x: x[1], reverse=True)

    while i < bed:
        print(f"{hrr_sorted[i][0]} : {hrr_sorted[i][1]*100:.2f}%")
        i += 1


percent_of_available_beds(arguments.path, arguments.bed)
