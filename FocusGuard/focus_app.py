import cv2
import mediapipe as mp
import time
import vlc
import os
import sys

print("=" * 60)
print("       FOCUS GUARD - IMPROVED DISTANCE DETECTION")
print("=" * 60)

# =============== YOUR PAGE ID ===============
YOUR_PAGE_ID = "YOUR_PAGE_ID_HERE"
print(f"📱 Page ID: {YOUR_PAGE_ID}")
print("-" * 60)

# =============== VIDEO DETECTION ===============
def find_video_in_folder(folder="media"):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
        return None
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    
    video_files = []
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_files.append(file)
    
    if not video_files:
        return None
    
    video_files.sort()
    return os.path.join(folder, video_files[0])

print("\n🔍 Looking for video files...")
VIDEO_FILE = find_video_in_folder("media")

if VIDEO_FILE is None:
    print("❌ No video found. Please add a video to 'media' folder")
    sys.exit(1)

print(f"✅ Video: {os.path.basename(VIDEO_FILE)}")

# =============== CAMERA SETUP ===============
print("\n📷 Starting camera...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Camera error")
    sys.exit(1)

print("✅ Camera ready")

# =============== IMPROVED FACE DETECTION ===============
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.3,  # Reduced for distance
    min_tracking_confidence=0.3    # Reduced for distance
)

print("✅ Face detection ready (optimized for distance)")

# =============== IMPROVED SETTINGS ===============
SENSITIVITY = 0.38      # Higher = less sensitive (better for distance)
DELAY_TIME = 3.0        # Longer delay to avoid false positives
FACE_CONFIDENCE_THRESHOLD = 0.3  # Minimum face detection confidence

print(f"\n⚙️  Optimized Settings (for sitting farther):")
print(f"   • Sensitivity: {SENSITIVITY} (adjusted for distance)")
print(f"   • Delay: {DELAY_TIME}s (longer to prevent false alarms)")
print(f"   • Face confidence: {FACE_CONFIDENCE_THRESHOLD}")

# =============== INSTRUCTIONS ===============
print("\n" + "=" * 60)
print("🎮 Tips for better detection:")
print("   1. Sit 50-80cm from camera")
print("   2. Ensure good frontal lighting")
print("   3. Camera at eye level or slightly higher")
print("   4. Remove glasses if possible")
print("=" * 60)

input("\nPress ENTER to start...")

# =============== VARIABLES ===============
look_start_time = None
is_video_playing = False
vlc_player = None
face_detected = False
last_face_time = time.time()

print(f"\n🚀 Monitoring started")
print("   Looking for your face...\n")

# =============== MAIN LOOP WITH IMPROVEMENTS ===============
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (640, 480))
        
        # =============== IMPROVED FACE PROCESSING ===============
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        status_msg = "Status: Looking at screen"
        status_color = (0, 255, 0)  # Green
        eye_position = "center"
        face_detected_now = False
        
        if results.multi_face_landmarks:
            face_detected_now = True
            last_face_time = time.time()
            
            for face_landmarks in results.multi_face_landmarks:
                # Get multiple points for better accuracy
                iris_y = face_landmarks.landmark[468].y  # Right eye iris
                forehead_y = face_landmarks.landmark[10].y  # Forehead
                chin_y = face_landmarks.landmark[152].y  # Chin
                
                # Calculate face size for distance estimation
                face_height = chin_y - forehead_y
                
                height, width, _ = frame.shape
                x_pixel = int(face_landmarks.landmark[468].x * width)
                y_pixel = int(iris_y * height)
                
                # Draw face bounding box for visual feedback
                if face_height > 0.1:  # If face is reasonably close
                    cv2.circle(frame, (x_pixel, y_pixel), 6, (0, 0, 255), -1)
                    
                    # Detect "looking down" with distance consideration
                    if iris_y > SENSITIVITY and face_height > 0.15:  # Must be close enough
                        eye_position = "down"
                        
                        if look_start_time is None:
                            look_start_time = time.time()
                            print(f"⏱️  Looking down detected")
                        
                        elapsed = time.time() - look_start_time
                        
                        cv2.putText(frame, f"Countdown: {elapsed:.1f}s", 
                                  (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                        
                        if elapsed > DELAY_TIME:
                            if not is_video_playing:
                                print(f"🎬 Playing video (after {elapsed:.1f}s)")
                                vlc_player = vlc.MediaPlayer(VIDEO_FILE)
                                vlc_player.play()
                                is_video_playing = True
                            
                            status_msg = "Status: VIDEO PLAYING!"
                            status_color = (0, 0, 255)
                            
                            cv2.putText(frame, "FOCUS ALERT!", 
                                      (120, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                    else:
                        eye_position = "up"
                        
                        if look_start_time is not None:
                            print("✅ Looking at screen")
                            look_start_time = None
                        
                        if is_video_playing:
                            if vlc_player:
                                vlc_player.stop()
                            is_video_playing = False
                            print("⏹️  Video stopped")
                else:
                    # Face is too far
                    cv2.putText(frame, "Move closer to camera", 
                              (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # If no face detected for a while
        if not face_detected_now:
            no_face_time = time.time() - last_face_time
            if no_face_time > 2.0:
                status_msg = "Status: Face not detected"
                status_color = (255, 165, 0)  # Orange
        
        # =============== DISPLAY INFO ===============
        cv2.putText(frame, status_msg, (20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(frame, f"Eye: {eye_position}", (20, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"ID: {YOUR_PAGE_ID}", (20, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 255), 2)
        cv2.putText(frame, "ESC = Quit | F = Increase sensitivity", (20, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Real-time sensitivity adjustment hint
        cv2.putText(frame, f"Sensitivity: {SENSITIVITY}", (500, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        cv2.imshow(f'Focus Guard - {YOUR_PAGE_ID}', frame)
        
        # Key controls for live adjustment
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            print(f"\n👋 Exiting...")
            break
        elif key == ord('f'):  # Increase sensitivity (lower number)
            SENSITIVITY = max(0.2, SENSITIVITY - 0.02)
            print(f"🔧 Sensitivity increased to: {SENSITIVITY:.2f}")
        elif key == ord('d'):  # Decrease sensitivity (higher number)
            SENSITIVITY = min(0.5, SENSITIVITY + 0.02)
            print(f"🔧 Sensitivity decreased to: {SENSITIVITY:.2f}")

except KeyboardInterrupt:
    print(f"\n⏹️  Stopped")

finally:
    cap.release()
    cv2.destroyAllWindows()
    if vlc_player:
        vlc_player.stop()
    
    print(f"\n✅ Session complete")
    print("=" * 60)