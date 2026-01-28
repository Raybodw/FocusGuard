#🛡️ Focus Guard - Fight distractions while studying!

<div align="center">

![Focus Guard Demo](https://img.shields.io/badge/DEMO-LIVE-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-orange?style=for-the-badge&logo=opencv)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Study Smart, Focus Smart!**

[✨ Features](#-features) • [🚀 Installation](#-installation) • [🎮 How to Use](#-How to Use) • [📸 Demo](#-Demo) • [🤝 Contribution](#-Contribution)

</div>

---

## 🌟 **The Story Behind Focus Guard**

Are you constantly reaching for your phone while studying? 📱
**Focus Guard** is a smart assistant that uses AI to track your eye movements. If it detects that you're looking down (at your phone), it will immediately play a video to bring you back to studying!

---

## ✨ **Features**

| Feature | Description | 🎯 |
|---------|-----------|-----|
| **Real-time eye tracking** | Uses Google MediaPipe | 👁️ |
| **Adjustable sensitivity** | Adjustable for different distances | ⚙️ |
| **Play video** | Autoplay video when distracted | 🎬 |
| **Live controls** | Adjust settings while running | 🎮 |
| **Full debugging** | Detailed Error Report | 🐛 |

---

## 📊 **How ​​to work**

```Mermaid
LR Chart
A[Camera on] --> B{Face detected?}
B -->|Yes| C[Eye coordinate analysis]
B -->|No| D[Show 'Face not found']
C --> E{Eyes looking down?}
E -->|Yes| F[Start countdown]
E -->|No| G[Continue reading ✅]
F --> H{More than 3 seconds?}
H -->|Yes| I[Play motivational video 🎬]
H -->|No| G
I --> J[Back to Reading]
```

---

## 🚀 **Quick Installation**

### **Prerequisites:**
- Python 3.8 or higher
- Camera (laptop or webcam)
- Windows 10/11 (also works on Linux and Mac)

### **Installation Steps:**
```bash
# 1. Copy the repository
git clone https://github.com/yourusername/FocusGuard.git
cd FocusGuard
# 2. Install the libraries
pip install -r requirements.txt
# 3. Install VLC (for video playback)
# Download from https://www.videolan.org/vlc/
# 4. Add Video
# Place a video file in the 'media' folder
# 5. Run!
python focus_app.py
```

---

## 🎮 **How ​​to use**

### **Setup Steps:**
1. Run the program
2. Sit facing the camera (distance 50-80 cm)
3. The camera should be at eye level or slightly higher
4. Start reading!

### **Live controls:**
| Key | Action |
|-----|--------|
| **ESC** | Exit the program |
| **F** | Increase sensitivity (for further distance) |
| **D** | Decrease sensitivity (for closer distance) |

---

## 📸 **Visual Demo**

### **Normal Mode (Reading):**
```
📊 [Mode: Looking at Screen]
👁️ [Eyes: Up]
✅ Active Focus
```

### **Distraction Alert:**
```
⚠️ [Mode: Looking Down]
⏱️ [Countdown: 2.3 seconds]
🎬 [Video Coming Soon...]
```

### **Playing Video:**
```
🚨 [Mode: Playing Video!]
🎬 [Playing Video...]
📱 "Put Your Phone Down!" ```

---

## 🛠️ **Project Files**

```
FocusGuard/
├── 📁 media/ # Video folder
│ └── motivational.mp4 # Video
├── 📄 focus_app.py # Main app
├── 📄 debug_focus.py # Debug version
├── 📄 requirements.txt # Required libraries
├── 📄 README.md # This file
└── 📄 .gitignore # Ignored files
```

---

## 🔧 **Troubleshooting**

| Problem | Solution |
|--------|-----|
| **Camera not working** | Close other apps (Zoom, Skype) |
| **Face not detected** | Improve lighting |
| **Video not playing** | Install VLC Player |
| **Mistake detection** | Adjust sensitivity with F/D keys |

---

## 🤝 **Contribution**

We welcome your contributions! 🙌

### **Ways to contribute:**
1. **Report bugs** 🐛
2. **Suggest new features** 💡
3. **Improve documentation** 📖
4. **Translate to other languages** 🌍

### **Steps to contribute:**
```bash
# 1. Fork the project
# 2. Create a new branch
git checkout -b feature/amazing-feature
# 3. Commit changes
git commit -m 'Add amazing feature ✨'
# 4. Push
git push origin feature/amazing-feature
# 5. Create a pull request
```

---

## 📱 **Contact us**

| Platform | Link | Description |
|----|------------|---------|
| **GitHub** | [github.com/raybodo yourusername](https://github.com/raybodw) | Source Code |
| **Instagram** | [instagram.com/yourpage](https://instagram.com/amirrezailaghi) | Video Tutorials |


---

## 📊 **Project Statistics**

![Stars](https://img.shields.io/github/stars/raybodw/FocusGuard?style=social)
![Forks](https://img.shields.io/github/forks/raybodw/FocusGuard?style=social)
![Contributors](https://img.shields.io/github/contributors/raybodw/FocusGuard?color=blue)

---

## 🎯 **Creative Uses**

1. **Exam Preparation** 📚
2. **Remote Work** 🏠
3. **Practice meditation and concentration** 🧘
4. **Control phone use** ⏰
5. **Teach children to concentrate** 👶

---

## 📜 **License**

This project is released under the **MIT Lice** license.
