#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

#define DHT11PIN 13
DHT dht(DHT11PIN, DHT11);

const char* ssid = "OPPO"; // Ganti dengan SSID WiFi yang digunakan
const char* password = "i5nab6gx"; // Ganti dengan password WiFi yang digunakan
const char* server_url = "http://192.168.117.44:5000/sensor"; // Ganti dengan IP dan port server yang digunakan

unsigned long lastMsg = 0;
float temp = 0;
float hum = 0;

void startWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to the WiFi network");
}

void setup() {
  Serial.begin(115200);
  Serial.println("Sensor is starting...");
  startWifi();
  dht.begin();
  Serial.println("Setup completed. Sensor is ready");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    startWifi();
  }

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    if (isnan(temp) || isnan(hum)) {
      Serial.println("Failed to read from DHT sensor");
      return;
    }

    HTTPClient http;
    http.begin(server_url);
    http.addHeader("Content-Type", "application/json");
    String payload = "{\"temperature\": " + String(temp, 1) + ", \"humidity\": " + String(hum, 1) + "}";
    
    Serial.print("Sending data to server: ");
    Serial.println(payload);
    int httpResponseCode = http.POST(payload);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      Serial.print("Response from server: ");
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();

    Serial.print("Temperature: ");
    Serial.print(temp);
    Serial.print(" C, Humidity: ");
    Serial.print(hum);
    Serial.println(" %");
  }
}