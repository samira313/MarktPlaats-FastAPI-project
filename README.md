# MarktPlaats – FastAPI Backend Project

This is a *group project* developed during a training program.  
The goal of the project was to design and implement a backend API for a simple marketplace application using modern Python backend technologies.

---

## 📌 Project Description

*MarktPlaats* is a RESTful API built with *FastAPI* that allows users to:
- Register and authenticate
- Post and manage advertisements
- Exchange messages
- Access protected resources using JWT authentication

The project focuses on:
- Clean API design
- Separation of concerns (routers, services, schemas)
- Authorization and access control
- Automated testing

---

## 🚀 Main Features

### 🔐 Authentication
- User registration
- User login (OAuth2 password flow)
- JWT access tokens
- Token-based authorization for protected endpoints

### 💬 Messages
- Send and retrieve messages between users
- Protected endpoints (requires authentication)
- Conversation logic between sender and receiver
- WebSocket support for real-time messaging
- 
### 📢 Advertisements (Ads)
- Create, read, update and delete ads
- Public listing of ads
- Fetch ads by ID
- Only the owner of an ad can update or delete it
- Proper error handling (401, 403, 404)
- Comment system for advertisements
- Rating system for users and ads
- Search and filtering for ads
---

## 🧱 Technology Stack
- *Python*
- *FastAPI*
- *SQLAlchemy*
- *SQLite*
- *Pydantic*
- *pytest*

---

## 🧪 Testing

The project contains automated tests for:
- Authentication flow (register, login, token handling)
- Messages endpoints (authorized and unauthorized access)
- Advertisement endpoints (CRUD and access rules)
- Shared test helpers for reusable logic

Run tests with:
```bash
pytest -vv
