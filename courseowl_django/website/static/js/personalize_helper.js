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