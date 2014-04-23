// Sets click listener to list items to move/animate movement between lists
function setSwitchActions(firstList, secondList) {
  var setMoveAction = function(currentList, newList) {
    $(currentList).on('click', '.list-group-item', function(event) {
      var $movingItem = $(this);
      $movingItem.fadeOut(function() {
        $movingItem.appendTo(newList);
        $movingItem.fadeIn();
      });
    });
  }

  setMoveAction(firstList, secondList);
  setMoveAction(secondList, firstList);
}

// Adds hidden input before form is submitted that contains all selected IDs
function bundleSelectionsOnSubmit(values) {
  $(values.buttonID).on('click', function(event) {
    var ids = [];
    $selectedItems = $(values.selectedItemsSelector);
    _.each($selectedItems, function(item) {
      ids.push($(item).data(values.dataID));
    });
    $('form').append(
      $('<input type="hidden" value="' + JSON.stringify(ids) + '" name="' + values.inputName + '">')
    );
  });
}

/*
 * Displays info modal when a user clicks on the info button for that course
 */
function setInfoModalListener() {
  $('.info-button').on('click', function(event) {
    var courseID = $(this).closest('tr').data('id');
    $.post(
      '/api/course_info',
      { course_id : courseID }
    ).done(function(res){
      $('#course_name').text(res.info.name);
      $('#provider').text(res.info.provider);
      $('#subject').text(res.info.subjects);
      $('#course_ins').text(res.info.instructor);
      $('#course_desc').text(res.info.description);
      $('#url').text(res.info.url);
      $('#url').attr('href', res.info.url);
      $('#helpout-url').attr('href', res.info.helpouturl);
      $('#similar_course_1').text(res.info.similar_courses_names[0])
      $('#similar_course_1_link').attr('href', res.info.similar_courses_links[0])
      $('#similar_course_2').text(res.info.similar_courses_names[1])
      $('#similar_course_2_link').attr('href', res.info.similar_courses_links[1])
      $('#similar_course_3').text(res.info.similar_courses_names[2])
      $('#similar_course_3_link').attr('href', res.info.similar_courses_links[2])
    });
  });
}
