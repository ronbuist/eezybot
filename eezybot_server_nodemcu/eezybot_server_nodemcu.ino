// Server for EEZYbotARM mk I, to run on NodeMCU.

#include <ESP8266WiFi.h>        // WiFi Library
#include <WebSocketsServer.h>   // Web socket server library
#include <Servo.h>              // Servo library

#define LED D4                  // Led in NodeMCU (v3).
#define WSPort 8000             // Websocket Port

//#define DEBUG                   // Define this to switch on debugging

#ifdef DEBUG
 #define DEBUG_PRINT(x)  Serial.println (x)
#else
 #define DEBUG_PRINT(x)
#endif

const char* WiFi_hostname = "eezybot01";
const char* ssid = "wifi_ssid";            // Name of WiFi Network
const char* password = "wifi_password";    // Password of WiFi Network

bool nodeLedOn;
Servo eezyServos[5];
int servoPins[5] = {D0,D1,D5,D6,D7};
int armPosition[3] = {90,90,90};

// Initialize WebSocket server
WebSocketsServer webSocket = WebSocketsServer(WSPort);

void setup() {

  Serial.begin(115200);
  delay(10);

  pinMode(LED, OUTPUT);    // NodeMCU LED pin as output.
  nodeLedOn = false;

  // Connect to WiFi network
  WiFi.hostname(WiFi_hostname);
  WiFi.mode(WIFI_STA); //Indicate to act as wifi_client only.
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  // Wait until connected to WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
    switchNodeMCULed();
  }

  // Confirmation that WiFi is connected
  Serial.println("");
  Serial.print("WiFi connected. Local IP address is ");
  Serial.println(WiFi.localIP());
  nodeMCULedOn(true);

  // Initialize websocket
  DEBUG_PRINT("Opening Websocket server...");
  webSocket.begin(); 
  DEBUG_PRINT("Setting event handler...");
  webSocket.onEvent(webSocketEvent); 
  DEBUG_PRINT("Websocket ready.");
}

void loop() {
  // Handle websocket
  webSocket.loop();
}

void switchNodeMCULed() {
  if (nodeLedOn) {
    // NodeMCU led is on. Switch it off.
    digitalWrite(LED, HIGH);
  } else {
    // NodeMCU led is off. Switch it on.
    digitalWrite(LED, LOW);    
  }
  nodeLedOn = !nodeLedOn;
}

void nodeMCULedOn(bool ledOn) {
  if (ledOn) {
    // Switch NodeMCU led on.
    digitalWrite(LED, LOW);
  } else {
    // Switch NodeMCU led off.
    digitalWrite(LED, HIGH);    
  }
  nodeLedOn = ledOn;
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length){

  String cmdLine("");
  String params[5];
  String gatePos;
  int delimLoc;
  int pos;
  int servo;
  int newArmPosition[3];
  int armDistance[3];
  int armSpeed;
  int maxDistance;

  // We are only interested in messages of type TEXT...
  if (type == WStype_TEXT){

    // Get everything that was passed into a single string.
    cmdLine = String((char*) payload);
    DEBUG_PRINT("Command line received: ");
    DEBUG_PRINT(cmdLine);

    // Now get the actual command and the parameters
    delimLoc = cmdLine.indexOf(' ');            // finds location of first space
    if (delimLoc == -1) {
      params[0] = cmdLine;
    } else {
      pos = 0;
      while (delimLoc != -1) {
        params[pos] = cmdLine.substring(0, delimLoc);
        cmdLine = cmdLine.substring(delimLoc+1);    // keep the rest; continue with that
        delimLoc = cmdLine.indexOf(' ');
        pos++;
      }
      params[pos] = cmdLine;
    }
    DEBUG_PRINT("Command is ");
    DEBUG_PRINT(params[0]);

    // switch the Node MCU led.
    switchNodeMCULed();

    // Handle the command.
    if (params[0] == "init") {
      // Connect to all the servos and set them to neutral
      for (int i = 0; i <= 4; i++) {
        eezyServos[i].attach(servoPins[i]);
        eezyServos[i].write(90);
      }
      for (int i = 0; i <= 2; i++) {
        armPosition[i] = 90;
      }
      
    }

    // setneutral command
    if (params[0] == "setneutral") {
      for (int i = 0; i <= 4; i++) {
        eezyServos[i].write(90);
      }
    }

    // setservo command
    if (params[0] == "setservo") {
      servo = params[1].toInt() - 1;
      pos = 90 - params[2].toInt();
      eezyServos[servo].write(pos);
    }

    // setgate command
    if (params[0] == "setgate") {
      gatePos = params[1];
      if (gatePos == "open") {
        eezyServos[4].write(90);
      } else {
        eezyServos[4].write(10);
      }
    }

    // setgripper command
    if (params[0] == "setgripper") {
      pos = 180 - params[1].toInt();
      eezyServos[3].write(pos);
    }

    // setarm command
    if (params[0] == "setarm") {
      for (int i = 0; i <= 2; i++) {
        newArmPosition[i] = params[i+1].toInt();
      }
      armSpeed = params[4].toInt();

      // Calculate distance
      maxDistance = 0;
      for (int i = 0; i <= 2; i++) {
        armDistance[i] = armPosition[i] - newArmPosition[i];
        armDistance[i] = abs(armDistance[i]);
        if (armDistance[i] > maxDistance) {
          maxDistance = armDistance[i];
        }
      }

      // Move the three servos to their new position
      for (int d = 0; d <= maxDistance; d++) {
        for (int i = 0; i <= 2; i++) {
          if (armPosition[i] < newArmPosition[i]) {
            armPosition[i]++;
            eezyServos[i].write(armPosition[i]);
          } else {
            if (armPosition[i] > newArmPosition[i]) {
              armPosition[i]--;
              eezyServos[i].write(armPosition[i]);
            }
          }
        }
        delay(100-armSpeed);
      }
      webSocket.broadcastTXT("OK");
    }
    
  } 
}
