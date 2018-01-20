"""
This is the template server side for ChatBot
"""
import json
from bottle import route, run, template, static_file, request
import requests
import boto_lists


def cat_joke():
    response = requests.get("http://catfact.ninja/fact")
    result = json.loads(response.content)
    return json.dumps(result["fact"])

    # url = 'https://catfact.ninja/fact' #different test for same API
    # response = urllib.urlopen(url)
    # datastore = json.loads(response.read())
    # random_joke = datastore["fact"]
    # print random_joke
    # return random_joke
    
    # response = requests.get("http://catfact.ninja/fact") #different test for same API
    # if (response.status_code == 200):
    #     result = json.loads(response.content)
    # return json.dumps(result["fact"])

    # response = requests.get("http://catfact.ninja/fact") #different test for same API
    # if (response.status_code == 200):
    #     result = json.loads(response.content)
    # return result["fact"]
    
@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')

    if ("love" in user_message):
        return json.dumps({"animation": "inlove", "msg": "I'm in love"})

    if ("joke" in user_message):
        user_response=cat_joke()
        return json.dumps({"animation": "inlove", "msg": user_response})

    for curse in boto_lists.curses:
        if curse in user_message:
            return json.dumps({
                "animation":
                "afraid",
                "msg":
                "Watch your mouth, buddy! We have a zero tolerance policy around this part of town."
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
