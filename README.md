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
systemctl --user enable wallepy.service
systemctl --user enable wallepy.timer
systemctl --user start wallepy.service
```
