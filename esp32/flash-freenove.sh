# baud rates: 115200, 230400, 460800, 921600

PORT="${PORT:-/dev/ttyUSB0}"
BAUD="${BAUD:-115200}"
BIN="${BIN:-esp32spiram-idf4-20210202-v1.14.bin}"

if esptool.py --chip esp32 --port ${PORT} --baud ${BAUD} erase_flash
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
