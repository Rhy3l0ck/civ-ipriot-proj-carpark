from parking_lot import ParkingLot


def get_message(client, userdate, message):
    msg = message.payload.decode('UTF-8')
    print(msg)


pl = ParkingLot()
pl.create_mqtt_client()

if __name__ == 'main':
    pl = ParkingLot()
    pl.create_mqtt_client()
    print(pl.mqtt_client.name)

    pl.mqtt_client.client.loop_forever()
