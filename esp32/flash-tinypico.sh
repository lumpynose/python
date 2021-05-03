# baud rates: 115200, 230400, 460800, 921600

PORT="${PORT:-/dev/ttyUSB0}"
BAUD="${BAUD:-115200}"
BIN="${BIN:-tinypico-20210418-v1.15.bin}"

if esptool.py --chip esp32 --port ${PORT} --baud 115200 erase_flash
then
    esptool.py \
	--chip esp32 \
	--port ${PORT} \
	--baud ${BAUD} \
	write_flash -z \
	--flash_mode dio \
	--flash_freq 80m \
	--flash_size detect \
	0x1000 ${BIN}
fi
