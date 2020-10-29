import os
import shutil
import zipfile
from datetime import datetime
from ftplib import FTP


def backup(server, username, password, path):
    """
Performs a backup of a folder of an FTP connection and export it to a ZIP file. The ZIP file is named by the current timestamp
    :param server: server name or IP
    :param username: username for the FTP connection
    :param password: password for the FTP connection
    :param path: path that to back up
    """
    # Saves the current working directory
    owd = os.getcwd()
    # Creates the same path of the FTP in the local machine
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)
    # Performs a connection to the FTP server
    ftp = FTP(server)
    ftp.login(username, password)
    # Download all the files from the FTP server
    download_tree(ftp, path)
    # Close the connection to the FTP server
    ftp.quit()
    # Restores the current working directory
    os.chdir(owd)
    # Extracts current timestamp
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # Creates a .zip file with the files downloaded from the serever
    path = path.split("/")[0]
    zip_file = zipfile.ZipFile(now + '.zip', 'w', zipfile.ZIP_DEFLATED)
    zip_directory(path, zip_file)
    zip_file.close()
    # Deletes the created directory
    shutil.rmtree(path)


def download_tree(ftp, path):
    """
Download all the files in an FTP directory
    :param ftp: ftp connection
    :param path: path to start navigating and downloading files
    """
    # Set current path
    ftp.cwd(path)
    os.chdir(path)
    # Get the items
    items = []
    ftp.dir(items.append)
    # For each item
    for item in items:
        # If is directory
        is_directory = item.startswith('d')
        # Extract the name of the item
        item_name = item[56:]
        if is_directory:
            # Set path and append to the tree
            path = path + "/" + item_name
            os.mkdir(item_name)
            # Find all sub-directories
            download_tree(ftp, item_name)
            # Get back
            ftp.cwd("..")
            os.chdir("..")
        # Otherwise
        else:
            # Download the file
            with open(item_name, 'wb') as fp:
                ftp.retrbinary('RETR ' + item_name, fp.write)


def zip_directory(path, method):
    """
Zips a given directory
Refer to https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory-in-python
    :param path: path of the directory to be zipped
    :param method: ZIP compression method
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            method.write(os.path.join(root, file))
