# QR-Based Event Check-In System 🎟️

A backend system built with **FastAPI** that allows students to register for college events and receive unique QR codes for entry. Admins can scan these codes on event day to verify attendance and mark check-ins.

This is a fork/clone maintained under [`charveemasand108/OR-GDG`](https://github.com/charveemasand108/OR-GDG).

---

## 📦 Features

- 🔐 JWT-based User Authentication (Admin/User roles)
- 🗓️ Event Creation by Admins
- ✅ QR Code Generation on Registration
- 📲 Admin Check-In using QR scan
- 📊 Attendance View for Admins
- 🧾 Swagger API Docs (`/docs`)

---

## ⚙️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB (via `pymongo`)
- **Auth**: JWT (using `python-jose`, `passlib`)
- **QR Code**: `qrcode` Python lib
- **Environment Config**: `python-dotenv`

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/charveemasand108/OR-GDG.git
cd OR-GDG
