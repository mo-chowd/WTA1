# 🚀 Space Bot API Investigation Sheet

**Total Marks: 40**  
**TASK 1: Collect Required API Documentation**

This investigation sheet helps you gather key technical information from the three APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current Location API**, **Weather API** and a **Geocoding API** , plus the Python time module. Also furhter investigate the application of Web Architecture and MVC design pattern in development of the Bot

---

##  Webex Messaging API (4 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `https://webexapis.com/v1` |
| Authentication Method | `bearer token` |
| Endpoint to list rooms | `/rooms` |
| Endpoint to get messages | `/messages` |
| Endpoint to send message | `/messages` |
| Required headers | `bearer <token>` |
| Sample full GET or POST request | `GET https://webexapis.com/v1/messages?roomId=<room id>&max=1` |


##  ISS Current Location API (2 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org/iss-now.json` |
| Endpoint for current ISS location | `/iss-now.json` |
| Sample response format (example JSON) |  
```
{
  "message": "success",
  "timestamp": 1792277645,
  "iss_position": {
    "latitude": "-45.8103",
    "longitude": "-51.5680"
  }
}
```

##  Geocoding API (4 marks)

| Criteria | Details |
|---------|---------|
| Provider used | `OpenWeatherMap Geocoding API: Uses same key as OpenWeather key` |
| API Base URL | `https://api.openweathermap.org/geo/1.0` |
| Endpoint for geocoding | `GET /direct` |
| Endpoint for reverse geocoding | `GET /reverse` |
| Authentication method | `API key in 'appid' query parameter` |
| Required query parameters | `Geocoding: q, appid. Reverse: lat, lon, appid` |
| Sample request with latitude/longitude | `https://api.openweathermap.org/geo/1.0/reverse?lat=51.27&lon=-0.88&limit=1&appid=<API_KEY>` |
| Sample JSON response (formatted example) |  
```
[
    {
        "name": "Hart",
        "lat": 51.2761671,
        "lon": -0.8927989805623809,
        "country": "GB",
        "state": "England"
    }
]
```

##  Weather API (3 marks)

| Criteria | Details |
|---------|---------|
| API Provider | `OpenWeather` |
| API Base URL | `https://api.openweathermap.org/data/2.5/weather` |
| Endpoint for current weather | `GET /weather` |
| Authentication method | `parameter "appid"` |
| Required query parameters | `	lat, lon, appid (optional: units=metric, lang)` |
| Sample JSON response (formatted example) |  
```
{
  "name": "Paris",
  "weather": [{ "description": "clear sky" }],
  "main": { "temp": 9.59, "humidity": 82 },
  "wind": { "speed": 4.12 },
  "clouds": { "all": 1 },
  "sys": { "country": "FR", "sunrise": 1792304098, "sunset": 1792342575 }
}
```

##  Epoch to Human Time Conversion (Python time module) (2 marks)

| Criteria | Details |
|---------|---------|
| Library used | `datetime` |
| Function used to convert epoch | `datetime.fromtimestamp() and .strftime()` |
| Sample code to convert timestamp |  
```
from datetime import datetime, timezone
timestamp = 1760710000
readable = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%d %b %Y %H:%M:%S")
print(readable)
```
Output (human-readable time) `17 Oct 2025 14:06:40`

##  Extended Feature API ( 3 marks)

| Criteria | Details |
|---------|---------|
| API Provider | `Nasa Astronomy Picture of The Day (APOD)` |
| API Base URL | `https://api.nasa.gov` |
| Endpoint | `GET /planetary/apod` |
| Authentication method | `API key in "api_key" query parameter` |
| Required query parameters | `api_key` |
| Sample JSON response (formatted example) |  
```

```
|

--- 

##  Evaluation – Web Architecture, MVC Design & Security 

In this section, evaluate how web technologies, architecture, and design patterns have been applied in your **AstroBot**. Your responses must relate directly to your implementation and include reflection on your design decisions.

---

###  Web Architecture – Client–Server Model (3 marks)

Explain how the client–server model applies to your AstroBot:

- Identify the **client** 
- Identify the **server(s)** 
- Describe how data flows between:
  - User, AstroBot and APIs

Include a **simple block diagram** to illustrate this interaction.

####  Security Considerations: (3 marks )
- Consider but not limiting to secure handling of API keys and tokens, API rate limiting, and Input validation (e.g., handling user commands safely), include examples from code where necessary to illustrate.

---

###  RESTful API Usage in Your Application (3 marks )

Explain how REST APIs are used in your AstroBot: 

- Describe how HTTP methods (GET, POST) are used  
- Explain how your bot interacts with APIs (Webex, Weather, ISS, Geocoding)  
- Describe how JSON responses are received and processed  

Note: Relate your explanation directly to your code for higher grade. 

#### Security Considerations: (2 marks)
- Check response status codes, Handling invalid or unexpected API responses, Avoiding excessive API calls

---

###  MVC Design Pattern in AstroBot (3 Marks)

Explain how the **Model–View–Controller (MVC)** pattern applies to your solution:
Provide a short example based on your implementation

| Component   | Description and Example (Relate to your Bot) |
|------------|----------------------------------|
| **Model**  |  |
| **View**   |  |
| **Controller** |  |

---

### 📝 Reflection and Evaluation ( 8 marks )

Reflect on your AstroBot (400 words):

- How effective is your bot in meeting the Astronomy Club’s needs?  
- What design decisions worked well?  
- What challenges did you face when integrating APIs?  
- What security risks did you identify and how were they handled?  
- How could your solution be improved in the future?  

---

 **Tip:** Link your answers directly to your code and examples for higher marks.
### Notes

- Use official documentation for accuracy (e.g. developer.webex.com, locationiq.com or Mapbox, open-notify.org or other ISS API).
- Be prepared to explain your findings to your instructor or demo how you retrieved them using tools like Postman, Curl, or Python scripts.

---

###  Total: /40
