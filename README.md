https://youtu.be/QYMXNqOteqs

Inspiration
The inspiration behind Tyso comes from a personal issue I encountered while starting on my fitness journey at home a few months ago. In a journey for self-improvement, I began working out alone taking guidance from self-improvement creators. However, the challenges I faced during my home workouts became apparent. Training until failure and getting sidetracked with music or losing count during reps made me want to find a solution. Working out solo at home also showed the absence of a personal trainer for form correction, which risked possible injuries and non-optimal training. Thus, Tyso was born, which uses AI technology to count reps, assess form, and offer real-time guidance—a comprehensive solution to the hurdles faced during solo home workouts. Tyso aims to help individuals in achieving their fitness goals and enhancing overall health through personalized guidance and progress tracking, especially to those with fewer resources and help.

What it does
Tyso is an AI-powered all-in-one personal fitness training platform that uses advanced facial recognition and computer vision technology, and a trained machine-learning model to accurately count reps of an exercise and provide real-time form guidance to ensure a user is doing an exercise with optimal form. The platform also tracks progress over time with comments and pictures and the progress is displayed on a calendar. First, a user securely signs up on our website, with an authentication system that utilizes 2FA. After logging in, the user can start a workout. The user first selects the exercises they plan to do during the workout, in order, and asks for the weight of any dumbbells or barbells being used in the session (this will be tracked for progress in the calendar). The platform then prompts the user to open the devices camera which will be needed to count the reps and check form of an exercise. The data from the camera is then processed and passed into a haarcascade facial recognition model to detect the face of the user working out. Once the face is detected, landmarks through out the body will appear. The advanced computer vision model detects where all the joints and muscles are located on the body, and places landmarks on them for the user to see. Let's say the users first exercise is the classic bicep curl. After the face is recognized and the landmarks appear, the computer vision model predicts an angle between the elbow, shoulder, and wrist. It will use this to count the reps. When the arm is in the extended state, the angle between the joints will be 180 degrees, while when the arm is contracted, the angle between the joints is less than 60 degrees. If the CV model detects both the extended and contracted states of the arm and logs it in a variable. As for the form correction, a mediapipe pose model that I have trained with thousands of bicep curl videos (Datasets were found on kaggle, called InfiniteRep) is put on the video-streaming data. The model predicts how accurate the form is. If the form is accurate enough, it will count the rep, if not, it will offer advice on how to fix the form for the next rep. This process is continued for each rep and each exercise (there are 5 exercises I have trained so far). Finally, once the user finishes the workout, a workout summary screen displays which shows how many reps of each exercise they completed and the time it took. It then stores it into a database. After this, the user can go to the calendar and they should see their workout data for that day.

The meditation game is called rocket. In this game, a rocket ascends as you engage in meditation, and the longer you meditate, the higher the rocket goes. By incentivizing the meditation process, Tyso Rocket aims to enhance your mindfulness practice and provide a fun and interactive way to track your progress. It uses a computer vision model to detect movement in your body and predicts if you are really meditating.

How we built it
I built it using many technologies and languages. For the front-end, I used HTML, SCSS/CSS, JS, and Jquery. I used Descope for the authentication system, which is a workflow that helps add authentication, authorization, and identity management to a web app. For the back-end, I went with the Python's flask web framework. Alongside this framework, I had to use Tensorflow, Keras, NumPy, OpenCV.js, and MediaPipe.js for the computer vision models. Other libraries I used were PathLib, Google_Auth, Flask_Login, Flask_Bcrypt, Flask_Session, and WTforms, all for the authentication system. For the database that stores workout information, I used Flask SQLAlchemy and Elasticsearch to retrieve the data. To stream the data from python on the front-end, I used AJAX. The datasets I used to train the form-correction model were InfiniteRep and LUXAI. For the facial recognition as the workout was happening, I used a facial recognition haarcascade.

Challenges we ran into
I ran into many challenges building Tyso. Integrating computer vision into the frontend using JavaScript was a big challenge, as Python, my initial choice, was too slow for real-time processing. The adoption of Descope for the first time for authentication also was a steep learning curve. Training machine learning models for form correction and rep counting was something new to me so I had to do extensive research and experimentation to overcome the intricacies of the training process. The communication between Python and JavaScript, which was important for the data streaming and real-time responsiveness, was challenging because it was often too slow and choppy.

Accomplishments that we're proud of
I am proud of entering into the realm of machine learning for the first time. It was a challenging but rewarding experience, especially in training the model for precise form-correction during workouts. I am proud of in overcoming the initial hurdles and achieving success in implementing this complex feature. Ultimately, I am proud of Tyso's potential impact on the health and well-being of users, and how it can guide them towards a positive path by providing accessible, responsive, and personalized fitness support.

What we learned
I learned many new technologies. This experience provided insights into the world of computer vision, and I expanded my understanding of how advanced technologies can be uses for fitness solutions. Working with Descope for authentication was also a learning experience to a new workflow, presenting a learning opportunity in implementing authentication features. Overcoming challenges in AI rep counting and model training reinforced the importance of perseverance and in-depth research in addressing technical obstacles. Overall, I learned how to adapt and be flexible.

What's next for Tyso
My immediate focus is rigorous bug fixing and system polishing to ensure a seamless user experience. The calendar feature, integral for tracking workout progress, is nearing completion, awaiting its final touches. I plan on refining the code to enhance overall efficiency and maintainability. As Tyso evolves, our commitment extends to continuous development, with an eye on deployment.
