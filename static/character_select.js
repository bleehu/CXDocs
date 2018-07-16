
//This file uses AJAX to reach out to the github API to retrieve and display news on recent development.
(function(){
    $(document).ready(initialize)

    function initialize(){
        console.log("Starting character select javascript.");
        
        $(".deleteButton").click(deleteCharacter); 
        
        //$("#saveCharacterButton").click(saveCharacter);

        console.log("done initializing character select javascript.");
    }

    function deleteCharacter(){
        var pk_id = $(this).attr("pk_id");
        $.ajax({
            url:'/character/modify/' + pk_id,
            type:'DELETE',
            success: function(result){
                //notify of success
                console.log("Deleted Character with pk_id " + pk_id);
                location.reload();
            }
        });
    }


})();