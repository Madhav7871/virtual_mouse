🖐️ Virtual Mouse Controller using Hand Gesture Recognition:-

Control your computer mouse using hand gestures!
This project uses OpenCV, MediaPipe, and PyAutoGUI to convert hand movement into cursor movement, clicking, and dragging.

📌 Features
✔️ Hand Tracking
Detects 21 hand landmarks using MediaPipe
Tracks finger tips with high precision

✔️ Cursor Movement
Move the cursor using index finger
Smooth & stable cursor control with custom smoothing algorithm

✔️ Gestures Supported
Gesture	Action
Index finger up	Move cursor
Thumb + Index pinch	Left Click
Thumb + Index pinch + Middle finger up	Click-and-Drag
Release pinch	Stop click or drag

✔️ Stability Enhancements
Smooth cursor motion
Prevents accidental double-clicks using a click delay system
Works automatically on any screen resolution

🧰 Tech Stack
Python 3.x
OpenCV
MediaPipe
PyAutoGUI
NumPy


🚀 How It Works
🎯 1. Hand Detection
MediaPipe identifies hand landmarks in real-time.

🎯 2. Mapping
The finger positions inside a “control box” are mapped to screen coordinates.

🎯 3. Gesture Recognition
Detects finger states
Calculates distance between index & thumb
Uses gesture logic to trigger actions

🎯 4. Mouse Control
PyAutoGUI is used to:
Move cursor
Perform clicks
Perform drag operations

📸 Gestures
👉 Cursor Movement
Move only your index finger → mouse follows.

👉 Left Click
Pinch thumb + index fingers.

👉 Drag
Pinch + lift middle finger.

👉 Stop Drag / Reset
Release the pinch.

🔧 Installation
1. Clone the repository
git clone https://github.com/Madhav7871/virtual_mouse
cd virtual_mouse

2. Install required packages
pip install opencv-python mediapipe pyautogui numpy

3. Run the application
python virtual_mouse.py

📌 Future Enhancements
Right-click gesture
Scrolling gesture
Multi-hand support
On-screen UI

🙌 Author
Madhav Kalra
🔗 GitHub: https://github.com/Madhav7871/virtual_mouse

💬 Suggestions
If you have any suggestions, improvements, or ideas, feel free to open an issue or contribute!
Your feedback is always appreciated 😊
