import requests
from bs4 import BeautifulSoup
import json


area_code = 211041270

# Empty dictionary to store JSON objects
json_data = {}

# ABS URL
abs_url = "https://www.abs.gov.au/census/find-census-data/quickstats/2021/211041270"

# Send HTTP GET request to the URL
response = requests.get(abs_url)

# Parse the HTML content using BS
soup = BeautifulSoup(response.content, "html.parser")


# Suburb Name
suburb = soup.find("h1").get_text()

##################### SUMMARY TABLES #####################

# Get all <table class="summaryTables">
summary_tables = soup.find_all(class_="summaryTables")

# Loop through each row in summary_tables
for table in summary_tables:
    summary_table_dict = {}

    # Get all table row elements
    summary_table_rows = table.find_all("tr")

    # Loop through each row
    for row in summary_table_rows:
        # Table headings
        summary_table_heading = row.find("th").get_text().strip()

        # Table data
        summary_table_data = row.find("td").get_text().strip()

        # Add key-value pair to the dictionary
        summary_table_dict[summary_table_heading] = summary_table_data

# Create and write to json file with suburb name in the json name
with open(f"summary_data_{suburb}.json", "w") as f:
    json.dump(summary_table_dict, f)


############################################################

##################### MAIN TABLES #####################
main_tables = soup.find_all(class_="qsTable")

row_headings_dict = {}
main_table_dict = {}
table_headings_list = []
row_headings_list = []

for table in main_tables:
    # Table Headings
    th_tags = table.find(class_="firstCol topRow")
    th_tags_string = str(th_tags)
    th_tags_split_one = th_tags_string.split(">")
    th_tags_split_two = th_tags_split_one[1].split("<")
    stripped_heading = th_tags_split_two[0].strip()
    table_headings_list.append(stripped_heading)

    # Row Headings

    # Use BS4 to find all rows
    row_tags = table.find_all(class_="firstCol", scope="row")

    # For Loop to split and strip row tags into text and append to list
    for row in row_tags:
        row_tags_string = str(row)
        row_tags_split_one = row_tags_string.split(">")
        row_tags_split_two = row_tags_split_one[1].split("<")
        stripped_row_tags = row_tags_split_two[0].strip()
        row_headings_list.append(stripped_row_tags)

    for row_heading in row_headings_list:
        if stripped_heading not in main_table_dict:
            main_table_dict.update({row_heading: {"Geography": [], "Value": []}})
        else:
            main_table_dict[stripped_heading][row_heading] = {
                "Geography": [],
                "Value": [],
            }

    print("*********Next Table Heading*********")

print(table_headings_list)
print(row_headings_list)
print(main_table_dict)


with open(f"main_data_{suburb}.json", "w") as f:
    json.dump(main_table_dict, f)
