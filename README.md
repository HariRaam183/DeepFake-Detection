# Deepfake Detection System

A full-stack deepfake detection application using deep learning and React.

## Project Structure

```
deepfake_project/
│
├── dataset/
│   ├── train/
│   │   ├── real/
│   │   └── fake/
│   └── test/
│       ├── real/
│       └── fake/
├── model/
│   └── deepfake_model.h5 (generated after training)
├── train_model.py
├── predict.py
├── backend/
│   └── app.py
└── frontend/
    ├── package.json
    ├── public/
    └── src/
        ├── App.js
        └── index.js
```

## Setup Instructions

### 1. Prepare Dataset

- Place real images in `dataset/train/real/` and `dataset/test/real/`
- Place fake images in `dataset/train/fake/` and `dataset/test/fake/`

### 2. Install Python Dependencies

```bash
pip install tensorflow opencv-python numpy flask flask-cors
```

### 3. Train the Model

```bash
python train_model.py
```

### 4. Run Backend Server

```bash
cd backend
python app.py
```

### 5. Run Frontend

```bash
cd frontend
npm install
npm start
```

## Features

- 🧠 MobileNetV2-based deep learning model
- 🔮 Binary classification (Real vs Fake)
- 🌐 Flask REST API backend
- ⚛️ React frontend with file upload
- 📊 Real-time prediction results

## Usage

1. Open the frontend (usually http://localhost:3000)
2. Select an image file
3. Click "Check" button
4. View the result (REAL or FAKE)

## Technologies Used

- **Backend**: Python, TensorFlow, Flask, OpenCV
- **Frontend**: React, Axios
- **Model**: MobileNetV2 (Transfer Learning)
