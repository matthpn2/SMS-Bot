from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import wikipedia, json, datetime, urllib.request, requests

# Set up FLASK to connect this code to the local host, later to be connected to the Internet through NGROK
app = Flask(__name__)

@app.route('/', methods = ['POST'])
def sms():
    '''
        When a POST request is sent to the local host through NGROK ( which creates a tunnel to the Web ), this
        code will run. The TWILIO service sends the POST request, such that this code will run when a message is
        sent over SMS to the TWILIO number.
    '''
    # Get text in message sent and send text to getReply method, where it'll query the String and formulate a response
    message = request.form['Body']
    reply_text = getReply(message)

    # Create a TWILIO response object to send a reply back and text back a response
    response = MessagingResponse()
    response.message('Hello there!\n\n' + reply_text)

    return str(response)

def getReply(message):
    '''
        This method will simply look through the text message body and figure out the type of information desired. IT will
        then get the information from different APIs and return a response. Assuming the text message will be formatted as
        "keyword request", a simple format used to identify what is requested in the message.
    '''
    # For easier handling, make the message lower case and strip it of spaces
    message = message.lower().strip()

    answer = ""
    if "wiki" in message:
        # Remove the keyword "wiki" from the message
        message = removeKeyWord(message, "wiki")

        try:
            answer = wikipedia.summary(message)

        except:
            answer = "Request was NOT found using Wikipedia. Please be more specific."
    
    elif "weather" in message:
        # Remove the keyword "weather" from the message
        message = removeKeyWord(message, "weather")

        try:
            data = fetchWeatherData(message)
            answer = outputWeatherData(data)

        except:
            answer = "There was an Open Weather Map Error. Please try again."

    elif "wolfram" in message:
        # Remove the keyword "wolfram" from the message
        message = removeKeyWord(message, "wolfram")

        try:
            data = fetchWolframData(message)
            answer = outputWolframData(data)

        except:
            answer = "Request was NOT found using Wolfram Alpha. Please be more specific."
        
    else:
        # If the message contains NO keyword, display a help prompt to identify
        answer = "\nPlease try again; no keywords were recognized. These are the commands you may use: \n\nWIKI [\"wikipedia request\"] \nWEATHER [\"city name\"] \nWOLFRAM [\"wolframalpha request\"]\n"

    if len(answer) > 1500:
        answer = answer[0:1500] + "..."

    return answer

def removeKeyWord(message, keyword):
    '''
        This method edits input text. For example, if you send the message "wolfram calories in bread" or "calories in
        bread wolfram", the progrma will recognize "wolfram" and call this function to change the text to "calroies in
        brea" which will then be sent to wolfram. 
    '''
    if message.endswith(keyword):
        message = message[:-len(keyword)].strip()

    elif message.startswith(keyword):
        message = message[len(keyword):].strip()
    
    return message

def convertTime(time):
    '''
        This method gets the local date corresponding to the POSIX timestamp and converts it to the proper format of 
        "Hour:Minute [AM/PM]", where Hour and Minute are zero-padded decimal numbers.
    '''    
    return datetime.datetime.fromtimestamp(int(time)).strftime('%I:%M %p')

def fetchWeatherData(cityname):
    '''
        This method constructs the Open Weather Map URL, issues an HTTP request to build the URL and gets an HTTP response.
        From the HTTP response, a Python object representing the parsed JSON response is returned.
    '''
    base_weather_url = 'http://api.openweathermap.org/data/2.5/weather?q='
    weather_api_key = '70eaba6802492b0faeeff8e0d9a3344d'

    build_weather_url = base_weather_url + str(cityname) + '&mode=json&units=imperial&appid=' + weather_api_key

    response = urllib.request.urlopen(build_weather_url)
    json_text = response.read().decode(encoding = 'utf-8')
    response.close()

    return json.loads(json_text)

def outputWeatherData(data):
    '''
        This method pulls out all the necessary data from the previously obtained json data and returns a formatted string.
    '''
    cityname = data.get('name')
    country = data.get('sys').get('country')

    current_temp = str(data.get('main').get('temp'))
    sky_desc = data['weather'][0]['main']

    max_temp = str(data.get('main').get('temp_max'))
    min_temp = str(data.get('main').get('temp_min'))

    wind_speed = str(data.get('wind').get('speed'))
    wind_deg = data.get('deg')

    humidity = str(data.get('main').get('humidity'))
    cloudiness = str(data.get('clouds').get('all'))
    pressure = str(data.get('main').get('pressure'))

    sunrise = str(convertTime(data.get('sys').get('sunrise')))
    sunset = str(convertTime(data.get('sys').get('sunset')))
    latest_time = str(convertTime(data.get('dt')))

    temp_symbol = '\xb0' + 'F '

    answer = ( 'Current weather in {}, {}:'.format(cityname, country) + '\n' +  
               current_temp + temp_symbol + sky_desc + ' Skies\n' + 
               'Max Temp: {} {}, Min Temp: {} {}'.format(max_temp, temp_symbol, min_temp, temp_symbol) + '\n\n' +
               'Wind Speed: {}, Degree: {}'.format(wind_speed, wind_deg) + '\n' +
               'Humidity: {}'.format(humidity) + '\n' +
               'Cloudiness: {}'.format(cloudiness) + '\n' +
               'Pressure: {}'.format(pressure) + '\n' +
               'Sunrise at {}'.format(sunrise) + '\n' +
               'Sunset at {}'.format(sunset) + '\n\n' +
               'Last update from server at {}'.format(latest_time) )
               
    return answer

def fetchWolframData(query):
    '''
        This method constructs the Wolfram Alpha API URL, issues an HTTP request to get the webpage and gets Response
        object. From the Response object, it decodes and returns the JSON data.
    '''
    base_wolfram_url = 'http://api.wolframalpha.com/v2/query?'
    wolfram_api_key = 'VK9RKX-V2VJW282RE'

    build_wolfram_url = base_wolfram_url + 'appid=' + wolfram_api_key + '&input=' + query + '&output=json'

    return requests.get(build_wolfram_url).json()

def outputWolframData(data):
    '''
        This method pulls out all the necessary data from the previously obtained json data and returns a resulting string.
    '''
    for pod in data['queryresult']['pods']:
        if pod['title'] == 'Result' or pod['title'] == 'Solution':
            return pod['subpods'][0]['img']['alt']
        
if __name__ == '__main__':
    app.run()