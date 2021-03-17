import os
import shutil


class FileOrganizer:
    def __init__(self, source_path: str, destination_path: str, copy: bool):
        self.all_files = []
        self.files = {}
        self.count = 0
        self.copy = copy

        # List all files from source path
        try:
            for file in os.listdir(source_path):
                if os.path.isfile(os.path.join(source_path, file)):
                    self.all_files.append(file)
        except FileNotFoundError:
            print('Invalid source path')

        # Make dictionary from all files; filename:(name, type)
        for file in self.all_files:
            name = os.path.splitext(file)
            ext = name[1:][0]
            first = name[0]
            # Don't move or copy ini files
            if ext.strip('.') == 'ini':
                pass
            else:
                self.files[file] = first, ext.strip('.')

        # Loop through all files in dictionary
        for key, value in self.files.items():
            # Make new folder if not already exists e.g. c:\destination_path\jpg
            new_folder_path = os.path.join(destination_path, value[1])
            try:
                os.makedirs(new_folder_path)
            except FileExistsError:
                pass

            # Full path for source file e.g. c:\source_path\picture.jpg
            src_file = os.path.join(source_path, key)

            # Full path for destination file e.g. c:\destination_path\jpg\picture.jpg
            destination = os.path.join(new_folder_path, key)

            # If destination folder have already file with same name as destination file
            while os.path.isfile(destination):
                # Add first free number to file name e.g. picture(1).jpg
                self.count += 1
                destination = os.path.join(new_folder_path, f"{value[0]}({self.count}).{value[1]}")

            # Copy or move based on user input
            if copy:
                shutil.copy(src_file, destination)
                print(f'{src_file} copied to {destination}')
            else:
                shutil.move(src_file, destination)
                print(f'{src_file} moved to {destination}')


if __name__ == '__main__':

    while True:

        src_list = []
        des_list = []

        src = input("Enter source path (absolute) e.g. C:/folder or C:\\folder : ")
        for letter in src:
            if letter == '/':
                letter = '\\'
            src_list.append(letter)

        des = input("Enter destination path (absolute) e.g. C:\\folder or C:/folder : ")
        for letter in des:
            if letter == '/':
                letter = '\\'
            des_list.append(letter)

        source_folder = os.path.join(''.join(src_list))
        destination_folder = os.path.join(''.join(des_list))

        try:
            action = input("Enter 'c' to copy files or 'm' to move files: ").lower()
            if action == 'm':
                FileOrganizer(source_folder, destination_folder, False)
            elif action == 'c':
                FileOrganizer(source_folder, destination_folder, True)
            else:
                print('Invalid input. Enter c to copy files or m to move files')
        except FileNotFoundError:
            print(f'FileNotFoundError: The system cannot find the path specified: {destination_folder}')

        if input('Do you want to organize more folders? "y" or "n": ').lower() != 'y':
            break
