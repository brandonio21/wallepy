wallepy
=======
An automatic wallpaper getter and setter using `feh`. Specify a list of URLs in
a textfile and wallepy will randomly choose one, download the image, and set it
as your wallpaper.

When urls are removed from the text file, their corresponding 
cached images are also removed.


## Requirements
By default, wallepy has the following dependencies:
* Python3
* python-click
* feh

## Installation/Run Instructions
wallepy is available in the [AUR](https://aur.archlinux.org/packages/wallepy)

To install and run `wallepy`, do the following:

```bash
git clone https://github.com/brandonio21/wallepy
cd wallepy
python3 walle.py
```

wallepy also comes with a systemd service unit that changes your wallpaper on
startup and every hour

```bash
cp wallepy.service /usr/lib/systemd/user
cp wallepy.timer /usr/lib/systemd/user
systemctl --user enable wallepy.timer
systemctl --user start wallepy.service
```

## Usage
wallepy takes a list of image URLs, picks one at random, downloads it if needed,
and sets it as your wallpaper. Thus, to operate, it needs a list of URLs. This
list can be provided as a newline delineated textfile. By default, wallepy reads
from `$HOME/.config/wallepy/urls.txt` and downloads all images to
`$HOME/.config/wallepy/images`. However, these can be set with the --urlfile
and --imagedir flags, respectively.

For instance,
```bash
walle.py --urlfile ~/Downloads/urls.txt --imagedir ~/wallpapers
```
