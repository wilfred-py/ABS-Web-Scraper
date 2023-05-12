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


test_tuple = ("People", "()", "")

for table in main_tables:
    # Table Headings
    th_tags = table.find(class_="firstCol topRow")
    th_tags_string = str(th_tags)
    th_tags_split_one = th_tags_string.split(">")
    th_tags_split_two = th_tags_split_one[1].split("<")
    stripped_heading = th_tags_split_two[0].strip()
    # print(f"Table Heading: {stripped_heading}")

    # Row Headings
    row_tags = table.find_all(class_="firstCol", scope="row")

    row_headings_list = []

    for row in row_tags:
        row_tags_string = str(row)
        row_tags_split_one = row_tags_string.split(">")
        row_tags_split_two = row_tags_split_one[1].split("<")
        stripped_row_tags = row_tags_split_two[0].strip()
        row_headings_list.append(stripped_row_tags)

        # print(f"Row Heading: {stripped_row_tags}")

    print(row_headings_list)
    print("*********Next Table Heading*********")
    # main_table_dict[stripped_heading] = row_headings_dict


# print(row_headings_list)
with open(f"main_data_{suburb}.json", "w") as f:
    json.dump(main_table_dict, f)

# ISSUE: for loop is overriding all ROW headings except last heading
#        before moving onto the next TABLE heading

# Dictionary comprehension to loop over all row tags and create a dictionary
# row_headins_dicct = {heading: {} for heading in row_headings_list}


# main_table_dict[stripped_heading] = {stripped_row_tags: {}}
# row_headings_list.append({stripped_heading: stripped_row_tags})

{
    "People": {
        "Male": {
            "Geography": ["Suburb", "%", "Victoria", "%", "Australia", "%"],
            "Value": [
                "<td></td>",
                "<td></td>",
                "<td></td>",
                "<td></td>",
                "<td></td>",
                "<td></td>",
            ],
        },
        "Female": {
            "Geography": ["Suburb", "%", "Victoria", "%", "Australia", "%"],
            "Value": [
                "<td></td>",
                "<td></td>",
                "<td></td>",
                "<td></td>",
                "<td></td>",
                "<td></td>",
            ],
        },
    },
    "Indigenous Status": {
        "Aboriginal and/or Torres Strait Islander": {
            "Geography": [],
            "Value": [],
        },
        "Non-Indigenous": {
            "Geography": [],
            "Value": [],
        },
    },
}
