# WEATHER GLIDER
This weather monitoring glider collects real-time temperature, humidity, and orientation data using an ESP32, DHT22, and MPU6050. Unlike weather balloons, it’s reusable, cost-effective, and can cover targeted paths. Data is transmitted over Wi-Fi and saved as comma-separated value (CSV) files for later analysis. The system includes onboard sensors, a custom-built glider, and live graph plotting via Python, making it ideal for short-range atmospheric research.

## Components Used:

      🧠 ESP32 – Wi-Fi enabled microcontroller
    
      🌡️ DHT22 – Temperature & Humidity Sensor
    
      🧭 MPU6050 – Accelerometer & Gyroscope
      
      🔋 Li-Po Battery – Power source
      
      ✈️ Custom-built Glider – Foam-based, lightweight, aerodynamic

## Key Features:

      📡 Wireless data transmission in Access Point (AP) mode
      
      📁 Real-time logging to timestamped CSV files
      
      📊 Live graph plotting using Python (matplotlib)
      
      🔁 Reusable system for multiple flight tests
      
      📉 Cost-effective compared to traditional weather balloons

## Sample CSV Data:

      Time (s),Ax,Ay,Az,Temp (C),Humidity (%)
      22.974,1856.0,-796.0,15348.0,24.4,56.9
      23.693,1948.0,-740.0,15232.0,23.9,54.5
      24.814,1944.0,-680.0,15228.0,23.9,54.5
      30.541,-2636.0,-3168.0,14244.0,23.9,54.6
      34.83,1272.0,244.0,15324.0,23.9,54.7
      36.875,-5240.0,8156.0,12676.0,23.9,54.8
      40.965,-2200.0,6792.0,13572.0,23.9,55.0
      46.075,-2860.0,-3756.0,13808.0,23.8,55.0
      48.018,3904.0,-2852.0,14848.0,23.8,55.0
      51.496,1928.0,1104.0,15068.0,23.8,55.1

## How To Use:

 - Install the necessary libraries on your Arduino IDE
 - Compile and upload the C++ code on your ESP32.
 - Turn on the power source to the ESP32.
 - Connect to the Wi-Fi network "Glider_AP" using the password set in the script and run the Python script.

## Author

- [@Naman Soin](https://www.github.com/spacebar0) - Hardware, Code, Data Analysis & Flight Testing
