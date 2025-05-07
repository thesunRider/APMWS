from ollama import chat
from ollama import ChatResponse
import time,random
import datetime
from flask import Flask, request, jsonify
from flask import render_template
import json

def current_milli_time():
  return round(time.time() * 1000)

start_index = 0
start_time = current_milli_time()
message_history = []
random.seed(10)

plant_growth_rate = 1e-4 #cm/ms
plant_start_height = 10 #cm

plant_height = 10 #cm
moisture_data = 20 #%
sunlight_data = 0  #1 shinig, 0 no sunlight
temperature_data = 15 #temp in C

motor_stat = 0
notfications_list = [{}]

thinking_prompt = prompt = """
You are an automatic plant monitoring and watering system. Your task is to analyze incoming sensor data and respond with appropriate actions.

Sensor Input Format (example):
{
  'time': 2025-05-07 19:37:07.82964,
  'sunlight': 0,
  'moisture_level': 47,
  'plant_height': 10.0,
  'temperature': 35
}

Expected Output Format (example):
{
  "motor_status": 1,
  "notifications": [
    {
      "notification_title": "Sunlight Warning",
      "notification_msg": "Not enough sunlight"
    },
    {
      "notification_title": "Temperature Warning",
      "notification_msg": "Temperature too high"
    }
  ]
}

Decision Rules:
- Temperature:
  - If below 10 or above 30 then send a temperature warning.
- Sunlight:
  - Keep a daily total of sunlight (sum of non-zero sunlight readings).
  - At the end of the day:
    - If total sunlight duration < 30 minutes then send "Not enough sunlight" warning.
    - If total sunlight duration > 5 hours then send "Too much sunlight" warning.
- Moisture Level:
  - If below 30 then set motor_status as 1 until it reaches 50%, then motor_status as 0.

Instructions:
- Do not write any code.
- If moisture is below 30 then motor_status is 1
- If moisture is above 50 then motor_status is 0
- Only return the output JSON based on the logic above.
- I will provide sensor input, and you will process it and return only the output.
"""


def prompt_chaining(prompt): 
  global motor_stat
  message_history.append({"role":"user", "content":prompt})
  response: ChatResponse = chat(model='llama3.2', messages=message_history)

  print("Response: ",response.message.content)
  message_history.append({"role":"assistant", "content":response.message.content})
  try:
    data_json = json.loads(response.message.content)
    motor_stat = data_json["motor_status"]
    notfications_list = data_json["notifications"]
  except json.JSONDecodeError as e:
    notfications_list = [{}]
    motor_stat = 0
    print(f"Failed to decode JSON: {e}")

  return response.message.content


#set output data
def set_motor(motor_status = 0):
  global motor_stat
  motor_stat = motor_status
  print(set_motor)

def send_notification(title,msg):
  print(title,msg)

#random sensor data
def get_plant_height():
  return plant_height #plant_start_height + ((current_milli_time() - start_time) * plant_growth_rate) 

def get_moisture_data(): 
  return moisture_data #random.randint(20, 70) 

def get_sunlight_data():
  return sunlight_data #random.randint(0, 1) 

def get_temperature_data():
  return temperature_data #random.randint(5, 40) 

def get_sensor_inputs():
  now = datetime.datetime.now()
  sensor_val = {"time":str(now),"sunlight": get_sunlight_data(),"moisture_level":get_moisture_data(),"plant_height":get_plant_height(),"temperature":get_temperature_data()}
  print(sensor_val)
  return str(sensor_val)

#print(get_sensor_inputs())

prompt_chaining(thinking_prompt)


app = Flask(__name__)

@app.route('/setvar', methods=['GET'])
def setvar():
    global plant_height,moisture_data,sunlight_data,temperature_data
    global motor_stat,notfications_list


    plant_height = int(request.args.get('plant_height', '10'))  
    moisture_data = int(request.args.get('moisture_data', '10'))  
    sunlight_data = 0 if request.args.get('sunlight_data', '0')=="false" else 1 
    temperature_data = int(request.args.get('temperature_data', '10')) 
    print("plant_height:",plant_height,"  moisture_data:",moisture_data, "  sunlight_data:",sunlight_data,"  temperature_data:",temperature_data)
    prompt_chaining(get_sensor_inputs())
    out = {'mot': motor_stat,"notify":notfications_list}
    print(out)
    return jsonify(out)


@app.route('/', methods=['GET'])
def indexhtml():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()