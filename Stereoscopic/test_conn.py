import os

import serial

newline = os.linesep

# Replace the port path with the actual device path on your system
port_path = '/dev/ttyUSB0'
serial_port = serial.Serial(port_path, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)

# Check if the port is open
if serial_port.is_open:
    print(f"Serial port {serial_port.name} is open.")

    # String to write to the serial port
    command = "set2d3d 1" + newline

    # Convert the string to bytes and write to the serial port
    serial_port.write(command.encode('utf-8'))

    print(f"Command '{command}' written to the serial port.")

    # Read the response from the serial port
    response = serial_port.read_until('\r\n\r\n'.encode('utf-8'))

    # Check if the response contains "OK"
    if b"OK" in response:
        print("Success (received \"OK\" as response)")
    else:
        print(f"Failure. Response: {response.decode('utf-8')}")

    # Close the serial port when done
    serial_port.close()
else:
    print(f"Failed to open serial port {port_path}.")

