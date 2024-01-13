import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Video feed
cap = cv2.VideoCapture(0)

# Counter 
counter = 0
stage = None
prev_hip = None
hip_moving = False

def calculate_angles(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
    
    return angle

# Change confidence to be tighter on user's form
with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.6) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False # Improves Performance

        # Detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # Improves Performance

        # Extract Landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Hip Movement
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            if prev_hip is not None:
                dx = hip[0] - prev_hip[0]
                dy = hip[1] - prev_hip[1]
                if dy > 0.07:
                    hip_moving = True
                if dy < -0.2 and hip_moving:
                    counter += 1
                    hip_moving = False

            prev_hip = hip

            # Deadlift
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            left_angle = calculate_angles(left_shoulder, left_hip, left_knee)
            cv2.putText(image, str(round(left_angle)), tuple(np.multiply(left_knee, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            right_angle = calculate_angles(right_shoulder, right_hip, right_knee)
            cv2.putText(image, str(round(right_angle)), tuple(np.multiply(right_knee, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)


            left_knee_check = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
            right_knee_check = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
            # print("left_knee: " + str(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]))
            # Check if user is standing straight
            if left_knee_check.visibility > 0.5 or right_knee_check.visibility > 0.5:
                if left_angle > 165 and right_angle > 165:
                    stage = "extended"

                elif left_angle < 165 and right_angle < 165 and stage == "compressed":
                        cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                        text = "Fully extend your legs and hips, with a straight back throughout."
                        cv2.putText(image, text, (55, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 2, cv2.LINE_AA)

                if (right_angle < 120 and stage == "extended") and (right_angle < 120 and stage == "extended"):
                    stage = "compressed"
                    counter += 1
                elif left_angle > 120 and right_angle > 120 and stage == "extended":
                        cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                        text = "Bend your knees and lower the weight towards your feet."
                        cv2.putText(image, text, (40, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 2, cv2.LINE_AA)
            
            else:
                cv2.rectangle(image, (0, 650), (1280, 720), (51, 68, 255), -1)
                text = "Please step back and show your full body for accurate movement tracking"
                cv2.putText(image, text, (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                # y0, dy = 700, 50
                # for i, line in enumerate(text.split('\n')):
                #     y = y0 + i*dy
                #     cv2.putText(image, line, (100, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    


        except Exception as err:
            pass


        # Counter text
        cv2.rectangle(image, (0, 0), (225, 73), (51, 68, 255), -1)
        cv2.putText(image, "REPS: ", (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

        # Rendering connections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(56, 55, 54), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(51, 68, 255), thickness=2, circle_radius=2)
        )

        cv2.imshow('Cam', image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()