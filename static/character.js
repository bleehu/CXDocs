
//This file uses AJAX to reach out to the github API to retrieve and display news on recent development.
(function(){
    $(document).ready(initialize)

    function initialize(){
        console.log("Starting character javascript.");
        
        $("#name").blur(checkStats); //the dollarsign engages the jquery flavor of javascript.
        $("#str").blur(checkStats); // the string starting with the pound sign looks for an element with that id.
        $("#cha").blur(checkStats); // the blur method attaches a listener that fires when the element loses focus.
        $("#dex").blur(checkStats); 
        $("#per").blur(checkStats);
        $("#fort").blur(checkStats);
        $("#int").blur(checkStats);
        $("#luck").blur(checkStats);

        $("#maxHealth").blur(checkStats);
        $("maxNanites").blur(checkStats);


        console.log("done initializing character javascript.");
    }

    function checkStats(){
        var str = parseInt($("#str")[0].value); //get the integer of strength
        var per = parseInt($("#per")[0].value); //get the integer of perception
        var fort = parseInt($("#fort")[0].value); //get the integer of fortitude
        var cha = parseInt($("#cha")[0].value); //get the integer of charisma
        var int = parseInt($("#int")[0].value); //get the integer of intelligence
        var dex = parseInt($("#dex")[0].value); //get the integer of dexterity
        var luck = parseInt($("#luck")[0].value); //get the integer of luck
        
        checkNanites();
        checkHealth();

        var strMod = getMod(str);
        var perMod = getMod(per);
        var fortMod = getMod(fort);
        var chaMod = getMod(cha);
        var intMod = getMod(int);
        var dexMod = getMod(dex);
        var luckMod = getMod(luck);

        var moveSpeed = Math.max(str, dex);
        var carryCap = Math.max(str, fort);
        var skillGain = Math.max(int, cha);

        var willScore = 2 * (cha + fort - 6);
        var reflexScore = 2 * (per + dex - 6);
        var shockScore = 2 * (fort + int - 6);

        $("#strmod").val(strMod);
        $("#permod").val(perMod);
        $("#fortmod").val(fortMod);
        $("#chamod").val(chaMod);
        $("#intmod").val(intMod);
        $("#dexmod").val(dexMod);
        $("#luckmod").val(luckMod);

        $("#will").val(willScore);
        $("#reflex").val(reflexScore);
        $("#shock").val(shockScore);

        var totalStats = str + per + fort + cha + int + dex + luck;
        $("#totalStats").val(totalStats);

    }

    function getMod(baseStat){
        return (baseStat - 5) * 4; 
    }

    function checkHealth(){
        var fort = parseInt($("#fort").val()); //get the integer of fortitude
        var health = parseInt($("#maxHealth").val());
        var expectedHealth = 50 + (10 * fort);
        var healthBox = $("#maxHealth");
        if (health == expectedHealth){
            // Light health input field up green
            healthBox.addClass("is-valid"); // by using the class list, we set more than one class at a time
            healthBox.removeClass("is-invalid");
        } else {
            // Light up red
            healthBox.addClass("is-invalid");
            healthBox.removeClass("is-valid");
        }
    }

    function checkNanites(){
        var int = parseInt($("#int").val()); //get the integer of fortitude
        var nanites = parseInt($("#maxNanites")[0].value);
        var expectedNanites = 50 + (10 * int);
        var naniteBox = $("#maxNanites");
        if (nanites == expectedNanites){
            // Light health input field up green
            naniteBox.addClass("is-valid"); // by using the class list, we set more than one class at a time
            naniteBox.removeClass("is-invalid");
        } else {
            // Light up red
            naniteBox.addClass("is-invalid");
            naniteBox.removeClass("is-valid");
        }
    }

    function toggleMenu(){
        $('#whosHereDiv').toggle();
    }

    function blurMenu(){
        $('#whosHereDiv').hide();
    }
})();