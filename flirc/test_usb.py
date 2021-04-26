import usb.core
import usb.util
import time
import sys

USB_IF      = 0 # Interface
USB_TIMEOUT = 1000 # Timeout in MS

USB_VENDOR  = 0x20a0
USB_PRODUCT = 0x0006

dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

# was it found?
if dev is None:
    raise ValueError('Device not found')

if dev.is_kernel_driver_active(USB_IF) is True:
    print("detaching")
    dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

# set the active configuration. With no arguments, the first
# configuration will be the active one
# dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()

intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
ep.write('reboot')

# this also works to set the endpoint
# ep = dev[0][(0,0)][1]

print("dev:", dev)
print("endpoint:", ep)

msg = 'test'
assert dev.write(1, msg, 100) == len(msg)
ret = dev.read(0x81, len(msg), 5000)
sret = ''.join([chr(x) for x in ret])
assert sret == msg

sys.exit()

while True:
    control = None

    try:
        control = dev.read(ep.bEndpointAddress, ep.wMaxPacketSize, USB_TIMEOUT)
        print(control)
    except:
        pass

    time.sleep(1.0) # Let CTRL+C actually exit
