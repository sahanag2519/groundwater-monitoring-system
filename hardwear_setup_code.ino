#include <WiFi.h>
#include <HTTPClient.h>

// =====================================================
// PIN DEFINITIONS
// =====================================================

#define TDS_PIN 34
#define TRIG_PIN 23
#define ECHO_PIN 18


// =====================================================
// WATER TANK / WELL DEPTH
// =====================================================

// Total depth of your prototype in centimeters
const float WELL_DEPTH_CM = 5.0;


// =====================================================
// WIFI
// =====================================================

const char* WIFI_SSID = "Max";
const char* WIFI_PASSWORD = "maxiii_007";

// IP address of the laptop running Flask
// Example:
// http://10.25.91.247:5000/data

const char* serverURL = "http://10.25.91.247:5000/data";


// =====================================================
// TDS CALCULATION
// =====================================================

// Assuming water temperature is 25°C for now
const float WATER_TEMPERATURE = 25.0;


// =====================================================
// SEND DATA TO FLASK
// =====================================================

void sendData(float waterLevel, float tdsValue)
{
    // Check Wi-Fi connection
    if (WiFi.status() == WL_CONNECTED)
    {
        HTTPClient http;

        // Connect to Flask server
        http.begin(serverURL);

        // Tell Flask that we are sending JSON
        http.addHeader("Content-Type", "application/json");


        // -------------------------------------------------
        // CREATE JSON DATA
        // -------------------------------------------------

        String jsonData = "{";

        jsonData += "\"village\":\"Village A\",";
        jsonData += "\"well\":\"Well 1\",";
        jsonData += "\"water_level\":";
        jsonData += String(waterLevel, 2);
        jsonData += ",";

        jsonData += "\"tds\":";
        jsonData += String(tdsValue, 0);

        jsonData += "}";


        // -------------------------------------------------
        // DISPLAY DATA BEING SENT
        // -------------------------------------------------

        Serial.println();
        Serial.println("Sending data to Flask:");
        Serial.println(jsonData);


        // -------------------------------------------------
        // SEND HTTP POST REQUEST
        // -------------------------------------------------

        int httpResponseCode = http.POST(jsonData);

        Serial.print("HTTP Response Code: ");
        Serial.println(httpResponseCode);


        // -------------------------------------------------
        // CHECK RESPONSE
        // -------------------------------------------------

        if (httpResponseCode > 0)
        {
            Serial.println("Data sent successfully!");

            String response = http.getString();

            Serial.println("Flask response:");
            Serial.println(response);
        }
        else
        {
            Serial.print("Error sending data: ");
            Serial.println(httpResponseCode);
        }


        // Close HTTP connection
        http.end();
    }
    else
    {
        Serial.println("Wi-Fi disconnected!");
    }
}


// =====================================================
// READ TDS AND CALCULATE PPM
// =====================================================

float readTDS()
{
    // Read raw ADC value from TDS sensor
    int rawADC = analogRead(TDS_PIN);


    // Convert ADC value to voltage
    float voltage = (rawADC * 3.3) / 4095.0;


    // -------------------------------------------------
    // TEMPERATURE COMPENSATION
    // -------------------------------------------------

    float compensationCoefficient =
        1.0 + 0.02 * (WATER_TEMPERATURE - 25.0);

    float compensatedVoltage =
        voltage / compensationCoefficient;


    // -------------------------------------------------
    // TDS CALCULATION
    // -------------------------------------------------

    float tdsValue =
        (133.42 * compensatedVoltage * compensatedVoltage * compensatedVoltage
        - 255.86 * compensatedVoltage * compensatedVoltage
        + 857.39 * compensatedVoltage)
        * 0.5;


    // Prevent negative values
    if (tdsValue < 0)
    {
        tdsValue = 0;
    }


    return tdsValue;
}


// =====================================================
// READ ULTRASONIC SENSOR
// =====================================================

float readDistanceCM()
{
    // Send trigger pulse
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);

    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);

    digitalWrite(TRIG_PIN, LOW);


    // Measure echo pulse duration
    long duration = pulseIn(
        ECHO_PIN,
        HIGH,
        30000
    );


    // If no echo is received
    if (duration == 0)
    {
        return -1;
    }


    // Calculate distance in centimeters
    float distance =
        duration * 0.0343 / 2.0;


    return distance;
}


// =====================================================
// SETUP
// =====================================================

void setup()
{
    Serial.begin(115200);


    // -------------------------------------------------
    // ULTRASONIC SENSOR
    // -------------------------------------------------

    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);


    // -------------------------------------------------
    // ESP32 ADC
    // -------------------------------------------------

    analogReadResolution(12);

    analogSetPinAttenuation(
        TDS_PIN,
        ADC_11db
    );


    // -------------------------------------------------
    // STARTUP MESSAGE
    // -------------------------------------------------

    Serial.println();
    Serial.println("================================");
    Serial.println("  Groundwater Monitoring System");
    Serial.println("================================");


    // -------------------------------------------------
    // CONNECT TO WI-FI
    // -------------------------------------------------

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    Serial.print("Connecting to Wi-Fi");


    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }


    Serial.println();
    Serial.println("Wi-Fi connected!");

    Serial.print("ESP32 IP: ");
    Serial.println(WiFi.localIP());
}


// =====================================================
// MAIN LOOP
// =====================================================

void loop()
{
    // =================================================
    // READ TDS
    // =================================================

    int rawTDS = analogRead(TDS_PIN);


    // Calculate sensor voltage
    float voltage =
        (rawTDS * 3.3) / 4095.0;


    // Calculate TDS in ppm
    float tdsValue = readTDS();


    // =================================================
    // READ WATER LEVEL
    // =================================================

    float distance = readDistanceCM();

    float waterLevel = -1;


    if (distance >= 0)
    {
        // Calculate water level
        waterLevel =
            WELL_DEPTH_CM - distance;


        // Prevent negative water level
        if (waterLevel < 0)
        {
            waterLevel = 0;
        }


        // Prevent water level exceeding tank depth
        if (waterLevel > WELL_DEPTH_CM)
        {
            waterLevel = WELL_DEPTH_CM;
        }
    }


    // =================================================
    // DISPLAY SENSOR DATA
    // =================================================

    Serial.println();
    Serial.println("-----------------------------------");

    Serial.print("TDS Raw ADC : ");
    Serial.println(rawTDS);

    Serial.print("TDS Voltage : ");
    Serial.print(voltage, 3);
    Serial.println(" V");

    Serial.print("TDS : ");
    Serial.print(tdsValue, 0);
    Serial.println(" ppm");


    // Display only WATER LEVEL
    if (waterLevel >= 0)
    {
        Serial.print("Water Level : ");
        Serial.print(waterLevel, 1);
        Serial.println(" cm");
    }
    else
    {
        Serial.println("Water Level : No reading");
    }

    Serial.println("-----------------------------------");


    // =================================================
    // SEND DATA TO FLASK
    // =================================================

    if (waterLevel >= 0)
    {
        // Convert centimeters to metres by scaling
        float waterLevelMeters =
            waterLevel ;


        sendData(
            waterLevelMeters,
            tdsValue
        );
    }


    // =================================================
    // WAIT 5 SECONDS
    // =================================================

    delay(5000);
}