## Welcome
This project started as a way to use the command line to connect to a wireless network.
The original sample information for campus.wifi was captured from "nmcli con show campus" after using the xfce nm gui.

## Wifi file
For variable `ifname` the `$WNIC` means do a lookup of the wireless network card device name.

For variables `identity` and `password`, the value "file:///etcetera" means it will open up that file. The type of file used is the same as for fstab or mount:

    username=alice
    password=filesharepw
