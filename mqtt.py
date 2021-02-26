import random
import time
from paho.mqtt import client as mqtt_client

class Mqtt:
    def __init__(self):
        self.broker = '192.168.1.118'
        self.port = 1883
        self.topic = "home-assistant/dylan/mood"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.username = 'dylanMQTT'
        self.password = 'letsgoBucks'

        self.temp = '0'

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                client.connected_flag = True  # set flag
            else:
                print("Failed to connect, return code %d\n", rc)
                client.connected_flag = False  # set flag
        # Set Connecting Client ID
        client = mqtt_client.Client(self.client_id)
        client.connected_flag = False  # set flag
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def on_disconnect(client, userdata, rc):
        logging.info("disconnecting reason  "  +str(rc))
        client.connected_flag=False
        client.disconnect_flag=True

    def publish(self,client):
        msg_count = 0
        while True:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = client.publish(self.topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")
            msg_count += 1

    def subscribe(self,client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.temp = msg.payload.decode()
            # print(type(temp))
            # print(temp)

        client.subscribe(self.topic)
        client.on_message = on_message

    # def run(self):
    #     # print(temp)
    #     client = self.connect_mqtt()
    #     # client.loop_start()
    #     # publish(client)
    #     while 1:
    #         try:
    #             temp_old = self.temp
    #             self.subscribe(client)
    #             client.loop(.1)
    #
    #         except:
    #             if client.connected_flag==False:
    #                 client = self.connect_mqtt()
    #         if temp_old != self.temp:
    #             print(self.temp)
    #             temperature = round(float(self.temp))
    #             print(temperature)

# Main function
if __name__ == "__main__":
    my_mqtt = Mqtt()
    temp_old = '0'
    client = my_mqtt.connect_mqtt()
    while 1:
        my_mqtt.subscribe(client)
        client.loop_start()
        if(my_mqtt.temp != '0'):
            mqtt_temp = round(float(my_mqtt.temp))
            if temp_old != my_mqtt.temp:
                print(mqtt_temp)
        temp_old = my_mqtt.temp
        client.loop_stop()














