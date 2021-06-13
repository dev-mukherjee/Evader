#!/bin/bash
arch=$(head -n1 /etc/issue | cut -d' ' -f1)

update() {
    apt update -y
    apt full-upgrade -y
}
installation() {
    apt-get install -y wine
    dpkg --add-architecture i386
    apt install metasploit-framework -y
    apt install mingw-w64
    apt install gcc-mingw-w64-i686-win32
    apt install python3
    apt install python3-pip
    pip install hashlib
}

if [ $(whoami) = 'root' ]; then
    if [ "$arch" = "Kali" ]; then
        main() {
            update
            installation
            chmod +x evader.py
        }
    else
        echo "You are not using KALI LINX,
        this tool is for kali linux still,now.
        Update will bring other distro support"
        exit
    fi
else
    echo "You are not root, run it as root"
    exit
fi
