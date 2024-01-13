window.onload = function () {
  // Get the URL parameters
  var url = document.location.href;
  var params = url.split('?')[1];
  if (!params) {
    return;
  }
  params = params.split('&');
  var data = {};
  for (var i = 0; i < params.length; i++) {
    var tmp = params[i].split('=');
    data[tmp[0]] = decodeURIComponent(tmp[1]);
  }
  // Display the exercise name
  var outputElement = document.getElementById("output");
  outputElement.innerHTML = data.name;


  // Get the exercises string from the output element's innerHTML
  var exercisesString = outputElement.innerHTML
  exercisesString = exercisesString.replace("Exercises: ", "");

  // Split the exercises string into an array using commas as the separator
  var exercises = exercisesString.split(",");

  // Remove spaces and convert to lowercase for each item in the array
  for (var i = 0; i < exercises.length; i++) {
    exercises[i] = exercises[i].trim().toLowerCase().replace(/\s/g, '');
  }

  console.log(exercises);

  // Load the exercise based on the URL parameters
  var currentExerciseIndex = 0;
  var exerciseName = data.exercise;
  if (exerciseName) {
    currentExerciseIndex = exercises.indexOf(exerciseName.toLowerCase());
    if (currentExerciseIndex === -1) {
      currentExerciseIndex = 0;
    }
  }

  // Load the current exercise
  console.log(exercises[currentExerciseIndex]);

  // Load the next exercise when the "Next" button is clicked
  var nextButton = document.getElementById("next-btn");
  nextButton.addEventListener("click", function () {
    currentExerciseIndex++;
    if (currentExerciseIndex >= exercises.length) {
      currentExerciseIndex = 0; // Wrap around to the first exercise
    }
    var url = '/' + exercises[currentExerciseIndex] + "?name=" + encodeURIComponent("Exercises: " + exercisesString) + "&exercise=" + encodeURIComponent(exercises[currentExerciseIndex]);
    window.location.href = url;
    var prevButton = document.getElementById("prev-btn");
    prevButton.disabled = false;

    if (currentExerciseIndex === exercises.length - 1) {
      nextButton.disabled = true;
    } else {
      nextButton.disabled = false;
    }
  });

  // Load the previous exercise when the "Prev" button is clicked
  var prevButton = document.getElementById("prev-btn");
  prevButton.addEventListener("click", function () {
    currentExerciseIndex--;
    if (currentExerciseIndex < 0) {
      currentExerciseIndex = 0;
    }
    var url = '/' + exercises[currentExerciseIndex] + "?name=" + encodeURIComponent("Exercises: " + exercisesString) + "&exercise=" + encodeURIComponent(exercises[currentExerciseIndex]);
    window.location.href = url;
    nextButton.disabled = false;

    if (currentExerciseIndex === 0) {
      prevButton.disabled = true;
    } else {
      prevButton.disabled = false;
    }
  });

  // Disable the previous button if we're on the first exercise
  if (currentExerciseIndex === 0) {
    prevButton.disabled = true;
  }
};

