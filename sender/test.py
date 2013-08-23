import dial_discover
import dial_rest


ds = dial_discover.discover_devices()

d = ds[0]

print d

dial_rest.launch_app(d,"YouTube")

dial_rest.app_status(d,"YouTube")
