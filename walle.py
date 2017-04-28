#!/usr/bin/env python3
###############################################################################
# wallepy
# Brandon Milton
# https://github.com/brandonio21/wallepy
#
# An automatic wallpaper setter and getter using feh
###############################################################################
import click
import errno
import os
import sys
from random import choice
from shutil import copyfileobj
from subprocess import check_call
from hashlib import sha256
from urllib.request import urlopen


def set_wallpaper(feh_path, wallpaper_path):
    if os.name == "nt":
        sys_params_call = None
        import ctypes
        import struct
        if struct.calcsize('P') * 8 == 64:
            sys_params_call = ctypes.windll.user32.SystemParametersInfoW
        else:
            sys_params_call = ctypes.windll.user32.SystemParametersInfoA

        assert sys_params_call(20, 0, wallpaper_path, 0)
    else:
        check_call([f'{feh_path}', '--bg-fill', f'{wallpaper_path}'])


def get_urls_from_url_file(urlfile_path):
    url_list = []
    with open(urlfile_path, 'r') as f:
        url_list = list(f.read().splitlines())

    return [(sha256(url.encode('utf-8')).hexdigest(), url) for url in url_list]


def download_image_from_url(url, dest):
    progress_dest = dest + ".download"
    with urlopen(url) as online_image_fd:
        with open(progress_dest, 'wb') as local_image_fd:
            copyfileobj(online_image_fd, local_image_fd)
    os.rename(progress_dest, dest)


def assert_dir_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def assert_file_exists(path):
    if not os.path.exists(path):
        open(path, 'w').close()


def get_default_config_path(filename, is_dir=False):
    home_dir = os.path.expanduser('~')
    config_dir = os.path.join(home_dir, '.config')
    walle_cfg_dir = os.path.join(config_dir, 'wallepy')

    file_path = os.path.join(walle_cfg_dir, filename)

    assert_dir_exists(walle_cfg_dir)

    if not is_dir:
        assert_file_exists(file_path)
    else:
        assert_dir_exists(file_path)

    return file_path


@click.command()
@click.option('--urlfile', default=get_default_config_path('urls.txt'),
              type=click.Path(exists=True),
              help='Path to a file containing newline delineated image URLs')
@click.option('--imagedir',
              default=get_default_config_path('images', is_dir=True),
              type=click.Path(exists=True),
              help='Path to directory where images will be downloaded')
@click.option('--fehpath', default='feh',
              help='Path to feh executable used to set wallpapers')
def main(urlfile, imagedir, fehpath):

    # First, load all existing images into a cache.
    existing_images = set(os.listdir(imagedir))

    # Now load all urls from the textfile
    requested_urls = dict(get_urls_from_url_file(urlfile))

    # Now remove any images that are not in the url file
    for image_hash in existing_images:
        if (os.path.splitext(image_hash)[1] == ".download" or
                image_hash not in requested_urls):
            os.remove(os.path.join(imagedir, image_hash))

    # If there are no requested urls, exit early
    if not requested_urls:
        return

    # Now select an image at random from the requested_urls
    random_url_hash = choice(list(requested_urls.keys()))
    random_url = requested_urls[random_url_hash]

    # If it doesnt exist, download it
    image_path = os.path.join(imagedir, random_url_hash)
    if random_url_hash not in existing_images:
        try:
            download_image_from_url(random_url, image_path)
        except Exception as e:
            sys.stderr.write("Could not download image {}\n".format(str(e)))

            if not existing_images:
                return

            image_path = os.path.join(imagedir, choice(existing_images))

    # Display it
    set_wallpaper(fehpath, image_path)


if __name__ == '__main__':
    main()
