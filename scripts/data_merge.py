import json
import csv

data_folder = "./../dataset"

with open(f"{data_folder}/restaurants_list.json") as json_file:
    json_data = json.load(json_file)

restaurants = {}

with open(f"{data_folder}/restaurants_info.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    for row in csv_reader:
        obj_id = row["objectID"]
        restaurants[f"{obj_id}"] = row

# After a quick check it looked like the data in both files has the same objectIDs, so I'm not doing any checks here but this could be improved
for data in json_data:
    obj_id = data["objectID"]
    data.update(restaurants[f"{obj_id}"])

with open(f'{data_folder}/merged_file.json', 'w') as merged_file:
    json.dump(json_data, merged_file, indent=4)



