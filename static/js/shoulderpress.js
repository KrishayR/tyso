const video5 = document.getElementsByClassName('input_video5')[0];
const out5 = document.getElementsByClassName('output5')[0];
const controlsElement5 = document.getElementsByClassName('control5')[0];
const canvasCtx5 = out5.getContext('2d');

const parentElement = out5.parentElement;

// Create a new span element for the angle display
const angleDisplayLefth = document.createElement('span');
angleDisplayLefth.id = 'angle-display-left';
angleDisplayLefth.style.color = 'white';

// Create a new div element for the text display
const textDisplay = document.createElement('div');
textDisplay.id = 'text-display';
textDisplay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
textDisplay.style.color = '#fff';
textDisplay.style.padding = '50px';
textDisplay.style.position = 'absolute';
textDisplay.style.bottom = '0';
textDisplay.style.width = '95%';
textDisplay.style.display = 'flex';
textDisplay.style.justifyContent = 'space-around';
textDisplay.style.alignItems = 'center';

let up = false;
const workout = window.location.pathname; // get the current workout page
const workoutKey = `${workout}-count`; // create a unique key for the current workout
let counter = parseInt(localStorage.getItem(workoutKey)) || 0; // get the count from localStorage or set it to 0


// Create a new span element for the counter
const counterDisplay = document.createElement('span');
counterDisplay.id = 'counter-display';
counterDisplay.style.color = 'white';
counterDisplay.style.background = '-webkit-linear-gradient(left, #FA6045, #9F1D11)';
counterDisplay.style.webkitBackgroundClip = 'text';
counterDisplay.style.backgroundClip = 'text';
counterDisplay.style.webkitTextFillColor = 'transparent';
counterDisplay.style.fontSize = '3em';
counterDisplay.style.fontFamily = 'glacial';


// Create a new span element for the feedback
const feedbackDisplay = document.createElement('span');
feedbackDisplay.id = 'feedback-display';
feedbackDisplay.style.color = 'white';
feedbackDisplay.style.fontSize = '1.7em';
feedbackDisplay.style.fontFamily = 'glacial';


// Append the counter and feedback elements to the text display element

textDisplay.appendChild(counterDisplay);
textDisplay.appendChild(feedbackDisplay);

// Append the text display element to the parent element of the canvas
parentElement.appendChild(textDisplay);

// Create a new span element
const newHeader = document.createElement('span');
newHeader.classList.add('panel-heading');
newHeader.style.backgroundColor = '#ff4433';
newHeader.style.textAlign = 'center';
newHeader.style.position = 'absolute';
newHeader.innerText = 'Exercise: Shoulder Press';


const angleDisplayRighth = document.createElement('span');
angleDisplayRighth.id = 'angle-display-right';
angleDisplayRighth.style.color = 'white';

// Append the angle display element to the new header element
newHeader.appendChild(angleDisplayLefth);

newHeader.appendChild(angleDisplayRighth);



// Replace the existing panel-heading with the new header element
const oldHeader = document.querySelector('.panel-heading');
oldHeader.parentNode.replaceChild(newHeader, oldHeader);


const fpsControl = new FPS();

const spinner = document.querySelector('.loading');
spinner.ontransitionend = () => {
  spinner.style.display = 'none';
};

function zColor(data) {
  const z = clamp(data.from.z + 0.5, 0, 1);
  return `rgb(0, 0, 0)`;
}

function calculateAngles(a, b, c) {
    const angle = Math.abs(
      Math.atan2(c[1] - b[1], c[0] - b[0]) - Math.atan2(a[1] - b[1], a[0] - b[0])
    ) * (180.0 / Math.PI);
  
    return angle > 180.0 ? 360 - angle : angle;
  }

  function nextClear(){
    console.log("cleared")
    counter = 0;
    window.location.href = "/finish";
  
  }


function onResultsPose(results) {
 
  counterDisplay.textContent = `REPS: ${counter.toString()}`;
  localStorage.setItem(workoutKey, counter); // store the count in localStorage
  document.body.classList.add('loaded');
  fpsControl.tick();
  parentElement.insertBefore(newHeader, out5);

  canvasCtx5.save();
  canvasCtx5.clearRect(0, 0, out5.width, out5.height);
  canvasCtx5.drawImage(
      results.image, 0, 0, out5.width, out5.height);


  const right_shoulder = [results.poseLandmarks[11].x, results.poseLandmarks[11].y];
  const left_shoulder = [results.poseLandmarks[12].x, results.poseLandmarks[12].y];

  const right_elbow = [results.poseLandmarks[14].x, results.poseLandmarks[14].y];
  const right_wrist = [results.poseLandmarks[16].x, results.poseLandmarks[16].y];
//   const right_ankle = [results.poseLandmarks[27].x, results.poseLandmarks[27].y];
  let angle_right = calculateAngles(right_shoulder, right_elbow, right_wrist);

  // console.log(angle_right)
  // Display the angle of the right arm
  const angleDisplayRight = document.getElementById("angle-display-right");
  angleDisplayRight.textContent = `∠R: ${Math.round(angle_right)}`;

  const left_elbow = [results.poseLandmarks[13].x, results.poseLandmarks[13].y];
  const left_wrist = [results.poseLandmarks[15].x, results.poseLandmarks[15].y];
//   const left_ankle = [results.poseLandmarks[28].x, results.poseLandmarks[28].y];
  let angle_left = calculateAngles(left_shoulder, left_elbow, left_wrist);


  // Display the angle of the left arm
  const angleDisplayLeft = document.getElementById("angle-display-left");
  // Update the header with the left angle and exercise name
  angleDisplayLeft.textContent = `∠L: ${Math.round(angle_left)}`;
  drawConnectors(
    canvasCtx5, results.poseLandmarks, POSE_CONNECTIONS, {
      color: (data) => {
        const x0 = out5.width * data.from.x;
        const y0 = out5.height * data.from.y;
        const x1 = out5.width * data.to.x;
        const y1 = out5.height * data.to.y;

        const z0 = clamp(data.from.z + 0.5, 0, 1);
        const z1 = clamp(data.to.z + 0.5, 0, 1);

        const gradient = canvasCtx5.createLinearGradient(x0, y0, x1, y1);
        gradient.addColorStop(
            0, `rgb(54, 55, 56)`);
        gradient.addColorStop(
            1.0, `rgb(255, 68, 51)`);
        return gradient;
      }
    });
drawLandmarks(
    canvasCtx5,
    Object.values(POSE_LANDMARKS_LEFT)
        .map(index => results.poseLandmarks[index]),
    {color: zColor, fillColor: '#FF4455'});
drawLandmarks(
    canvasCtx5,
    Object.values(POSE_LANDMARKS_RIGHT)
        .map(index => results.poseLandmarks[index]),
    {color: zColor, fillColor: '#ff4455'});
drawLandmarks(
    canvasCtx5,
    Object.values(POSE_LANDMARKS_NEUTRAL)
        .map(index => results.poseLandmarks[index]),
    {color: zColor, fillColor: '#ff4455'});
canvasCtx5.restore();
// console.log(right_elbow[1], right_shoulder[1])
// Curling logic
if (!up && (right_elbow[1]*100 + 15 <= right_shoulder[1] * 100) && (left_elbow[1] * 100 + 15  <= left_shoulder[1] * 100)) {
    up = true;
    counter += 1;
    let text = "Perfect, now lower the weight to shoulder level, keeping elbows tucked.";
    feedbackDisplay.textContent = text;
} else if ((right_elbow[1] > right_shoulder[1]) && (left_elbow[1] > left_shoulder[1])){
    up = false;
    let text = "Lift the weight straight up above your head, and hold it there for a second.";
    feedbackDisplay.textContent = text;
} else if ((right_elbow[1] > right_shoulder[1]) && (left_elbow[1] > left_shoulder[1])){
    let text = "Perfect, now lower the weight to shoulder level, keeping elbows tucked.";
    feedbackDisplay.textContent = text;
}

    
}

// function onResultsPose(results) {
//     document.body.classList.add('loaded');
//     fpsControl.tick();
//     parentElement.insertBefore(newHeader, out5);
  
//     canvasCtx5.save();
//     canvasCtx5.clearRect(0, 0, out5.width, out5.height);
//     canvasCtx5.drawImage(
//         results.image, 0, 0, out5.width, out5.height);
    
//     // Get landmark coordinates
//     const landmarks = results.poseLandmarks;
//     const left_shoulder = [landmarks[11].x, landmarks[11].y];
//     const left_elbow = [landmarks[13].x, landmarks[13].y];
//     const left_wrist = [landmarks[15].x, landmarks[15].y];
//     const left_hip = [landmarks[23].x, landmarks[23].y];
    
//     drawConnectors(
//         canvasCtx5, landmarks, POSE_CONNECTIONS, {
//           color: (data) => {
//             const x0 = out5.width * data.from.x;
//             const y0 = out5.height * data.from.y;
//             const x1 = out5.width * data.to.x;
//             const y1 = out5.height * data.to.y;
  
//             const z0 = clamp(data.from.z + 0.5, 0, 1);
//             const z1 = clamp(data.to.z + 0.5, 0, 1);
  
//             const gradient = canvasCtx5.createLinearGradient(x0, y0, x1, y1);
//             gradient.addColorStop(
//                 0, `rgb(54, 55, 56)`);
//             gradient.addColorStop(
//                 1.0, `rgb(255, 68, 51)`);
//             return gradient;
//           }
//         });
//     drawLandmarks(
//         canvasCtx5, [left_shoulder, left_elbow, left_wrist, left_hip],
//         {color: zColor, fillColor: '#FF4455'});
//     canvasCtx5.restore();
//   }
  
const pose = new Pose({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.2/${file}`;
}});
pose.onResults(onResultsPose);

const camera = new Camera(video5, {
  onFrame: async () => {
    await pose.send({image: video5});
  },
  width: 1120,
  height: 630
});

camera.start();

new ControlPanel(controlsElement5, {
      selfieMode: true,
      upperBodyOnly: false,
      smoothLandmarks: true,
      minDetectionConfidence: 0.8,
      minTrackingConfidence: 0.6
    })
    .add([
      new StaticText({title: 'MediaPipe Pose'}),
      fpsControl,
      new Toggle({title: 'Selfie Mode', field: 'selfieMode'}),
      new Toggle({title: 'Upper-body Only', field: 'upperBodyOnly'}),
      new Toggle({title: 'Smooth Landmarks', field: 'smoothLandmarks'}),
      new Slider({
        title: 'Min Detection Confidence',
        field: 'minDetectionConfidence',
        range: [0, 1],
        step: 0.01
      }),
      new Slider({
        title: 'Min Tracking Confidence',
        field: 'minTrackingConfidence',
        range: [0, 1],
        step: 0.01
      }),
    ])
    .on(options => {
      video5.classList.toggle('selfie', options.selfieMode);
      pose.setOptions(options);
    });