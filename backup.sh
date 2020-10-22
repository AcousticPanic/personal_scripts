#! /bin/bash

cd /
sudo rsync -aAXh --progress --exclude={/dev,/proc,/sys,/tmp,/run,/mnt,/lost+found,/media,/home/dustin/.cache/mozilla,/home/dustin/.cache/google-chrome,/home/dustin/.config/Microsoft/Microsoft\ Teams/} /  dpeet@10.2.200.213:/home/dpeet/WS-Backup/September2020


