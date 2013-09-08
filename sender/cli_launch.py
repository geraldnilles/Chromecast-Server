import dial_rest
import json

f = open("/tmp/ChromecastDevices",'r')
ds = json.load(f)
f.close()
print ds

#dial_rest.launch_app(d,"YouTube")
dial_rest.launch_app(ds[0],"e7689337-7a7a-4640-a05a-5dd2bd7699f9_1")

#dial_rest.app_status(d,"e7689337-7a7a-4640-a05a-5dd2bd7699f9_1")


# Add Argument Parser for testing

