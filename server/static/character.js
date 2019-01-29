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
        $("#maxNanites").blur(checkStats);

        $("#moveSpeed").blur(checkStats);
        $("#carryAbility").blur(checkStats);
        $("#skillGain").blur(checkStats);

        $("#base_stats_pane").show();
        $("#feats_pane").hide();
        $("#skills_pane").hide();

        $("#base_switch").click(showBasics);
        $("#feats_switch").click(showFeats);
        $("#skills_switch").click(showSkills);
        
        //$("#saveCharacterButton").click(saveCharacter);

        $("#newSkillButton").click(getNewSkillId);
        $("#updateSkillsButton").click(updateAllSkills);

        console.log("done initializing character javascript.");
    }

    function saveCharacter(){
        console.log("Beginning saving characters.");

        var str = parseInt($("#str")[0].value); //get the integer of strength
        var per = parseInt($("#per")[0].value); //get the integer of perception
        var fort = parseInt($("#fort")[0].value); //get the integer of fortitude
        var cha = parseInt($("#cha")[0].value); //get the integer of charisma
        var int = parseInt($("#int")[0].value); //get the integer of intelligence
        var dex = parseInt($("#dex")[0].value); //get the integer of dexterity
        var luck = parseInt($("#luck")[0].value); //get the integer of luck
        //we don't bother doing a lot of sanitization at this point; all of this
        // code can be bypassed with Burpsuite or even just the Chrome Console. 
        // instead, we are forced to really sanitize in the back end. However,
        // we can reduce unnecessary traffic by doing some simple checks.
        var newStats = {'strength':str, 'perception': per, 'fortitude': fort, 'charisma': cha};
        newStats['intelligence'] = int;
        newStats['dexterity'] = dex;
        newStats['luck'] = luck;

        var charname = $('#charname').val(); //the .val() syntax is from jquery. It's newer and nicer
        newStats['name'] = charname;

        var nanites = parseInt($('#maxNanites')[0].value); //the [0].value syntax is from plain old javascript.
        newStats['nanites'] = nanites; //it's ugly, but does the same thing. 

        var health = parseInt($('#maxHealth').val());
        newStats['health'] = health;

        newStats['carryAbility'] = parseInt($('#carryAbility').val());
        newStats['moveSpeed'] = parseInt($('#moveSpeed').val());
        newStats['skillGain'] = parseInt($('#skillGain').val());
        newStats['carryAbility'] = parseInt($('#carryAbility').val());
        newStats['class'] = $('#className').val();
        newStats['race'] = $('#race').val();

        var pk_id = parseInt($("#pk_id").val());

        //if the data has a NaN in it, it's just gonna fail anyway. May as well
        // save the bandwidth by not sending the save request. 
        if (str == NaN || per == NaN || fort == NaN || cha == NaN || int == NaN || dex == NaN ||  luck == NaN){
            console.log("NaN'd on basic stats")
            return false;
        } else if ( health == NaN || nanites == NaN || newStats['moveSpeed'] == NaN || newStats['skillGain'] == NaN || newStats['carryAbility'] == NaN) {
            console.log("NaN'd on other stats")
            return false;
        }

        var saveRequest = $.ajax({
            method: "PUT",
            URL: "/character/modify/" + pk_id,
            data: newStats});
        saveRequest.done(saveSuccess);
        saveRequest.fail(saveWarn);
    }

    function saveSuccess(){
        //TODO set flash notification that character was saved successfully
        console.log("Save Success!");
    }

    function saveWarn(){
        //TODO how do I get this to wire up? .error?
        var blahblah = this;
        console.log(this);
        console.log("Not saving due to a NaN.");
    }

    function checkStats(){
        var valid = true;

        var str = parseInt($("#str")[0].value); //get the integer of strength
        var per = parseInt($("#per")[0].value); //get the integer of perception
        var fort = parseInt($("#fort")[0].value); //get the integer of fortitude
        var cha = parseInt($("#cha")[0].value); //get the integer of charisma
        var int = parseInt($("#int")[0].value); //get the integer of intelligence
        var dex = parseInt($("#dex")[0].value); //get the integer of dexterity
        var luck = parseInt($("#luck")[0].value); //get the integer of luck
        
        if (!checkName()){
            valid = false;
        }

        checkNanites();
        checkHealth();
        checkLevel();

        checkSkillGain();
        checkMoveSpeed();
        checkCarryAbility();

        var strMod = getMod(str);
        var perMod = getMod(per);
        var fortMod = getMod(fort);
        var chaMod = getMod(cha);
        var intMod = getMod(int);
        var dexMod = getMod(dex);
        var luckMod = getMod(luck);

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

        return valid;
    }

    function getMod(baseStat){
        return (baseStat - 5) * 4; 
    }

    function checkName(){
        var name = $("#charname").val();
        var nameBox = $("#charname");
        var validName = name.length > 0;
        //if name is at least 1 character long, and doesn't contain a barred symbol
        if (name.indexOf("<") != -1 || name.indexOf(">") != -1 || name.indexOf("/") != -1)
            validName = false;
        if (validName){
            nameBox.addClass("is-valid");
            nameBox.removeClass("is-invalid");
            return true;
        } else {
            //light up red and show invalid feedback
            nameBox.removeClass("is-valid");
            nameBox.addClass("is-invalid");
            return false;
        }
    }

    function checkLevel(){
        var level = parseInt($("#level").val());
        var levelBox = $("#level");
        //check that the level is a number between 0 and 50.
        if (level != NaN && level > -1 && level < 51){
            //light up green and hide invalid feedback
            levelBox.addClass("is-valid");
            levelBox.removeClass("is-invalid");
        } else {
            //light up red and show invalid feedback
            levelBox.removeClass("is-valid");
            levelBox.addClass("is-invalid");
        }
    }

    function checkCarryAbility(){
        var str = parseInt($("#str").val()); //get the integer of Strength
        var fort = parseInt($("#fort").val()); //get the integer input from Dexterity 
        var carryAbility = parseInt($("#carryAbility").val());
        var expectedCarryAbility = Math.max(str, fort);
        var carryBox = $("#carryAbility"); //get the jquery object representing the skillgain input tag
        if (carryAbility == expectedCarryAbility){
            // Light health input field up green
            carryBox.addClass("is-valid"); // by using the class list, we set more than one class at a time
            carryBox.removeClass("is-invalid");
        } else {
            // Light up red
            carryBox.addClass("is-invalid");
            carryBox.removeClass("is-valid");
        }
    }

    function checkMoveSpeed(){
        var str = parseInt($("#int").val()); //get the integer of Intelligence
        var dex = parseInt($("#dex").val()); //get the integer input from Dexterity 
        var moveSpeed = parseInt($("#moveSpeed").val());
        var expectedMoveSpeed = Math.max(str, dex);
        var moveSpeedBox = $("#moveSpeed"); //get the jquery object representing the skillgain input tag
        if (moveSpeed == expectedMoveSpeed){
            // Light health input field up green
            moveSpeedBox.addClass("is-valid"); // by using the class list, we set more than one class at a time
            moveSpeedBox.removeClass("is-invalid");
        } else {
            // Light up red
            moveSpeedBox.addClass("is-invalid");
            moveSpeedBox.removeClass("is-valid");
        }
    }

    function checkSkillGain(){
        var int = parseInt($("#int").val()); //get the integer of Intelligence
        var cha = parseInt($("#cha").val()); //get the integer input from charisma
        var skillGain = parseInt($("#skillGain").val());
        var expectedskillGain = Math.max(int, cha);
        var skillGainBox = $("#skillGain"); //get the jquery object representing the skillgain input tag
        if (skillGain == expectedskillGain){
            // Light health input field up green
            skillGainBox.addClass("is-valid"); // by using the class list, we set more than one class at a time
            skillGainBox.removeClass("is-invalid");
        } else {
            // Light up red
            skillGainBox.addClass("is-invalid");
            skillGainBox.removeClass("is-valid");
        }
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

    function showBasics(){
        $("#base_stats_pane").fadeIn();
        $("#feats_pane").hide();
        $("#skills_pane").hide();
    }

    function showFeats(){
        $("#base_stats_pane").hide();
        $("#feats_pane").fadeIn();
        $("#skills_pane").hide();
    }

    function showSkills(){
        $("#base_stats_pane").hide();
        $("#feats_pane").hide();
        $("#skills_pane").fadeIn();
    }

    function getNewSkillId(){
        var pk_id = parseInt($("#newSkillButton").attr("character_id"));
        $.post("/skills/new/" + pk_id, AddNewSkillSpace);
    }

    function AddNewSkillSpace(data){
        //note to self, we need an asynch call to the server to find out what our next pk_id is.
        var nameDiv = document.createElement("div");
        nameDiv.className = "col-lg-4";
        var nameInput = document.createElement("input");
        nameInput.type = "text";
        nameInput.value = "newSkill";
        nameDiv.appendChild(nameInput);
        var numberDiv = $("<div>", {"class":"col-lg-4"});
        var numberInput = $("<input>",{"type":"text", "value":0,});
        numberDiv.append(numberInput);
        var buttonDiv = $("<div>", {"class":"col-lg-4"});
        var delButton = $("<input>", {"class":"btn btn-danger", "type":"button", "value":"Delete Skill"});
        buttonDiv.append(delButton);
        $("#skillDiv").append(nameDiv, numberDiv, buttonDiv);
    }

    function updateAllSkills(){
        $(".skillNames").each(updateASkill);
    }

    function updateASkill(){
        var name = $(this).attr("name");
        var id = parseInt(name.replace("Label",""));
        var skillName = $(this).val();
        var skillPointsString = $("#" + id + "number").val();
        skillPointsString = skillPointsString.replace("number", "");
        var skillPoints = parseInt(skillPointsString);
        var payload = {"pk_id":id, "skillName":skillName, "skillPoints":skillPoints};
        $.ajax({
            type:"POST",
            url:"/skills/modify/" + id,
            data:payload,
            asynch: true,
            success: function(){
                console.log("updated skill pk_id:" + id);
            }
        });
    }

})();