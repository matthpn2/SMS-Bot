from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import wolframalpha_api, openweather_api, mapquest_api
import wikipedia

# Set up FLASK to connect this code to the local host, later to be connected to the Internet through NGROK
app = Flask(__name__)


@app.route('/', methods=['POST'])

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
        This method will simply look through the text message body and figure out the type of information desired. It will
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
            data = openweather_api.fetchWeatherData(message)
            answer = openweather_api.outputWeatherData(data)
        except:
            answer = "There was an Open Weather Map Error. Please try again."
    
    elif "wolfram" in message:
        # Remove the keyword "wolfram" from the message
        message = removeKeyWord(message, "wolfram")
        try:
            data = wolframalpha_api.fetchWolframData(message)
            answer = wolframalpha_api.outputWolframData(data)
        except:
            answer = "Request was NOT found using Wolfram Alpha. Please be more specific."

    elif "mapquest" in message:
        # Remove the keyword "mapquest" from the message
        message = removeKeyWord(message, "mapquest")
        try:
            data = mapquest_api.fetchMapData(message)
            answer = mapquest_api.outputMapData(data)
        except:
            answer = "There was a MapQuest Error. Please try again."
    
    else:
        # If the message contains NO keyword, display a help prompt to identify
        answer = ("\nPlease try again; no keywords were recognized. These are the commands you may use: " +
                  "\n\nWIKI [\"wikipedia request\"]" + "\nWEATHER [\"city name\"]" + 
                  "\nWOLFRAM [\"wolframalpha request\"]" + "\nMAPQUEST [\"locations separated by new line\"]\n")

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


if __name__ == '__main__':
    app.run()
