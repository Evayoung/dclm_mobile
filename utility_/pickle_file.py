# import pickle
# import os
#
#
# # Create a Pickle File
# def create_pickle_file(filename, data):
#     with open(filename, "wb") as file:
#         pickle.dump(data, file)
#
#
# # Read from a Pickle File
# def read_pickle_file(filename):
#     if os.path.exists(filename):
#         with open(filename, "rb") as file:
#             loaded_data = pickle.load(file)
#             return loaded_data
#     else:
#         print(f"File '{filename}' not found.")
#         return None
#
#
# # Update a Pickle File
# def update_pickle_file(filename, updated_data):
#     existing_data = read_pickle_file(filename)
#     if existing_data is not None:
#         existing_data.update(updated_data)
#         with open(filename, "wb") as file:
#             pickle.dump(existing_data, file)
#
#
# # Delete a Pickle File
# def delete_pickle_file(filename):
#     if os.path.exists(filename):
#         os.remove(filename)
#         print(f"File '{filename}' deleted.")
#     else:
#         print(f"File '{filename}' not found.")
#
#
# # Example Usage:
# data = {"name": "Alice", "age": 30, "city": "Wonderland"}
#
# create_pickle_file("data.pkl", data)
# loaded_data = read_pickle_file("data.pkl")
# print(loaded_data)
#
# update_data = {"age": 31, "country": "Wonderland"}
# update_pickle_file("data.pkl", update_data)
# updated_data = read_pickle_file("data.pkl")
# print(updated_data)
#
# delete_pickle_file("data.pkl")


import pickle
import os


# Create a directory for the pickle file if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Create a Pickle File in a specified directory
def create_pickle_file(directory, filename, data):
    create_directory(directory)
    filepath = os.path.join(directory, filename)
    with open(filepath, "wb") as file:
        pickle.dump(data, file)


# Read from a Pickle File
def read_pickle_file(directory, filename):
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as file:
            loaded_data = pickle.load(file)
            return loaded_data
    else:
        print(f"File '{filepath}' not found.")
        return None


# Update a Pickle File
def update_pickle_file(directory, filename, updated_data):
    existing_data = read_pickle_file(directory, filename)
    if existing_data is not None:
        existing_data.update(updated_data)
        filepath = os.path.join(directory, filename)
        with open(filepath, "wb") as file:
            pickle.dump(existing_data, file)


# Delete a Pickle File
def delete_pickle_file(directory, filename):
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"File '{filepath}' deleted.")
    else:
        print(f"File '{filepath}' not found.")


# Example Usage:
data = {"name": "Alice", "age": 30, "city": "Wonderland"}
data2 = {"program_domain": "Global Crusade",
         "program_type": "Crusade",
         "program_level": "Location",
         "location_id": ""}

directory = "data_directory"

create_pickle_file(directory, "data.pkl", data)
loaded_data = read_pickle_file(directory, "data.pkl")
print(loaded_data)

update_data = {"age": 31, "country": "Wonderland"}
update_pickle_file(directory, "data.pkl", update_data)
updated_data = read_pickle_file(directory, "data.pkl")
print(updated_data)

# delete_pickle_file(directory, "data.pkl")
