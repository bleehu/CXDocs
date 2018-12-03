(function(){

window.onload = function(){
	randobutton = document.getElementById("RandomButton");
	randobutton.onclick = randomNPC;
	str = document.getElementById("Strength");
	per = document.getElementById("Perception");
	fort = document.getElementById("Fortitude");
	cha = document.getElementById("Charisma");
	smart = document.getElementById("Intelligence");
	dex = document.getElementById("Dexterity");
	luk = document.getElementById("Luck");
	shk = document.getElementById("Shock");
	will = document.getElementById("Will");
	ref = document.getElementById("Reflex");
	str.onchange = updateStats;
	per.onchange = updateStats;
	smart.onchange = updateStats;
	cha.onchange = updateStats;
	dex.onchange = updateStats;
	luk.onchange = updateStats;
	export_text_button = document.getElementById("textButton");
	export_text_button.onclick = export_text;
	
}

function get_name(){
	namebox = document.getElementById("unit_name");
	unit_name = namebox.value;
	if (unit_name != ""){
		return unit_name;
	} else {
		alert("Please enter a name for your unit!")
		namebox.focus();
		return false;
	}
}

function get_level(){
	levelbox = document.getElementById("unit_level");
	unit_level = parseInt(levelbox.value);
	return unit_level;
}

function get_role(){
	rolebox = document.getElementById("role");
	unit_role = rolebox.value;
	return unit_role;
}



function updateStats(){
	str = document.getElementById("Strength");
	per = document.getElementById("Perception");
	fort = document.getElementById("Fortitude");
	cha = document.getElementById("Charisma");
	smart = document.getElementById("Intelligence");
	dex = document.getElementById("Dexterity");
	luk = document.getElementById("Luck");
	shk = document.getElementById("Shock");
	will = document.getElementById("Will");
	ref = document.getElementById("Reflex");
	awe = document.getElementById("Awareness");
	
	strength = parseInt(str.value);
	perception = parseInt(per.value);
	fortitude = parseInt(fort.value);
	charisma = parseInt(cha.value);
	intelligence = parseInt(smart.value);
	dexterity = parseInt(dex.value);
	luck = parseInt(luk.value);
	
	shock = 2 * (intelligence + fortitude - 6);
	willsave =  2 * (charisma + fortitude - 6);
	reflex =  2 * (perception + dexterity - 6);
	awareness = 2 * (perception + luck - 6);
	
	total = strength + perception + dexterity + fortitude + charisma + intelligence + luck;
	
	shk.value = shock;
	ref.value = reflex;
	will.value = willsave;
	awe.value = awareness;
	
	tot = document.getElementById("TotalStats");
	tot.value = total;
	
	health = 50 + (10 * fortitude);
	nanites = 50 + (10 * intelligence);
	
	hp = document.getElementById("Health");
	nn = document.getElementById("Nanites");
	speed = document.getElementById("Speed");
	
	hp.value = health;
	nn.value = nanites;
	speed.value = dexterity;
	
	str_mod = document.getElementById("strMod");
	dex_mod = document.getElementById("dexMod");
	fort_mod = document.getElementById("fortMod");
	cha_mod = document.getElementById("chaMod");
	int_mod = document.getElementById("intMod");
	per_mod = document.getElementById("perMod");
	luk_mod = document.getElementById("lukMod");
	
	strengthMod = (strength - 5) * 4;
	perceptionMod = (perception - 5) * 4;
	fortitudeMod = (fortitude - 5) * 4;
	charismaMod = (charisma - 5) * 4;
	dexterityMod = (dexterity - 5) * 4;
	intelligenceMod = (intelligence - 5) * 4;
	luckMod = (luck - 5) * 4;
	
	str_mod.value = strengthMod;
	dex_mod.value = dexterityMod;
	fort_mod.value = fortitudeMod;
	cha_mod.value = charismaMod;
	dex_mod.value = dexterityMod;
	int_mod.value = intelligenceMod;
	luk_mod.value = luckMod;
	
}

function randomNPC(){
	str = document.getElementById("Strength");
	per = document.getElementById("Perception");
	fort = document.getElementById("Fortitude");
	cha = document.getElementById("Charisma");
	smart = document.getElementById("Intelligence");
	dex = document.getElementById("Dexterity");
	luk = document.getElementById("Luck");
	
	str.value = Math.floor((Math.random() * 10) + 1);
	per.value = Math.floor((Math.random() * 10) + 1);
	fort.value = Math.floor((Math.random() * 10) + 1);
	smart.value = Math.floor((Math.random() * 10) + 1);
	cha.value = Math.floor((Math.random() * 10) + 1);
	dex.value = Math.floor((Math.random() * 10) + 1);
	luk.value = Math.floor((Math.random() * 10) + 1);
	updateStats();
}

function export_text(){
	exportArea = document.getElementById("exportArea");
	//dry this up later
	unit_name = get_name();
	if (unit_name == false){
		return false;
	}
	
	unit_level = get_level();
	unit_role = get_role();
	
	str = document.getElementById("Strength");
	per = document.getElementById("Perception");
	fort = document.getElementById("Fortitude");
	cha = document.getElementById("Charisma");
	smart = document.getElementById("Intelligence");
	dex = document.getElementById("Dexterity");
	luk = document.getElementById("Luck");
	shk = document.getElementById("Shock");
	will = document.getElementById("Will");
	ref = document.getElementById("Reflex");
	
	strength = parseInt(str.value);
	perception = parseInt(per.value);
	fortitude = parseInt(fort.value);
	charisma = parseInt(cha.value);
	intelligence = parseInt(smart.value);
	dexterity = parseInt(dex.value);
	luck = parseInt(luk.value);
	
	shock = 2 * (intelligence + fortitude - 6);
	willsave =  2 * (charisma + fortitude - 6);
	reflex =  2 * (perception + dexterity - 6);
	health = 50 + (10 * fortitude);
	nanites = 50 + (10 * intelligence);
	strengthMod = (strength - 5) * 4;
	perceptionMod = (perception - 5) * 4;
	fortitudeMod = (fortitude - 5) * 4;
	charismaMod = (charisma - 5) * 4;
	dexterityMod = (dexterity - 5) * 4;
	intelligenceMod = (intelligence - 5) * 4;
	luckMod = (luck - 5) * 4;
	//end dry
	export_string = "\t\t\t" + unit_name + "\n";
	export_string += "Health:\t\t" + health + "\n";
	export_string += "Level " + unit_level + " \t\t\t\t\t" + unit_role + " unit\n";
	export_string += "Nanites:\t" + nanites + "\n\n";
	export_string += "Ability Sores:\n"
	export_string += "\tStrength:\t\t" + strength + "\t(" + strengthMod + ")\n";
	export_string += "\tDexterity:\t\t" + dexterity + "\t(" + dexterityMod + ")\n";
	export_string += "\tFortitude:\t\t" + fortitude + "\t(" + fortitudeMod + ")\n";
	export_string += "\tPerception:\t\t" + perception + "\t(" + perceptionMod + ")\n";
	export_string += "\tCharisma:\t\t" + charisma + "\t(" + charismaMod + ")\n";
	export_string += "\tIntelligence:\t" + intelligence + "\t(" + intelligenceMod + ")\n";
	export_string += "\tLuck:\t\t\t" + luck + "\t(" + luckMod + ")\n";
	export_string += "\nSaving Throws:\n"
	export_string += "\tShock:\t" + shock + "\n";
	export_string += "\tWill:\t" + willsave + "\n";
	export_string += "\tReflex:\t" + reflex + "\n";
	export_string += "\n";
	export_string += "Resistances:\n";
	export_string += "Weaknesses:\n";
	export_string += "Extra Senses:\n";
	
	exportArea.innerHTML = export_string;
	exportArea.hidden = false;
}

})();