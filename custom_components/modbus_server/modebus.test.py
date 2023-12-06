from pymodbus.server import StartAsyncTcpServer, ServerStop
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
import asyncio
from homeassistant.core import HomeAssistant


store = ModbusSlaveContext(di=ModbusSequentialDataBlock(0, [0]*100))

    # Создайте контекст сервера Modbus
context = ModbusServerContext(slaves=store, single=True)
loop = asyncio.get_event_loop()


async def start_modbus_server():
    # Запустите сервер Modbus
    loop = asyncio.get_event_loop()
    server = await StartAsyncTcpServer(context, framer=ModbusRtuFramer, address=(host, port), loop=loop, custom_functions=[handle_modbus_event])

def handle_modbus_event(request):
    print(f"Received Modbus request: {request}")

start_modbus_server()
