# baud rates: 115200, 230400, 460800, 921600

PORT="${PORT:-/dev/ttyUSB0}"
BAUD="${BAUD:-750000}"
BIN="${BIN:-esp32spiram-idf4-20210202-v1.14.bin}"
#BIN="${BIN:-firmware.bin}"

# --flash_size detect 0x1000 \

if esptool.py --chip esp32 --port "${PORT}" --baud 115200 erase_flash
then
    esptool.py \
	--chip esp32 \
	--port ${PORT} \
	--baud ${BAUD} \
	--before default_reset \
	write_flash -z \
	--flash_mode dio \
	--flash_freq 80m \
	--flash_size detect \
	0x1000 ${BIN}
fi
