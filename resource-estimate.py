from asyncore import write
import yaml
import pprint
import csv
import os
import copy

def extract_limits_and_replicas(yaml_file):
    with open(yaml_file, 'r') as file:
        deployment = yaml.safe_load(file)

    # Extracting replicas
    replicas = deployment['spec'].get('replicas', 1)

    # Extracting CPU and Memory limits
    containers = deployment['spec']['template']['spec'].get('containers', [])

    for container in containers:
        container_name = container['name']
        cpu_limit = container['resources']['limits'].get('cpu', 'Not specified')
        memory_limit = container['resources']['limits'].get('memory', 'Not specified')
        
        _data={
            'container_name': container_name,
            'cpu_limit': cpu_limit,
            'memory_limit': memory_limit,
            'replicas': replicas
        }




    return _data

def write_to_csv(csv_file, data):
    try:
        with open(csv_file, mode='a', newline='') as file:
            # Create a DictWriter object
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            
            # Write the header
            writer.writeheader()
            
            # Write the data
            writer.writerows(data)

        print(f"Data has been written to {csv_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_files_in_directory(directory):
    # List to hold all file names
    file_list = []
    
    # Loop through the directory
    for filename in os.listdir(directory):
        # Construct full file path
        file_path = os.path.join(directory, filename)
        # Check if it is a file
        if os.path.isfile(file_path):
            file_list.append(file_path)  # Add the file name to the list
    
    return file_list

if __name__ == "__main__":
    yaml_file_directory = "yamls"  # Path to your deployment YAML file
    csv_file = "resource-estimate.csv"
    data = []
    files = list_files_in_directory(yaml_file_directory)
    print(files)
    for yaml_file in files:
        result = extract_limits_and_replicas(yaml_file)
        d = copy.deepcopy(result)
        data.append(d)

    pprint.pprint(data)
    write_to_csv(csv_file,data)

