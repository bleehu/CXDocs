
//This file uses AJAX to reach out to the github API to retrieve and display news on recent development.
(function(){
    $(document).ready(initialize)

    function initialize(){
        console.log("Who's here file loaded.");
        //check who's here every minute
        setInterval(askWhosHere, 60000);
        askWhosHere();
        $("#whosHereToggle").click(toggleMenu);
        $("#whosHereToggle").blur(blurMenu);
        console.log("done initializing who's here function.");
    }

    function askWhosHere(){
        var whoHereRequest = new XMLHttpRequest();
        whoHereRequest.onreadystatechange = thatsWhosHere;
        whoHereRequest.open("GET", "/whoshere", true);
        whoHereRequest.send();
    }

    function thatsWhosHere(){
        console.log(this.responseText);
        var whosHereDiv = document.getElementById("whosHereDiv");
        var report = JSON.parse(this.responseText);
        whosHereDiv.innerHTML = ""; //remove old data
        for(var signature in report){
            var signatureElement = document.createElement("a");
            signatureElement.classList.add("dropdown-item");
            if (report[signature]['status'] == 'in'){
                signatureElement.classList.add("text-success");
            } else if (report[signature]['status'] == 'away'){
                signatureElement.classList.add('text-warning');
            }
            signatureElement.innerHTML = signature;
            whosHereDiv.appendChild(signatureElement)
            var divider = document.createElement("div");
            divider.classList.add("dropdown-divider");
            whosHereDiv.appendChild(divider);
        }
        signatureCount = Object.keys(report).length;
        $('#hereCount').html("There are " + signatureCount + " people on.");
    }

    function toggleMenu(){
        $('#whosHereDiv').toggle();
    }

    function blurMenu(){
        $('#whosHereDiv').hide();
    }
})();