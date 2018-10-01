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

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

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

def render(vote1,vote2):
    value1=int(vote1)
    value2=int(vote2)
    value3=int(vote1) + int(vote2)
    if (int(vote1 + vote2) > 0):
        value4=float(int(1000*int(vote1)/(int(vote1)+int(vote2))+0.5)/10)
        value5=float(int(1000*int(vote2)/(int(vote1)+int(vote2))+0.5)/10)
    else:
        value4=0
        value5=0
    return render_template("index.html", value1=value1, value2=value2, value3=value3, value4=value4, value5=value5, button1=button1, button2=button2, title=title, subtitle=subtitle)

@app.route('/vote', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        # Get current values
        vote1 = r.get(button1).decode('utf-8')
        vote2 = r.get(button2).decode('utf-8')
        if (int(vote1 + vote2) == 0):
        
            # Return index with values
            return render(0,0)

        else:
            # Return index with values
            return render(vote1,vote2)


    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            
            # Empty table and return results
            r.set(button1,0)
            r.set(button2,0)
            vote1 = r.get(button1).decode('utf-8')
            vote2 = r.get(button2).decode('utf-8')
            return render(vote1,vote2)
        
        else:

            # Insert vote result into DB
            vote = request.form['vote']
            r.incr(vote,1)

            # Get current values
            vote1 = r.get(button1).decode('utf-8')
            vote2 = r.get(button2).decode('utf-8')  
                
            # Return results
            return render(vote1,vote2)

if __name__ == "__main__":
    app.run()
