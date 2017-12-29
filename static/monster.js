
//This file uses AJAX to reach out to the github API to retrieve and display news on recent development.
(function(){
    $(document).ready(initialize)

    function initialize(){
        $(".inspectable").hover(showMe, hideMe);
        $(".inspectable").each(hideMe);
    }

    function hideMe(){
        var myBody = $(this).find(".card-body");
        $(myBody).collapse('hide');
    }
    function showMe(){
        var myBody = $(this).find(".card-body");
        $(myBody).collapse('show');
    }
})();