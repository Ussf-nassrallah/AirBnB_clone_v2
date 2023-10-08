#!/usr/bin/python3
"""
script that generates a .tgz archive from the web_static folder
  and send this file to our servers
"""
from datetime import datetime
from fabric.api import *
from os.path import exists
env.hosts = ['18.234.253.165', '100.25.196.203']


@task
def do_pack():
    """
    do_pack: function that generates a .tgz archive
    file_name format: web_static_<year><month><day><hour><minute><second>.tgz
    return: the archive path if the archive has been correctly generated.
            Otherwise, it should return None
    """

    # file information (the name of the file thats will be generated )
    dt_format = "%Y%m%d%H%M%S"
    current_dt = datetime.now().strftime(dt_format)
    file_name = "web_static_{}.tgz".format(current_dt)

    # All archives must be stored in the folder versions
    local("mkdir -p versions")

    # generate .tgz file from web_static folder
    generate_file = local("tar -cvzf versions/{} web_static".format(file_name))

    # checks if generate_file is succeeded
    if generate_file.succeeded:
        return file_name
    else:
        return None


@task
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
        f_name = f.split(".")[0]  # output: <filename>
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
    except Exception as e:
        print(e)
        return False


@task
def deploy():
    """creates & distributes an archive to the web servers"""
    archive_file = do_pack()
    if archive_file is None:
        return False
    return do_deploy(archive_file)