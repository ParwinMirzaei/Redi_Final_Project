import requests

api_key = 'ec0fdd298254fb963e76fbbb35bc51a4'

while True:
    location = input("Location: ")

    result = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}')
    if result.json()['cod'] == '404':
        print("Invalid location!")
        continue
    break

data = result.json()
description = data['weather'][0]['description']
temperature = round(data['main']['temp'])
feels_like = round(data['main']['feels_like'])
high = round(data['main']['temp_max'])
low = round(data['main']['temp_min'])

print(f"The weather in {location[0].upper()}{location[1:]} is {temperature}° C with {description}.")
print(f"It feels like {feels_like}° C.")
print(f"Today's high is {high}° C and today's low is {low}° C.")

# Additional advice based on weather conditions
advice_given = False

if 'rain' in description:
    print("Take an umbrella with you.")
    advice_given = True
if temperature < 5:
    print("Put on warm clothes.")
    advice_given = True
if 20 <= temperature <= 25:
    print("The weather is perfect for hiking.")
    advice_given = True
if 30 <= temperature <= 40:
    print("Put on sunglasses.")
    advice_given = True

if not advice_given:
    print("Check the weather carefully.")