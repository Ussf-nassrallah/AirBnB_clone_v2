#!/usr/bin/python3
"""
script that generates a .tgz archive from the contents
  of the web_static folder
"""
from datetime import datetime
from fabric.api import local


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
