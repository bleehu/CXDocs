
//This file uses AJAX to reach out to the github API to retrieve and display news on recent development.
(function(){
    $(document).ready(initialize)

    function initialize(){
        var today = new Date();
        var thisMonth = today.getMonth();
        var lastMonth = new Date();
        lastMonth.setMonth(thisMonth - 1);
        startString= lastMonth.toISOString();

        var cxUpdateRequest = new XMLHttpRequest();
        cxUpdateRequest.onreadystatechange = gitNews;
        cxUpdateRequest.open("GET", "https://api.github.com/repos/bleehu/compound_x/commits?since=" + startString, true);
        cxUpdateRequest.send();

        var doxUpdateRequest = new XMLHttpRequest();
        doxUpdateRequest.onreadystatechange = doxNews;
        doxUpdateRequest.open("GET", "https://api.github.com/repos/bleehu/CXDocs/commits?since=" + startString, true);
        doxUpdateRequest.send();

    }

    function gitNews(){
        var myNewsDiv = document.getElementById("cxNewsDiv");
        console.log(this.responseText);
        try
        {
            var report = JSON.parse(this.responseText);
            myNewsDiv.innerHTML = "<h2> CX Dev News </h2>";
            for (var itteration = 0; itteration < 5; itteration++){
                var commit = report[itteration]["commit"];
                reportCommit(commit, myNewsDiv);
            }
        } catch (err){

        }
    }

    function doxNews(){
        var myNewsDiv = document.getElementById("doxNewsDiv");
        try{
            var report = JSON.parse(this.responseText);
            myNewsDiv.innerHTML = "<h2> CX Docs News </h2>";
            for (var itteration = 0; itteration < 5; itteration++){
                var commit = report[itteration]["commit"];
                reportCommit(commit, myNewsDiv);
            }
        } catch(err){

        }
    }

    function reportCommit(commit, newsDiv){
        if (commit != null){
            var panel = document.createElement("div");
            panel.classList.add("panel");
            panel.classList.add("panel-primary");
            var panelHeading = document.createElement("div");
            panelHeading.classList.add("panel-heading");
            var title = document.createElement("h4");
            title.classList.add("panel-title");
            var panelContent = document.createElement("div");
            panelContent.classList.add("panel-body");
            var author = commit['author']['name'];
            var message = commit['message'];
            var time = commit['author']['date'];

            title.textContent = time;

            panelContent.textContent = author + " : ";
            panelContent.textContent += time + ". ";
            panelContent.textContent += message;

            panelHeading.appendChild(title);
            panel.appendChild(panelHeading);
            panel.appendChild(panelContent);

            newsDiv.appendChild(panel);
        }
    }


})();