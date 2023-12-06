from pymodbus.server import StartAsyncTcpServer, ServerStop
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
import asyncio
from homeassistant.core import HomeAssistant

from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    EVENT_HOMEASSISTANT_STOP,
    EVENT_HOMEASSISTANT_START
)

import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "modbus_server"


def setup(hass: HomeAssistant, config):
    # Получите IP-адрес и порт из конфигурации
    host = config[DOMAIN][CONF_HOST]
    port = config[DOMAIN][CONF_PORT]

    # Создайте хранилище данных Modbus
    store = ModbusSlaveContext(di=ModbusSequentialDataBlock(0, [0]*100))

    # Создайте контекст сервера Modbus
    context = ModbusServerContext(slaves=store, single=True)

    async def start_modbus_server(event):
        # Запустите сервер Modbus
        _LOGGER.error("Starting Modbus server")
        server = await StartAsyncTcpServer(context, framer=ModbusRtuFramer, address=(host, port), custom_functions=[handle_modbus_event])

    async def stop_modbus_server(event):
        # Остановите сервер Modbus
        _LOGGER.error("Stopping Modbus server")
        await ServerStop()

    # Запустите сервер Modbus, когда Home Assistant начинает работать
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, start_modbus_server)

    # Остановите сервер Modbus, когда Home Assistant останавливает работу
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, stop_modbus_server)

    # Обработчик событий Modbus
    def handle_modbus_event(request):
        _LOGGER.error(f"Received Modbus request: {request}")

    # Добавьте обработчик событий в контекст сервера

    return True