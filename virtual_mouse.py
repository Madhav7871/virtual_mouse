import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# --- Configuration ---
wCam, hCam = 640, 480         # Camera resolution
# DECREASING frameR makes the pink box BIGGER and movement LESS sensitive
frameR = 50                   
smoothening = 9               # Smoothing factor for cursor movement
wScr, hScr = pyautogui.size() # Get screen resolution

# --- Click System Parameters ---
CLICK_DELAY = 0.3             # Time (in seconds) to prevent immediate re-clicks
last_click_time = 0 
is_pinching = False           # Flag to track if the pinch gesture is currently held

# Variables for smoothing and state
plocX, plocY = 0, 0
clocX, clocY = 0, 0
is_dragging = False
tipIds = [4, 8, 12, 16, 20]   # Tip landmarks: Thumb, Index, Middle, Ring, Pinky

# --- Initialization ---
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7) 
mpDraw = mp.solutions.drawing_utils


# --- Helper Function: Check Which Fingers Are Up ---
def fingers_up(lmList):
    """Determines which fingers are open/up based on their tip position relative to the joint below."""
    fingers = []

    # Thumb check (specific to horizontal movement)
    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingers.append(1) # Up
    else:
        fingers.append(0) # Down

    # 4 Fingers (Index to Pinky): check if tip y-coordinate is above the joint's y-coordinate
    for id in range(1, 5):
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1) # Up
        else:
            fingers.append(0) # Down
    
    return fingers

# --- Main Loop ---
while True:
    success, img = cap.read()
    if not success:
        continue
        
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    current_time = time.time()

    lmList = []
    
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[0]
        mpDraw.draw_landmarks(img, myHand, mpHands.HAND_CONNECTIONS)

        h, w, c = img.shape
        for id, lm in enumerate(myHand.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    
    if len(lmList) != 0:
        # Get pixel coordinates for Index Tip (8) and Thumb Tip (4)
        x1, y1 = lmList[8][1], lmList[8][2] # Index Tip (8)
        x0, y0 = lmList[4][1], lmList[4][2] # Thumb Tip (4)

        my_fingers = fingers_up(lmList)

        # Draw the control zone rectangle
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        
        
        # 1. MOVEMENT MODE (Index Finger ONLY is Up - The primary control mode)
        if my_fingers[1] == 1 and my_fingers[2] == 0:
            
            # 1.1. Map Coordinates: Scales the hand position in the pink box to the screen size
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            
            # 1.2. Apply Smoothing: Gradually moves the cursor to the target position
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 1.3. Move Mouse Cursor
            try:
                pyautogui.moveTo(int(clocX), int(clocY), _pause=False)
            except Exception:
                pass

            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        
        # 2. CLICK/DRAG MODE (Index and Thumb involved)
        
        # Calculate distance between Index (8) and Thumb (4) tips
        length = np.sqrt((x1 - x0)**2 + (y1 - y0)**2) 
        mid_x, mid_y = int((x0 + x1) / 2), int((y0 + y1) / 2)
        cv2.line(img, (x0, y0), (x1, y1), (255, 0, 255), 3)

        # 2.1. PINCH DETECTED (Click or Drag Action)
        if length < 40: 
            cv2.circle(img, (mid_x, mid_y), 15, (0, 255, 0), cv2.FILLED)
            
            # --- DRAG Check (Index and Middle finger up while pinching) ---
            if my_fingers[1] == 1 and my_fingers[2] == 1:
                if not is_dragging:
                    pyautogui.mouseDown(button='left')
                    is_dragging = True
            
            # --- SINGLE CLICK Check (Only Index finger up while pinching) ---
            elif my_fingers[1] == 1 and my_fingers[2] == 0:
                
                # If we are currently dragging, release the drag and perform a normal click action
                if is_dragging:
                    pyautogui.mouseUp(button='left')
                    is_dragging = False

                # Only allow a click if the pinch is new and outside the delay period
                if not is_pinching and (current_time - last_click_time) > CLICK_DELAY:
                    pyautogui.click()
                    last_click_time = current_time
                
                # Set pinch state to true to block immediate re-clicks
                is_pinching = True 

        # 2.2. PINCH RELEASED (Movement or Drag Release)
        else: 
            # If the pinch was just released, reset the pinch state
            if is_pinching:
                is_pinching = False
            
            # If dragging was active, release the mouse button
            if is_dragging:
                pyautogui.mouseUp(button='left')
                is_dragging = False

    # 3. Display Frame
    cv2.imshow("Virtual Mouse Controller", img)
    
    # Break loop on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()