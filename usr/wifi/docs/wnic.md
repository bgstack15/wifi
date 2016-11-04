# Reference
# this works in shell
wnic=$( iw dev | grep -iE "Interface" | awk '{print $2}' )

