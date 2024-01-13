//global variables
var monthEl = $(".c-main");
var dataCel = $(".c-cal__cel");
var dateObj = new Date();
var month = dateObj.getUTCMonth() + 1;
var day = dateObj.getUTCDate();
var year1 = dateObj.getUTCFullYear();



var monthText = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];
var indexMonth = month;
var todayBtn = $(".c-today__btn");
var addBtn = $(".js-event__add");
var saveBtn = $(".js-event__save");
var closeBtn = $(".js-event__close");
var winCreator = $(".js-event__creator");
var inputDate = $(this).data();
today = year1 + "-" + month + "-" + day;


// ------ set default events -------
function defaultEvents(dataDay,dataName,dataNotes,classTag){
  var date = $('*[data-day='+dataDay+']');
  date.attr("data-name", dataName);
  date.attr("data-notes", dataNotes);
  date.addClass("event");
  date.addClass("event--" + classTag);
}



// ------ functions control -------

//button of the current day
todayBtn.on("click", function() {
  if (month < indexMonth) {
    var step = indexMonth % month;
    movePrev(step, true);
  } else if (month > indexMonth) {
    var step = month - indexMonth;
    moveNext(step, true);
  }
});

//higlight the cel of current day
dataCel.each(function() {
  if ($(this).data("day") === today) {
    $(this).addClass("isToday");
    fillEventSidebar($(this));
  }
});

//window event creator
addBtn.on("click", function() {
  winCreator.addClass("isVisible");
  $("body").addClass("overlay");
  dataCel.each(function() {
    if ($(this).hasClass("isSelected")) {
      today = $(this).data("day");
      document.querySelector('input[type="date"]').value = today;
    } else {
      document.querySelector('input[type="date"]').value = today;
    }
  });
});
closeBtn.on("click", function() {
  winCreator.removeClass("isVisible");
  $("body").removeClass("overlay");
});
saveBtn.on("click", function() {
  var inputName = $("input[name=name]").val();
  var inputDate = $("input[name=date]").val();
  var inputNotes = $("textarea[name=notes]").val();
  var inputTag = $("select[name=tags]")
    .find(":selected")
    .text();

  dataCel.each(function() {
    if ($(this).data("day") === inputDate) {
      if (inputName != null) {
        $(this).attr("data-name", inputName);
      }
      if (inputNotes != null) {
        $(this).attr("data-notes", inputNotes);
      }
      $(this).addClass("event");
      if (inputTag != null) {
        $(this).addClass("event--" + inputTag);
      }
      fillEventSidebar($(this));
    }
  });

  winCreator.removeClass("isVisible");
  $("body").removeClass("overlay");
  $("#addEvent")[0].reset();
});

//fill sidebar event info
function fillEventSidebar(self) {
  $(".c-aside__event").remove();
  var thisName = self.attr("data-name");
  var thisNotes = self.attr("data-notes");
  var thisImportant = self.hasClass("event--important");
  var thisBirthday = self.hasClass("event--birthday");
  var thisFestivity = self.hasClass("event--festivity");
  var thisEvent = self.hasClass("event");
  
  switch (true) {
    case thisImportant:
      $(".c-aside__eventList").append(
        "<p class='c-aside__event c-aside__event--important'>" +
        thisName +
        " <span> • " +
        thisNotes +
        "</span></p>"
      );
      break;
    case thisBirthday:
      $(".c-aside__eventList").append(
        "<p class='c-aside__event c-aside__event--birthday'>" +
        thisName +
        " <span> • " +
        thisNotes +
        "</span></p>"
      );
      break;
    case thisFestivity:
      $(".c-aside__eventList").append(
        "<p class='c-aside__event c-aside__event--festivity'>" +
        thisName +
        " <span> • " +
        thisNotes +
        "</span></p>"
      );
      break;
    case thisEvent:
      $(".c-aside__eventList").append(
        "<p class='c-aside__event'>" +
        thisName +
        " <span> • " +
        thisNotes +
        "</span></p>"
      );
      break;
   }
};
dataCel.on("click", function() {
  var thisEl = $(this);
  var thisDay = $(this)
  .attr("data-day")
  .slice(8);
  var thisMonth = $(this)
  .attr("data-day")
  .slice(5, 7);

  fillEventSidebar($(this));

  $(".c-aside__num").text(thisDay);
  $(".c-aside__month").text(monthText[thisMonth - 1]);

  dataCel.removeClass("isSelected");
  thisEl.addClass("isSelected");

});

function moveNext(fakeClick, indexNext) {
  for (var i = 0; i < fakeClick; i++) {
    switch (true) {
      case indexNext:
        indexMonth++;
        break;
    }
    $(".c-paginator__month").css({
      left: "-=100%"
    });
    $(".c-main").css({
      left: "-=100%"
    });
  }
  console.log(indexMonth);
}

function movePrev(fakeClick, indexPrev) {
  for (var i = 0; i < fakeClick; i++) {
    switch (true) {
        case indexPrev:
          break;
      }
    $(".c-main").css({
      left: "+=100%"
    });
    $(".c-paginator__month").css({
      left: "+=100%"
    });

  }
}


function buttonsPaginator(buttonId, mainClass, monthClass, next, prev) {
  switch (true) {
    case next:
      $(buttonId).on("click", function() {
        if (indexMonth >= 2) {
          $(mainClass).css({
            left: "+=100%"
          });
          $(monthClass).css({
            left: "+=100%"
          });
          indexMonth -= 1;
          console.log(indexMonth);

        } else {
            if (indexMonth === 1){
                window.year -= 1;
                document.getElementById("year").textContent = window.year;
                console.log(window.year)
              }
    
          $(mainClass).css({
            left: "-=1100%"
          });
          $(monthClass).css({
            left: "-=1100%"
          });
          indexMonth = 12;
          console.log(indexMonth);

        }
        return indexMonth;
      });
      break;
    case prev:
      $(buttonId).on("click", function() {


        if (indexMonth <= 12) {
          
          $(mainClass).css({
            left: "-=100%"
          });
          $(monthClass).css({
            left: "-=100%"
          });
          indexMonth += 1;
          console.log(indexMonth);
          if (indexMonth === 13){
            window.year += 1;
            // External script code
            updateYear(window.year);
            document.addEventListener("DOMContentLoaded", function() {
                document.getElementById("year").textContent = window.year;
              });
            //   let styleSheet = document.createElement('link');
// styleSheet.rel = 'stylesheet';
// styleSheet.type = 'text/css';
// styleSheet.href = '../static/assets/progress.css';
// document.head.appendChild(styleSheet);
            // document.getElementById("year").textContent = window.year;
            // External script code

                        
            // // first day of the week of the new year
            // today = new Date("January 1, " + year);
            // start_day = today.getDay() + 1;
            // fill_table("January", 31, "01");
            // fill_table("February", 28, "02");
            // fill_table("March", 31, "03");
            // fill_table("April", 30, "04");
            // fill_table("May", 31, "05");
            // fill_table("June", 30, "06");
            // fill_table("July", 31, "07");
            // fill_table("August", 31, "08");
            // fill_table("September", 30, "09");
            // fill_table("October", 31, "10");
            // fill_table("November", 30, "11");
            // fill_table("December", 31, "12");
     
            
            console.log(window.year)
            indexMonth = 1;
            console.log(indexMonth);
            $(mainClass).css({
              left: "+=1200%"
            });
            $(monthClass).css({
              left: "+=1200%"
            });
          }

        } else {
          indexMonth = 0;
          console.log(indexMonth);
          $(mainClass).css({
            left: "+=1200%"
          });
          $(monthClass).css({
            left: "+=1200%"
          });
          
          
          

        }
        return indexMonth;
      });
      break;
  }
}

buttonsPaginator("#next", monthEl, ".c-paginator__month", false, true);
buttonsPaginator("#prev", monthEl, ".c-paginator__month", true, false);

//launch function to set the current month
moveNext(indexMonth-1, false);

//fill the sidebar with current day
$(".c-aside__num").text(day);
$(".c-aside__month").text(monthText[month - 1]);
