import dial_discover
import json

ds = dial_discover.discover_devices()

d = ds[0]

f = open("/tmp/ChromecastDevices",'w')
json.dump(ds,f)
f.close()


#dial_rest.launch_app(d,"YouTube")
#dial_rest.launch_app(d,"e7689337-7a7a-4640-a05a-5dd2bd7699f9_1")

#dial_rest.app_status(d,"e7689337-7a7a-4640-a05a-5dd2bd7699f9_1")


# Add Argument Parser for testing
