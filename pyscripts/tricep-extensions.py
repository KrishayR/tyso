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

            # Tricep Extension
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            angle_left = calculate_angles(left_shoulder, left_elbow, left_wrist)
            cv2.putText(image, str(round(angle_left)), tuple(np.multiply(left_elbow, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            angle_right = calculate_angles(right_shoulder, right_elbow, right_wrist)
            cv2.putText(image, str(round(angle_right)), tuple(np.multiply(right_elbow, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            # cv2.putText(image, str(right_distance), tuple(np.multiply(right_elbow, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
            text = "To start, lift the dumbell straight overhead, with your arms parallel."
            cv2.putText(image, text, (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 1, cv2.LINE_AA)
            # Making sure the elbows are above the shoulders
            if left_elbow[1] < left_shoulder[1] and right_elbow[1] < right_shoulder[1]:
                # Tricep Extension logic

                if angle_left > 150 and angle_right > 150:
                    stage = "extended"
                    cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                    text = "Now lower it slowly behind your head until your hands touch your back."
                    cv2.putText(image, text, (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 1, cv2.LINE_AA)
                else:
                    cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                    text = "Extend your arms up so they are parallel straight over your head"
                    cv2.putText(image, text, (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 1, cv2.LINE_AA)



                if (angle_left < 80 and stage == "extended") and (angle_right < 80 and stage == "extended"):
                    stage = "compressed"
                    counter += 1

                if right_elbow[1]*10 + 0.75 < left_elbow[1]*10:
                    # Right ELBOW is lower than left ELBOW, do something
                    cv2.rectangle(image, (0, 650), (1280, 720), (51, 68, 255), -1)
                    text = "Form Check: Your right arm is higher than your left."
                    cv2.putText(image, text, (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                elif left_elbow[1]*10 + 0.75 < right_elbow[1]*10:
                    cv2.rectangle(image, (0, 650), (1280, 720), (51, 68, 255), -1)
                    text = "Form Check: Your left arm is higher than your right."
                    cv2.putText(image, text, (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

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