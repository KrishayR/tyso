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
prev_left_shoulder = None
prev_right_shoulder = None
shoulder_moving = False

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

            # Shoulder Movement
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            if prev_left_shoulder is not None and prev_right_shoulder is not None:
                left_dx = left_shoulder[0] - prev_left_shoulder[0]
                left_dy = left_shoulder[1] - prev_left_shoulder[1]
                right_dx = right_shoulder[0] - prev_right_shoulder[0]
                right_dy = right_shoulder[1] - prev_right_shoulder[1]
                if abs(left_dx) > 0.05 or abs(left_dy) > 0.05 or abs(right_dx) > 0.05 or abs(right_dy) > 0.05:
                    shoulder_moving = True
                    
            prev_left_shoulder = left_shoulder
            prev_right_shoulder = right_shoulder

            # Bicep Curl
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_distance = np.sqrt((left_elbow[0] - left_hip[0])**2 + (left_elbow[1] - left_hip[1])**2)
            angle_left = calculate_angles(left_shoulder, left_elbow, left_wrist)
            cv2.putText(image, str(round(angle_left)), tuple(np.multiply(left_elbow, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_distance = np.sqrt((right_elbow[0] - right_hip[0])**2 + (right_elbow[1] - right_hip[1])**2)
            angle_right = calculate_angles(right_shoulder, right_elbow, right_wrist)
            cv2.putText(image, str(round(angle_right)), tuple(np.multiply(right_elbow, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            # cv2.putText(image, str(right_distance), tuple(np.multiply(right_elbow, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Curling logic
            if not shoulder_moving:
                if left_distance < 0.3 and right_distance < 0.3:
                    if angle_left > 165 and angle_right > 165:
                        stage = "extended"
                    elif angle_left < 165 and angle_right < 165 and stage == "compressed":
                        cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                        text = "Extend your arms fully, making sure your elbows are almost straight."
                        cv2.putText(image, text, (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 2, cv2.LINE_AA)

                    if (angle_left < 25 and stage == "extended") and (angle_right < 25 and stage == "extended"):
                        stage = "compressed"
                        counter += 1
                    elif angle_left > 25 and angle_right > 25 and stage == "extended":
                        cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                        text = "Contract your arms fully, so that the dumbell almost touches your shoulder."
                        cv2.putText(image, text, (40, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 2, cv2.LINE_AA)
                else:
                    cv2.rectangle(image, (0, 650), (1280, 720), (51, 68, 255), -1)
                    text = "Form Tip: Your elbows should be tucked in when performing the bicep curl."
                    cv2.putText(image, text, (40, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            else:
                shoulder_moving = False

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