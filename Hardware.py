import serial

def dispense_items(data):
    # Configure the serial port
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace '/dev/ttyUSB0' with your actual serial port
    ser.timeout = 1  # Set the timeout value (in seconds)

    try:
        # Open the serial port
        if not ser.is_open:
            ser.open()

        data+="\n"    

        # Send the data to the device
        ser.write(data.encode())

        # Wait for a response (if expecting one)
        response = None
        while not response:
            response = ser.readline().decode().strip()
        
        print("Response:", response)

    except serial.SerialException as e:
        print("Serial port error:", str(e))

    finally:
        # Close the serial port
        if ser.is_open:
            ser.close()
