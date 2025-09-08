# Binary Calculator with Unreliable Socket Transmission

## 📖 Project Overview
Python application simulating a binary calculator using unreliable socket transmission.  
The goal was to simulate a **server and client** communicating via sockets:  
- The **client** inputs an operation  
- The **server** processes it and returns the result  
- The transmission simulates **random errors**, making communication unreliable  

The application has three major components:
1. **Connection Handling** – Establishing the connection between server and client using the `socket` Python package  
2. **Binary Conversion** – Converting decimal operations into binary using the `hashlib` Python package  
3. **Error Simulation** – Introducing random errors into the answer communication  

All of it is displayed in a simple yet effective **graphical interface** using the `customtkinter` and `tkinter` Python packages.

---

## ⚙️ Requirements
Make sure you have the following installed:
- Python 3.9+  
- `customtkinter`  
- `tkinter` (comes pre-installed with Python)  
- `hashlib` (standard library)  

Install dependencies (if needed):
```bash
pip install customtkinter
