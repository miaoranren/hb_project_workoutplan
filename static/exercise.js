"use strict";

// This function only exists to avoid creating global variables
function handleStatusUpdate() {
  $('#exercise=form').on('submit', (evt) => {
    evt.preventDefault();


    // Our GET request URL will look like this:
    //       /status?order=123
    $.get('/search',  (results) => {
      const 
      
      $('#exercise_results').html(exercise);

     
    });

}

handleStatusUpdate();
