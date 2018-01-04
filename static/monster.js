
//This file uses AJAX to reach out to the github API to retrieve and display news on recent development.
(function(){
    $(document).ready(initialize)

    function initialize(){
        $(".inspectable").find(".dropdown-toggle").click(toggleMe);
        $(".inspectable").each(hideMe);
    }

    function hideMe(){
        var myBody = $(this).parent().find(".card-body");
        $(myBody).collapse('hide');
    }
    function showMe(){
        var myBody = $(this).parent().find(".card-body");
        $(myBody).collapse('show');
    }
    function toggleMe(){
        var myBody = $(this).parent().parent().find(".card-body");
        $(myBody).collapse('toggle');
    }

})();