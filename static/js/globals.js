// // varants for accessing the webcam and canvas
// var video5 = document.getElementsByClassName('input_video5')[0];
// var out5 = document.getElementsByClassName('output5')[0];
// var controlsElement5 = document.getElementsByClassName('control5')[0];
// var canvasCtx5 = out5.getContext('2d');

// // Parent element for the canvas
// var parentElement = out5.parentElement;

// // Create a new span element for the angle display
// var angleDisplayLefth = document.createElement('span');
// angleDisplayLefth.id = 'angle-display-left';
// angleDisplayLefth.style.color = 'white';

// // Create a new div element for the text display
// var textDisplay = document.createElement('div');
// textDisplay.id = 'text-display';
// textDisplay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
// textDisplay.style.color = '#fff';
// textDisplay.style.padding = '50px';
// textDisplay.style.position = 'absolute';
// textDisplay.style.bottom = '0';
// textDisplay.style.width = '95%';
// textDisplay.style.display = 'flex';
// textDisplay.style.justifyContent = 'space-around';
// textDisplay.style.alignItems = 'center';

// // Create a new span element for the counter
// var counterDisplay = document.createElement('span');
// counterDisplay.id = 'counter-display';
// counterDisplay.style.color = 'white';
// counterDisplay.style.background = '-webkit-linear-gradient(left, #FA6045, #9F1D11)';
// counterDisplay.style.webkitBackgroundClip = 'text';
// counterDisplay.style.backgroundClip = 'text';
// counterDisplay.style.webkitTextFillColor = 'transparent';
// counterDisplay.style.fontSize = '3em';
// counterDisplay.style.fontFamily = 'glacial';

// // Create a new span element for the feedback
// var feedbackDisplay = document.createElement('span');
// feedbackDisplay.id = 'feedback-display';
// feedbackDisplay.style.color = 'white';
// feedbackDisplay.style.fontSize = '1.7em';
// feedbackDisplay.style.fontFamily = 'glacial';

// // Create a new span element for the angle display on the right
// var angleDisplayRighth = document.createElement('span');
// angleDisplayRighth.id = 'angle-display-right';
// angleDisplayRighth.style.color = 'white';

// // Create a new span element for the exercise header
// var newHeader = document.createElement('span');
// newHeader.classList.add('panel-heading');
// newHeader.style.backgroundColor = '#ff4433';
// newHeader.style.textAlign = 'center';
// newHeader.style.position = 'absolute';

// // varants for counting reps
// var up = false;
// var counter = 0;

// // Create a new FPS object for tracking frames per second
// var fpsControl = new FPS();

// // Hide the spinner when the loading transition is finished
// var spinner = document.querySelector('.loading');
// spinner.ontransitionend = () => {
//   spinner.style.display = 'none';
// };


// var pose = new Pose({locateFile: (file) => {
//     return `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.2/${file}`;
//   }});
//   pose.onResults(onResultsPose);
  
//    var camera = new Camera(video5, {
//     onFrame: async () => {
//       await pose.send({image: video5});
//     },
//     width: 1120,
//     height: 630
//   });
  
//   camera.start();

//   new ControlPanel(controlsElement5, {
//     selfieMode: true,
//     upperBodyOnly: false,
//     smoothLandmarks: true,
//     minDetectionConfidence: 0.8,
//     minTrackingConfidence: 0.6
//   })
//   .add([
//     new StaticText({title: 'MediaPipe Pose'}),
//     fpsControl,
//     new Toggle({title: 'Selfie Mode', field: 'selfieMode'}),
//     new Toggle({title: 'Upper-body Only', field: 'upperBodyOnly'}),
//     new Toggle({title: 'Smooth Landmarks', field: 'smoothLandmarks'}),
//     new Slider({
//       title: 'Min Detection Confidence',
//       field: 'minDetectionConfidence',
//       range: [0, 1],
//       step: 0.01
//     }),
//     new Slider({
//       title: 'Min Tracking Confidence',
//       field: 'minTrackingConfidence',
//       range: [0, 1],
//       step: 0.01
//     }),
//   ])
//   .on(options => {
//     video5.classList.toggle('selfie', options.selfieMode);
//     pose.setOptions(options);
//   });
