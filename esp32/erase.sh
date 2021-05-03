# baud rates: 115200, 230400, 460800, 921600

PORT="${PORT:-/dev/ttyUSB0}"
BAUD="${BAUD:-115200}"

esptool.py --chip esp32 --baud 115200 --port ${PORT} erase_flash
