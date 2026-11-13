
using System.IO.Ports;

var port = new SerialPort("COM3", 9600, Parity.None, 8, StopBits.One);

port.Open();

string response = port.ReadLine();

Console.WriteLine(response);

var parts = response.Split(';');

double speed = double.Parse(parts[0].Replace("SPEED=", string.Empty));
double torque = double.Parse(parts[1].Replace("TORQUE=", string.Empty));

Console.WriteLine($"SPEED = {speed}, TORQUE = {torque}");

