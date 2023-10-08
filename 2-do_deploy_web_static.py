#!/usr/bin/python3
"""
Fabric script that distributes an archive to our web servers
"""

from fabric.api import *
from os.path import exists
env.hosts = ['18.234.253.165', '100.25.196.203']


def do_deploy(archive_path):
    """
    do_deploy - function that distributes an archive to your web servers
    return: True if all operations have been done correctly,
            otherwise returns False
    """

    # Returns False if the file at the path archive_path doesn’t exist
    if exists(archive_path) is False:
        return False

    try:
        # file information (the name of the file that will be distributed)
        f = archive_path.split("/")[-1]  # output: <filename>.tgz
        f_name = file_name.split(".")[0]  # output: <filename>
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')
        # Uncompress the archive to the folder
        #   /data/web_static/releases/<filename> on the web server
        path = "/data/web_static/releases/"
        run('mkdir -p {}{}/'.format(path, f_name))
        run('tar -xzf /tmp/{} -C {}{}/'.format(f, path, f_name))
        # Delete the archive file from the web server
        run('rm /tmp/{}'.format(f))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, f_name))
        run('rm -rf {}{}/web_static'.format(path, f_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, f_name))
        print("New version deployed!")
        return True
    except Exception:
        print("something is wrong!")
        return False
