import requests
from bs4 import BeautifulSoup
import json


area_code = 211041270

# Empty dictionary to store JSON objects
json_data = {}

# ABS URL
abs_url = "https://www.abs.gov.au/census/find-census-data/quickstats/2021/211041270"
# abs_url_2 = "https://www.abs.gov.au/census/find-census-data/quickstats/2021/212021293"

# Send HTTP GET request to the URL
response = requests.get(abs_url)

# Parse the HTML content using BS
soup = BeautifulSoup(response.content, "html.parser")


# Suburb Name
suburb = soup.find("h1").get_text()

# State Name
location_row = soup.find_all(class_="geoCol", limit=2)
location_list = []
for location in location_row:
    location_str = str(location)
    location_split_one = location_str.split(">")
    location_split_two = location_split_one[1].split("<")
    location_stripped = location_split_two[0].strip()
    location_list.append(location_stripped)
state = location_list[1]


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

main_table_dict = {}
data_list = []

# Use BS4 to find all tables
main_tables = soup.find_all(class_="qsTable")

for table in main_tables:
    table_name = table.find(class_="topRow")

    #### TABLE NAME ###
    # Split and Strip BS4 result to get Table Name
    table_name_str = str(table_name)
    table_name_split_one = table_name_str.split(">")
    table_name_split_two = table_name_split_one[1].split("<")
    table_name_stripped = table_name_split_two[0].strip()

    ### ROW NAME ###
    # Use BS4 to find the number of rows per table
    row_count = 0
    row_name_list = []
    num_table_rows = 0
    table_rows = table.find_all(class_="firstCol")
    for row in table_rows:
        row_str = str(row)
        row_split_one = row_str.split(">")
        row_split_two = row_split_one[1].split("<")
        row_stripped = row_split_two[0].strip()
        if row_stripped == table_name_stripped:
            pass
        else:
            row_name_list.append(row_stripped)

    # THIS IS THE SOURCE OF THE BUG
    # IF THERE IS A BLANK, IT CAUSES THE COUNT TO BE WRONG
    num_table_rows = len(row_name_list)

    ### ROW DATA ###
    # Using the number of rows, we can limit how many <td> tags to search for using BS4
    # e.g. 3 rows in a table will mean 18 <td> tags (= 6 <td> per row * 3)
    td_tags = table.find_all("td", limit=num_table_rows * 6)
    data_list = []
    for td in td_tags:
        td_str = str(td)
        td_split_one = td_str.split(">")
        td_split_two = td_split_one[1].split("<")
        td_stripped = td_split_two[0].strip()
        data_list.append(td_stripped)
    data_list_length = len(data_list)
    print(
        f"TABLE NAME: {table_name_stripped} \n ROW NAMES: {row_name_list} \n NUMBER OF ROWS: {num_table_rows} \n LENGTH OF DATA LIST: {data_list_length} \n data : {data_list} \n\n\n"
    )

    # BUG: if blank row is in the middle of a table, subsequent rows are not picked up

    # Create dictionary
    for row_name in row_name_list:
        if table_name_stripped not in main_table_dict:
            main_table_dict.update(
                {
                    row_name: {
                        "Geography": [suburb, "%", state, "%", "Australia", "%"],
                        "Value": [data_list],
                    }
                }
            )
        else:
            main_table_dict[table_name][row_name]

    print("\n\n\n********* NEXT TABLE ********* \n\n\n")

with open(f"main_data_{suburb}.json", "w") as f:
    json.dump(main_table_dict, f)


# for row_heading in row_headings_list:
#     if table_name not in main_table_dict:
#         main_table_dict.update({row_heading: {"Geography": [], "Value": []}})
#     else:
#         main_table_dict[table_name][row_heading] = {
#             "Geography": [],
#             "Value": [],
#         }


# for table in main_tables:
#     # Table Names
#     # Use BS4 to find all table names
#     th_tags = table.find(class_="firstCol topRow")
#     th_tags_string = str(th_tags)
#     th_tags_split_one = th_tags_string.split(">")
#     th_tags_split_two = th_tags_split_one[1].split("<")
#     table_name = th_tags_split_two[0].strip()
#     print(f"Table name is: {table_name}")

#     # Row Headings
#     # Use BS4 to find all rows within the iterated table
#     rows = table.find_all(class_="firstCol", scope="row")

#     # Initialise blank list for row headings after each loop through main_tables
#     row_headings_list = []

#     # For Loop to split and strip row tags into text and append to a list
#     # List of row headings will allow us to create a nested dictionary
#     for row in rows:
#         row_tags_string = str(row)
#         row_tags_split_one = row_tags_string.split(">")
#         row_tags_split_two = row_tags_split_one[1].split("<")
#         stripped_row_tags = row_tags_split_two[0].strip()
#         row_headings_list.append(tags)

#         print(f"rowheadings_list: {row_headings_list}")
#         # For Loop to iterate over each row and handle data

#         # row_headings_list = ["Median weekly rent (a)"]

#         for row_heading in row_headings_list:
#             # Use BS4 to find data points within current row

#             # find_all(name, attributes, recursive, string, limit, **kwargs)
#             data_tags = table.find_all("td")

#             for data in data_tags:
#                 data_tags_string = str(data)
#                 data_tags_split_one = data_tags_string.split(">")
#                 data_tags_split_two = data_tags_split_one[1].split("<")
#                 stripped_data_tags = data_tags_split_two[0].strip()
#                 data_list.append(stripped_data_tags)
#                 print(f"data_list: {data_list}")

#             # print(f"row heading: {row_heading} \n data list: {data_list}")
#             data_list = []
#             # print(f"data for {row_heading}: {stripped_data_tags}")
#             # print(f"data_list is {data_list}")
#             # print("\n Next Row loop")

#         print("\n NEXT ROW LOOP \n")
#     #     data_string = str(data)
#     #     data_tags_split_one = data_string.split(">")
#     #     data_tags_split_two = data_tags_split_one[1].split("<")
#     #     stripped_data_tags = data_tags_split_two[0].strip()
#     #     print(stripped_data_tags)
#     #     row_data.append(stripped_data_tags)

#     # print(f"{stripped_row_tags}: {row_data}")

#     # Add data values to main_table_dict[table_name][row_heading][Value]

#     # print(f"{stripped_row_tags}: {row_data}")
#     # print("\n ***Next Row Heading*** \n")

#     # for row_heading in row_headings_list:
#     #     if table_name not in main_table_dict:
#     #         main_table_dict.update({row_heading: {"Geography": [], "Value": []}})
#     #     else:
#     #         main_table_dict[table_name][row_heading] = {
#     #             "Geography": [],
#     #             "Value": [],
#     #         }

#     print("\n\n\n*********Next Table Heading*********")


# print(main_table_dict)


# with open(f"main_data_{suburb}.json", "w") as f:
#     json.dump(main_table_dict, f)
