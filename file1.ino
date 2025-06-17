#include <WiFi.h>
#include <Wire.h>
#include <MPU6050.h>
#include <DHT.h>

// ==== CONFIG ====
const char* ssid = "Glider_AP";
const char* password = "12345678";

// DHT Sensor settings
#define DHTPIN 4         // GPIO4 (change if needed)
#define DHTTYPE DHT22    // or DHT22
DHT dht(DHTPIN, DHTTYPE);

WiFiServer server(80);
MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();
  dht.begin();

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 failed");
    while (1);
  }

  WiFi.softAP(ssid, password);
  server.begin();
  Serial.println("Access Point Started");
  Serial.println(WiFi.softAPIP());
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    while (client.connected()) {
      int16_t ax, ay, az;
      mpu.getAcceleration(&ax, &ay, &az);
      unsigned long time_ms = millis();

      float temp = dht.readTemperature();
      float hum = dht.readHumidity();

      // Handle failed reads
      if (isnan(temp) || isnan(hum)) {
        temp = 0.0;
        hum = 0.0;
      }

      // Send all values in one line
      String data = String(time_ms) + "," + String(ax) + "," + String(ay) + "," + String(az) + "," + String(temp) + "," + String(hum) + "\n";
      client.print(data);

      delay(100);  // ~10Hz
    }
    client.stop();
  }
}
