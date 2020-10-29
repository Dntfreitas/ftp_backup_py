# FTP Backup Using Python

Performs a backup of a given directory using Python.

The directory that was backed up is then exported to a ZIP file. The ZIP file is named by the current timestamp.

## Example of use:

```python
if __name__ == '__main__':
    server = "IP_or_server_name"
    username = "username"
    password = "password"
    path = "ftp"
    backup(server, username, password, path)
