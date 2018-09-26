# SMS-Bot
An SMS bot that obtains information you want without the need for a strong network connection.

### Program Overview
This program is an SMS bot built using Python and Twilio API [ https://www.twilio.com/ ], which allows you to send a Twilio 
phone number messages and get answers back. The Twilio library allows for you to send and receive messages, while Flask
[ http://flask.pocoo.org/ ] allows your program to connect to a local server. Furthermore, Ngrok [ https://ngrok.com/ ] 
will connect your local host running program to the World Wide Web and will provide an http address. Twilio will use this address to send you incoming messages.

### Program Execution
pip install -r requirements.txt </br >
python run_application.py </br >
ngrok http [port_number] </br >

Copy one of the forwarding addresses into your Twilio dashboard where it says "A MESSAGE COMES IN".  </br >

Text your Twilio number with one of the following commands and you should get a response:
  
  WIKI ["insert wikipedia request"] </br >
  WEATHER ["insert city name"] </br >
  WOLFRAM ["insert wolframalpha request"] </br >