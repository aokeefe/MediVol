#!/bin/sh
# Dropbox setup on a headless Ubuntu Server
# Script written by Jesse B. Hannah (http://jbhannah.net) <jesse@jbhannah.net>
# Based on http://wiki.dropbox.com/TipsAndTricks/UbuntuServerInstall

###
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

# All of the following commands are run as root, or run this script as root.

# Download and extract the Dropbox daemon itself into a system location
sudo mkdir -p /usr/local/dropbox
sudo wget -qO- http://www.dropbox.com/download/?plat=lnx.x86 | tar xz --strip 1 -C /usr/local/dropbox

sudo useradd -r -m -d /etc/dropbox -U -s /bin/false dropbox
sudo chown dropbox.dropbox /etc/dropbox
sudo chmod 700 /etc/dropbox

sudo su -l dropbox -s /bin/bash
umask 0027
/usr/local/dropbox/dropboxd
# Open the URL dropboxd gives you in a browser to link it to your account
# Exit dropboxd with C-c AFTER you've done this
exit
# If you're OCD, you can remove everything from /etc/dropbox except .dropbox and Dropbox now

# For Ubuntu 9.10 and later, this is an upstart script for starting and stopping dropbox with
# `start dropbox` and `stop dropbox`. Users of earlier Ubuntu or non-upstart distros, see
# http://wiki.dropbox.com/TipsAndTricks/TextBasedLinuxInstall for startup service configuration.
sudo cat <<EOF | sed -e "s,%,$,g" >/etc/init/dropbox.conf
# Dropbox upstart script

description "Dropbox"
author      "Jesse B. Hannah <jesse@jbhannah.net>"

start on runlevel [2345]
stop on runlevel [!2345]

respawn

env HOME=/etc/dropbox
umask 0027

pre-start script
    [ ! -e "$HOME/.dropbox/command_socket" ] || rm $HOME/.dropbox/command_socket
    [ ! -e "$HOME/.dropbox/iface_socket" ]   || rm $HOME/.dropbox/iface_socket
    [ ! -e "$HOME/.dropbox/unlink.db" ]      || rm $HOME/.dropbox/unlink.db
end script

script
    export LANG=en_US.UTF-8
    exec su -s /bin/sh -c /usr/local/dropbox/dropbox dropbox
end script
EOF

sudo start dropbox