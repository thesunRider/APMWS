## Assignment 3
Automatic Plant management Prototype
This is a Automatic Plant monitoring and watering system project as part of coursework in Uni sigen (LLM driven Plant Bot)

Thinking Prompt:
for every 15 minutes,Check time,check moisture level ,sunlight and temperature.
	1. if temperature below 10 C or above 30 C sent warning
	2. Sum over the sunlight data for the day, if it falls below 5% at the end of the day send too less sunlight warning, if it falls above 20% sent over sunlight warning
	3. if moisture level is below 30% start delivering water until moisture level is 50%

Sensor Inputs
- Time (RTC clock)
- Sunlight (LDR)
- Moisture level (resistance sensor)
- Plant Height
- Temperature sensor

Outputs
- Amount of water poured in
- Sunlight Deficiency Warning
- Temperature warning

![image](https://github.com/user-attachments/assets/91118576-964c-4f7b-b3ef-345aa56e6836)
