nmcli con add type wifi ifname "${wnic}" con-name EXAMPLE-Campus ssid EXAMPLE-Campus
nmcli con edit id EXAMPLE-Campus
nmcli> set ipv4.method auto
nmcli> set 802-1x.eap peap
nmcli> set 802-1x.phase2-auth mschapv2
nmcli> set 802-1x.identity bgstack15
nmcli> set 802-1x.password REDACTED
nmcli> set 802-11-wireless-security.key-mgmt wpa-eap
nmcli> set 802-11-wireless-security.wep-tx-keyidx 0
nmcli> set 802-11-wireless-security.auth-alg open
nmcli> save
nmcli> activate

