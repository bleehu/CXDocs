//This file uses AJAX to reach out to the github API to retrieve and display news on recent development.
(function(){
  $(document).ready(initialize)

  function initialize(){
    $(".delete-button").click(deleteCharacter);
  }

  function deleteCharacter(){
    var pk_id = $(this).attr("pk_id");
    var url = '/character/modify/' + pk_id;

    $.ajax(url, {
      method:'DELETE',
      success: function(result){
          console.log("Deleted character with pk_id " + result.id);
          $("#" + result.id).remove();
      }
    });
  }
})();