from flask import Flask, render_template, jsonify
from threading import Thread
import asyncio
from bleak import BleakClient

app = Flask(__name__) # create an instance of the Flask class

ble_data = {}

async def ble_read():
    address = "30:30:F9:18:0F:D1" # Device address
    char_uuid = "beb5483e-36e1-4688-b7f5-ea07361b26a8" # Characteristic UUID to read from

    async with BleakClient(address) as client:
        while True:
            value = await client.read_gatt_char(char_uuid)
            decoded_value = value.decode('utf-8').strip() # Decode the bytearray to a string
            parts = decoded_value.split() # Split the string into a list of strings separated by space
            data_dict = {"x": parts[0], "y": parts[1], "z": parts[2]} if len(parts) >= 3 else {} # Create a dictionary from the list
            ble_data['joystick'] = data_dict
            # print(ble_data)
            await asyncio.sleep(0.1)

        # characteristic = (await client.get_services())[0].characteristics[0]
        # value = await client.read_gatt_char(characteristic.uuid)
        # print(type(client))

def start_ble_read():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ble_read())


@app.route('/') # use the route() decorator to tell Flask what URL should trigger our function
def index():
    return render_template('index.html')


@app.route('/get_raw')
def getRawData():
    # print(f'{ble_data}')
    return jsonify(ble_data)


if __name__ == '__main__':
    thread = Thread(target=start_ble_read)
    thread.start()
    app.run() # run the application

