# Many Bugs, add in next version#

import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Video feed
cap = cv2.VideoCapture(0)

# Counter 
counter_left = 0
counter_right = 0

repetition_counted_left = False
repetition_counted_right = False

stage_left = None
stage_right = None

hysteresis = 5

lunge_counted = False

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

            # Lunge
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            angle_left = calculate_angles(left_hip, left_knee, left_ankle)


            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            angle_right = calculate_angles(right_hip, right_knee, right_ankle)

            cv2.putText(image, str(round(angle_left)), tuple(np.multiply(left_hip, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(round(angle_right)), tuple(np.multiply(right_hip, [1280, 720]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            if angle_left > (160 + hysteresis):
                stage_left = "extended"
                cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                text = "Lunge forward until your right thigh is parallel to the ground."
                cv2.putText(image, text, (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 1, cv2.LINE_AA)

            if (angle_left < (145 - hysteresis) and stage_left == "extended" and not repetition_counted_left):
                stage_left = "compressed"
                counter_left += 1
                text = "Slowly get back up, squeezing your quad muscles."
                cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                cv2.putText(image, text, (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 1, cv2.LINE_AA)
                repetition_counted_left = True
            elif angle_left >= 145-hysteresis:
                repetition_counted_left = False

            if angle_right > (160 + hysteresis):
                stage_right = "extended"
                cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                text = "Lunge forward until your right thigh is parallel to the ground."
                cv2.putText(image, text, (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 1, cv2.LINE_AA)

            if (angle_right < (145 - hysteresis) and stage_right == "extended" and not repetition_counted_right):
                stage_right = "compressed"
                counter_right += 1
                cv2.rectangle(image, (0, 650), (1280, 720), (255, 255, 255), -1)
                text = "Slowly get back up, squeezing your quad muscles."
                cv2.putText(image, text, (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (51, 68, 255), 1, cv2.LINE_AA)
                repetition_counted_right = True
            elif angle_right >= 145-hysteresis:
                repetition_counted_right = False




        except Exception as err:
            print(err)


        # Counter text
        cv2.rectangle(image, (0, 0), (200, 73), (51, 68, 255), -1)
        cv2.rectangle(image, (1280-200, 0), (1280, 73), (51, 68, 255), -1)
        # cv2.putText(image, "REPS: ", (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, "L: " + str(counter_left), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, "R: " + str(counter_right), ((1280-200)+10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

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