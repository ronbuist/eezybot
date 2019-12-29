# eezybot
Software for the EEZYbotARM MK1

In the directory eezybot_server_nodemcu you will find the Arduino code for the EEZYbotARM MK1 server. Connect the servos as follows:

* Pin D0 = move arm left/right
* Pin D1 = move arm up/down
* Pin D5 = move arm forward/backward
* Pin D6 = gripper
* Pin D7 = gate

I have used a NodeMCU v2 and placed that on a base board (see https://www.aliexpress.com/item/4000219252923.html). The base board allows you to connect 1 5V power source and hook everything up to the base board. I also used a level shifter (like [this one](https://www.aliexpress.com/item/32856524741.html)) because the servos don't seem to like the 3.3v that the NodeMCU supplies on the digital output pins. The level shifter will ensure the PWM signal is 5v.
