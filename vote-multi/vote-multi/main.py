from flask import Flask, request, render_template
import os
import random
import redis
import socket
import sys

app = Flask(__name__)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

if ("VOTE1VALUE" in os.environ and os.environ['VOTE1VALUE']):
    button1 = os.environ['VOTE1VALUE']
else:
    button1 = app.config['VOTE1VALUE']

if ("VOTE2VALUE" in os.environ and os.environ['VOTE2VALUE']):
    button2 = os.environ['VOTE2VALUE']
else:
    button2 = app.config['VOTE2VALUE']

if ("VOTE3VALUE" in os.environ and os.environ['VOTE3VALUE']):
    button3 = os.environ['VOTE3VALUE']
else:
    button3 = app.config['VOTE3VALUE']

if ("VOTE4VALUE" in os.environ and os.environ['VOTE4VALUE']):
    button4 = os.environ['VOTE4VALUE']
else:
    button4 = app.config['VOTE4VALUE']

if ("VOTE5VALUE" in os.environ and os.environ['VOTE5VALUE']):
    button5 = os.environ['VOTE5VALUE']
else:
    button5 = app.config['VOTE5VALUE']

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

if ("RESET" in os.environ and os.environ['RESET']):
    reset = os.environ['RESET']
else:
    reset = app.config['RESET']

# Redis configurations
redis_server = os.environ['REDIS']

# Redis Connection
try:
    if "REDIS_PWD" in os.environ:
        r = redis.StrictRedis(host=redis_server,
                        port=6379, 
                        password=os.environ['REDIS_PWD'])
    else:
        r = redis.Redis(redis_server)
    r.ping()
except redis.ConnectionError:
    exit('Failed to connect to Redis, terminating.')

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    subtitle = "(pod:" + socket.gethostname() + ")" 

# Init Redis
if not r.get(button1): r.set(button1,0)
if not r.get(button2): r.set(button2,0)
if not r.get(button3): r.set(button3,0)
if not r.get(button4): r.set(button4,0)
if not r.get(button5): r.set(button5,0)

def render(vote1,vote2,vote3,vote4,vote5):
    value1=int(vote1)
    value2=int(vote2)
    value3=int(vote3)
    value4=int(vote4)
    value5=int(vote5)
    total=0 + int(vote1) + int(vote2) + int(vote3) + int(vote4) + int(vote5)

    if (total > 0):
        value6=float(int(1000*int(vote1)/(total)+0.5)/10)
        value7=float(int(1000*int(vote2)/(total)+0.5)/10)
        value8=float(int(1000*int(vote3)/(total)+0.5)/10)
        value9=float(int(1000*int(vote4)/(total)+0.5)/10)
        value10=float(int(1000*int(vote5)/(total)+0.5)/10)
    else:
        value6=0
        value7=0
        value8=0
        value9=0
        value10=0

    if (button1 == ""):
        b1="none"
    else:
        b1="initial"

    if (button2 == ""):
        b2="none"
    else:
        b2="initial"

    if (button3 == ""):
        b3="none"
    else:
        b3="initial"

    if (button4 == ""):
        b4="none"
    else:
        b4="initial"

    if (button5 == ""):
        b5="none"
    else:
        b5="initial"

    if (reset == ""):
        b6="none"
    else:
        b6="initial"

    return render_template("index.html", value1=value1, value2=value2, value3=value3, value4=value4, value5=value5, value6=value6, value7=value7, value8=value8, value9=value9, value10=value10, button1=button1, button2=button2, button3=button3, button4=button4, button5=button5, b1=b1, b2=b2, b3=b3, b4=b4, b5=b5, b6=b6, total=total, title=title, subtitle=subtitle)

@app.route('/multi', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        # Get current values
        vote1 = r.get(button1).decode('utf-8')
        vote2 = r.get(button2).decode('utf-8')
        vote3 = r.get(button3).decode('utf-8')
        vote4 = r.get(button4).decode('utf-8')
        vote5 = r.get(button5).decode('utf-8')
        if (int(vote1 + vote2 + vote3 + vote4 + vote5) == 0):
        
            # Return index with values
            return render(0,0,0,0,0)

        else:
            # Return index with values
            return render(vote1,vote2,vote3,vote4,vote5)


    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            
            # Empty table and return results
            r.set(button1,0)
            r.set(button2,0)
            r.set(button3,0)
            r.set(button4,0)
            r.set(button5,0)
            vote1 = r.get(button1).decode('utf-8')
            vote2 = r.get(button2).decode('utf-8')
            vote3 = r.get(button3).decode('utf-8')
            vote4 = r.get(button4).decode('utf-8')
            vote5 = r.get(button5).decode('utf-8')
            return render(vote1,vote2,vote3,vote4,vote5)
        
        else:

            # Insert vote result into DB
            vote = request.form['vote']
            r.incr(vote,1)

            # Get current values
            vote1 = r.get(button1).decode('utf-8')
            vote2 = r.get(button2).decode('utf-8')  
            vote3 = r.get(button3).decode('utf-8')  
            vote4 = r.get(button4).decode('utf-8')  
            vote5 = r.get(button5).decode('utf-8')  
                
            # Return results
            return render(vote1,vote2,vote3,vote4,vote5)

if __name__ == "__main__":
    app.run()
