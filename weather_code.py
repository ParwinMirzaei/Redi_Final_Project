import sys
import random
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.api_key = 'ec0fdd298254fb963e76fbbb35bc51a4'
        
        # List of weather fun facts
        self.facts = [
            "Weather Is Unpredictable, Always",
            "Climate Is What You Expect, Weather Is What You Get",
            "Wind Blows From Areas Of High To Low Pressure",
            "Commonwealth Bay, Antarctica, Is The Windiest Place In The world",
            "Lightning Can Strike Twice",
            "The Entire Length Of The Mississippi River Froze Over In 1899",
            "Hurricanes And Typhoons Are The Same Types Of Storm",
            "Mawsynram, India, has the highest rainfall on the planet.",
            "The Average Speed Of A Raindrop Is 9 Meters (29.6 feet) Per Second",
            "One Billion Tons of Rain Falls On The Planet Every Minute",
            "Lightning Strikes The Earth's Surface 100 Times Per Second",
            "Snowflakes Can Take Up To An Hour To Reach The Earth",
            "Ozone Is Hazardous For Your Health",
            "Tornadoes And Waterspouts Are The Same Weather Phenomena",
            "Antarctica Is Completely Covered By A Glacier",
            "Why Hurricanes Have Female Names",
            "The Air Is 78 Percent Nitrogen",
            "Antarctica Is The Largest Desert In The World",
            "A Raindrop Is Not Tear-Shaped",
            "The highest temperature ever recorded was in Death Valley, USA",
            "A Warm Front Can Cause Rain",
            "Never Drive Through Flood Water"
        ]
        
        # Set up the GUI
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Weather App')
        self.setGeometry(300, 250, 700, 600)
        self.setStyleSheet("background-color: #809ea1;")  # Sky blue background

        # Layout
        self.layout = QVBoxLayout()

        # Location input
        self.location_label = QLabel('Enter Location:')
        self.location_label.setStyleSheet("font-family: 'Times New Roman'; font-size: 30px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.location_label)

        self.location_input = QLineEdit(self)
        self.location_input.setStyleSheet("font-family: 'Times New Roman';font-size: 26px; padding: 18px; background-color: #F0FFF0;")  # Light green background
        self.layout.addWidget(self.location_input)
        self.location_input.returnPressed.connect(self.fetch_weather)  # Connect Enter key to fetch_weather

        # Fetch weather button
        self.fetch_button = QPushButton('Get Weather', self)
        self.fetch_button.setStyleSheet("font-family: 'Times New Roman'; background-color: #2b8b7f; color: white; font-size: 22px; font-weight: bold; padding: 10px;")  # Cerulean button
        self.fetch_button.clicked.connect(self.fetch_weather)
        self.layout.addWidget(self.fetch_button)

        # Weather icon display
        self.icon_label = QLabel(self)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.icon_label)

        # Weather result display
        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("font-family: 'Times New Roman';font-size: 24px; padding: 16px; background-color: #F0FFF0;")  # Light green background
        self.layout.addWidget(self.result_display)

        # Fun fact display
        self.fun_fact_label = QLabel(self)
        self.fun_fact_label.setAlignment(Qt.AlignCenter)
        self.fun_fact_label.setWordWrap(True)
        self.fun_fact_label.setStyleSheet("font-family: 'Times New Roman';font-size: 20px; padding: 16px; background-color: #F0FFF0; color: #333;")  # Light green background
        self.layout.addWidget(self.fun_fact_label)
        
        # Set layout
        self.setLayout(self.layout)

    def fetch_weather(self):
        location = self.location_input.text()
        result = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={self.api_key}')
        
        if result.status_code != 200 or result.json().get('cod') == '404':
            self.result_display.setText("Invalid location. Please check the location spelling!")
            self.icon_label.clear()
            self.fun_fact_label.clear()
            return
        
        data = result.json()
        description = data['weather'][0]['description']
        temperature = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        high = round(data['main']['temp_max'])
        low = round(data['main']['temp_min'])

        weather_info = (
            f"The weather in {location.title()} now is <b><span style='color:red;'>{temperature}° C</span></b> with {description}.<br><br>"
            f"It feels like {feels_like}° C.<br><br>"
            f"Today's high is {high}° C and today's low is {low}° C.<br><br>"
        )

        advice = ""
        
        icon_directory = "C:/Users/nkogh/ReDI_Project/Redi_Final_Project/"
        if 'rain' in description:
            advice += "Take an umbrella with you.<br><br>"
            icon_path = icon_directory + 'rain.png'
        elif 'clear' in description:
            advice += "Put on sunglasses.<br><br>"
            icon_path = icon_directory + 'sun.png'
        elif 'cloud' in description:
            advice += "It might be a bit gloomy.<br><br>"
            icon_path = icon_directory + 'cloud.png'
        elif 'snow' in description:
            advice += "Wear warm clothes.<br><br>"
            icon_path = icon_directory + 'snow.png'
        elif 'thunderstorm' in description:
            advice += "Stay indoors if possible.<br><br>"
            icon_path = icon_directory + 'thunderstorm.png'
        else:
            advice = "Check the weather carefully."
            icon_path = ""

        if icon_path:
            pixmap = QPixmap(icon_path).scaled(50, 50, Qt.KeepAspectRatio)
            self.icon_label.setPixmap(pixmap)
        else:
            self.icon_label.clear()

        self.result_display.setHtml(weather_info + advice)
        self.display_random_fact()

    def display_random_fact(self):
        random_fact = random.choice(self.facts)
        self.fun_fact_label.setText(f"<h3 style='font-size: 24px; color: #2b8b7f;'>Fun Fact:</h3> <p style='font-size: 20px;'>{random_fact}</p>")

# Main function to run the app
def main():
    app = QApplication(sys.argv)
    ex = WeatherApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
