import os

folders = input("Please provide a list of folders separated by spaces: ").split()

for folder in folders:
    try:
        # Normalize the folder path to handle both forward slashes and backslashes
        folder_path = os.path.normpath(folder)
        files = os.listdir(folder_path)
        print('\n')
        print("List of files in " + folder_path + ":")
        
        for file in files:
            print(file)
            
    except FileNotFoundError:
        print("Folder '" + folder + "' not found.")