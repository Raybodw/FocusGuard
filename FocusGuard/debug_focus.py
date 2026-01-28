import cv2
import mediapipe as mp
import time
import vlc
import os
import sys
import traceback

print("=" * 60)
print("FOCUS GUARD - DEBUG VERSION")
print("=" * 60)

try:
    # =============== STEP 1: VIDEO ===============
    print("\n[1/4] Checking video...")
    folder = "media"
    video_file = None
    
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_file = os.path.join(folder, file)
                break
    
    if not video_file:
        print("❌ No video found in 'media' folder")
        print("   Please add a video file")
        sys.exit(1)
    
    print(f"✅ Video: {video_file}")
    
    # =============== STEP 2: CAMERA ===============
    print("[2/4] Opening camera...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("❌ CANNOT OPEN CAMERA!")
        print("   Solutions:")
        print("   1. Close Zoom, Skype, Discord")
        print("   2. Restart computer")
        print("   3. Check camera permissions")
        sys.exit(1)
    
    print("✅ Camera opened successfully")
    
    # =============== STEP 3: MEDIAPIPE ===============
    print("[3/4] Loading Mediapipe...")
    try:
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
        print("✅ Mediapipe loaded")
    except Exception as e:
        print(f"❌ Mediapipe failed: {e}")
        print("   Try: pip install mediapipe==0.10.8")
        sys.exit(1)
    
    # =============== STEP 4: VLC ===============
    print("[4/4] Checking VLC...")
    try:
        test_player = vlc.MediaPlayer(video_file)
        print("✅ VLC ready")
    except Exception as e:
        print(f"⚠️  VLC warning: {e}")
        print("   Make sure VLC Media Player is installed")
    
    # =============== ALL SYSTEMS GO ===============
    print("\n" + "=" * 60)
    print("✅ ALL SYSTEMS READY!")
    print("=" * 60)
    
    YOUR_PAGE_ID = "YOUR_PAGE_ID_HERE"
    SENSITIVITY = 0.42
    DELAY_TIME = 2.5
    
    print(f"\nPage ID: {YOUR_PAGE_ID}")
    print(f"Sensitivity: {SENSITIVITY}")
    print(f"Delay: {DELAY_TIME}s")
    
    input("\nPress ENTER to start monitoring...")
    
    # =============== MAIN LOOP ===============
    looking_start = None
    player = None
    
    print("\n🔥 MONITORING ACTIVE! Press ESC to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️  Frame read error")
            break
        
        frame = cv2.resize(frame, (640, 480))
        
        # Process
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        
        status = "Looking..."
        color = (0, 255, 0)
        
        if results.multi_face_landmarks:
            status = "Face detected ✓"
            
            for face_landmarks in results.multi_face_landmarks:
                iris_y = face_landmarks.landmark[468].y
                
                h, w, _ = frame.shape
                x = int(face_landmarks.landmark[468].x * w)
                y = int(iris_y * h)
                
                cv2.circle(frame, (x, y), 6, (0, 0, 255), -1)
                
                if iris_y > SENSITIVITY:
                    if looking_start is None:
                        looking_start = time.time()
                        print(f"⏱️  Looking down detected")
                    
                    elapsed = time.time() - looking_start
                    cv2.putText(frame, f"Timer: {elapsed:.1f}s", 
                              (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    
                    if elapsed > DELAY_TIME:
                        if player is None:
                            print(f"🎬 PLAYING VIDEO!")
                            player = vlc.MediaPlayer(video_file)
                            player.play()
                        
                        status = "VIDEO PLAYING!"
                        color = (0, 0, 255)
                else:
                    if looking_start is not None:
                        looking_start = None
                        print("✅ Looking up")
                    
                    if player:
                        player.stop()
                        player = None
        
        # Display
        cv2.putText(frame, status, (20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f"ID: {YOUR_PAGE_ID}", (20, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 255), 2)
        cv2.putText(frame, "ESC = Quit", (20, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Focus Guard - DEBUG', frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            print("\n👋 User pressed ESC")
            break
    
    print("\n🔄 Closing...")
    
except Exception as e:
    print(f"\n❌ CRITICAL ERROR!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    print("\nTraceback:")
    traceback.print_exc()

finally:
    print("\n🧹 Cleaning up...")
    try:
        cap.release()
    except:
        pass
    cv2.destroyAllWindows()
    print("✅ Cleanup done")
    print("=" * 60)