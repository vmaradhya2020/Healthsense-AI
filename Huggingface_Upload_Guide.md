---
title: HealthSense AI
emoji: 🏥
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 🏥 HealthSense AI - Multi-Agent Healthcare Platform

An intelligent healthcare platform powered by multiple AI agents to help users find hospitals, book doctor appointments, search lab tests, and get emergency services information.

## 🌟 Features

- **🏥 Hospital Comparison** - Search and compare hospitals by specialty, location, and ratings
- **👨‍⚕️ Doctor Booking** - Find doctors by specialty, view availability, and book appointments
- **🔬 Lab Tests** - Browse 4,800+ diagnostic tests and health screening packages
- **🚨 Emergency Services** - Locate nearest emergency facilities and ambulance services
- **💬 AI Chat Assistant** - Get intelligent health recommendations from multiple specialized AI agents

## 🤖 AI Agents

This platform uses **4 specialized AI agents** powered by LangChain and OpenAI:

1. **Emergency Services Agent** - Finds emergency facilities and ambulance services
2. **Hospital Comparison Agent** - Compares hospitals based on specialties and ratings
3. **Doctor Information Agent** - Manages doctor searches and appointment bookings
4. **Diagnostic Information Agent** - Provides lab test information and recommendations

## 🚀 How to Use

1. **Visit the Application** - The app will load automatically
2. **Navigate** - Use the top menu to access different features
3. **Search** - Use filters to find exactly what you need
4. **Book** - Schedule appointments or tests directly
5. **Ask AI** - Chat with the AI assistant for personalized recommendations

## 📊 Database Statistics

- **31** Emergency Facilities
- **28** Doctors with **3,024** Appointment Slots
- **4,818** Diagnostic Tests & Health Packages
- Comprehensive Hospital Database

## 🔧 Technology Stack

- **Backend:** FastAPI, Python 3.11
- **AI Framework:** LangChain, OpenAI GPT
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Database:** SQLite
- **Deployment:** Docker

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (HTML/CSS/JS)          │
│  6 Pages: Home, Emergency, Hospitals,   │
│  Doctors, Lab Tests, AI Chat            │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        FastAPI Backend API              │
│  20+ RESTful Endpoints                  │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌───────────────┐   ┌──────────────────┐
│  AI Agents    │   │    Databases     │
│  (LangChain)  │   │    (SQLite)      │
│               │   │                  │
│ • Emergency   │   │ • Emergency DB   │
│ • Hospital    │   │ • Appointments   │
│ • Doctor      │   │ • Hospital Data  │
│ • Diagnostic  │   │ • Lab Tests      │
└───────────────┘   └──────────────────┘
```

## 🔐 Environment Variables

This Space requires an OpenAI API key to function. The key should be set in the Space settings as a secret:

- `OPENAI_API_KEY` - Your OpenAI API key (required)

## 📝 API Documentation

Once the app is running, visit `/docs` for interactive API documentation powered by Swagger UI.

**Available Endpoints:**
- `GET /` - Home page
- `GET /health` - Health check
- `GET /api/emergency` - Emergency services search
- `GET /api/hospitals` - Hospital search and comparison
- `GET /api/doctors` - Doctor search
- `POST /api/appointments` - Book doctor appointment
- `GET /api/tests` - Lab tests search
- `POST /api/book-test` - Book lab test
- `POST /chat` - AI chat assistant

## 🎯 Use Cases

1. **Emergency Situations** - Quickly find nearest emergency rooms and ambulance services
2. **Specialist Search** - Find doctors by medical specialty and location
3. **Health Checkups** - Browse and book comprehensive health screening packages
4. **Hospital Comparison** - Compare hospitals for specific treatments or surgeries
5. **Health Questions** - Get AI-powered answers to health-related queries

## 🔒 Security & Privacy

- All data is processed securely
- No personal health information is stored permanently
- API keys are handled securely through environment variables
- Docker containerization for isolation

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Created with ❤️ for improved healthcare accessibility

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- AI powered by [OpenAI](https://openai.com/) and [LangChain](https://langchain.com/)
- Deployed on [Hugging Face Spaces](https://huggingface.co/spaces)

---

**Note:** This is a demonstration platform. Always consult with healthcare professionals for medical advice.
