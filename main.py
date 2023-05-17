import requests
import json
import openpyxl
from bs4 import BeautifulSoup

# Open Area_Codes.xlsx
workbook = openpyxl.load_workbook("Area_Codes.xlsx")

# Select a specific sheet within the workbook
sheet = workbook["SA2_2021_AUST_GDA2020"]


# Add area codes in column A to a list
area_code_list = []
for cell in sheet["A"]:
    area_code_list.append(cell.value)

# Remove first element which is the column heading
area_code_list.pop(0)

new_area_list = area_code_list[1751:]

for area_code in new_area_list:
    # ABS URL
    abs_url = (
        f"https://www.abs.gov.au/census/find-census-data/quickstats/2021/{area_code}"
    )

    # Send HTTP GET request to the URL
    response = requests.get(abs_url)

    # Parse the HTML content using BS
    soup = BeautifulSoup(response.content, "html.parser")

    # Suburb Name
    suburb = soup.find("h1").get_text()

    # State Name
    try:
        location_row = soup.find_all(class_="geoCol", limit=2)
        location_list = []
        for location in location_row:
            location_str = str(location)
            location_split_one = location_str.split(">")
            location_split_two = location_split_one[1].split("<")
            location_stripped = location_split_two[0].strip()
            location_list.append(location_stripped)
        print(f"location list: {location_list}")
        state = location_list[1]
    except IndexError:
        pass

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

        # Create dictionary
        nested_dict = {}
        nested_dict[table_name_stripped] = {}
        data_index = 0
        for row_name in row_name_list:
            nested_dict[table_name_stripped][row_name] = {
                suburb: data_list[data_index],
                "% of suburb": data_list[data_index + 1],
                state: data_list[data_index + 2],
                "% of state": data_list[data_index + 3],
                "Australia": data_list[data_index + 4],
                "% of country": data_list[data_index + 5],
            }
            data_index += 6

        main_table_dict.update(nested_dict)

    # Create main_data_suburb.json
    with open(f"main_data_{suburb}.json", "w") as f:
        json.dump(main_table_dict, f)
