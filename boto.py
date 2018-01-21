"""
This is the template server side for ChatBot
"""

import json
import urllib
from datetime import datetime, timedelta

import requests
from bottle import request, response, route, run, static_file, template

import boto_lists

disable_previous_visitor = False


def joke():
    url = "http://api.yomomma.info/"
    r = urllib.urlopen(url)
    data = json.loads(r.read())
    joke = data["joke"]
    return joke


def previous_visit_status():
    print disable_previous_visitor
    if request.get_cookie("user_name"):
        return True
    else:
        return False


def get_weather():
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?id=293396&appid=5ef9a65dfb88532f640e535ad54ce699'
    )
    json_object = json.loads(r.text)
    temp_kelvin = float(json_object['main']['temp'])
    temp_celsius = temp_kelvin - 273.15
    return {
        "animation": "dancing",
        "msg": "The temperature is {} degrees Celsius".format(
            str(temp_celsius))
    }


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg').lower()
    name = user_message.capitalize()
    previous_visitor = previous_visit_status()
    global disable_previous_visitor

    if previous_visitor and not disable_previous_visitor:
        disable_previous_visitor = True
        print "entered if previous statement"
        return json.dumps({
            "animation": "excited",
            "msg": "Nice seeing you again, {}!".format(name)
        })
    elif not previous_visitor and not disable_previous_visitor:
        disable_previous_visitor = True
        response.set_cookie(
            name="user_name",
            value=name,
            expires=datetime.now() + timedelta(days=30))
        return json.dumps({
            "animation": "excited",
            "msg": "Nice meeting you, {}!".format(name)
        })

    if ("commands" in user_message):
        return json.dumps({
            "animation":
            "takeoff",
            "msg":
            "Write 'joke' for something to make you laugh or 'get weather' to find out the weather in your location!"
        })

    if ("get weather" in user_message):
        temp = get_weather()
        return json.dumps(temp)

    if ("love" in user_message):
        return json.dumps({
            "animation":
            "inlove",
            "msg":
            "Do ya love me? Are you playing your love games with me?... I'm old gregg!!"
        })

    if ("?" in user_message):
        return json.dumps({
            "animation":
            "no",
            "msg":
            "I think you are smart enough to figure that out on your own."
        })

    if ("joke" in user_message):
        joke_response = joke()
        return json.dumps({"animation": "laughing", "msg": joke_response})

    for curse in boto_lists.curses:
        if curse in user_message:
            return json.dumps({
                "animation":
                "afraid",
                "msg":
                "Watch your mouth, buddy! We have a zero tolerance policy around this part of town."
            })

    return json.dumps({
        "animation":
        "confused",
        "msg":
        "I didn't quite get that. For a list of options, please enter 'commands'."
    })


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
