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
	
	strength = parseInt(str.value);
	perception = parseInt(per.value);
	fortitude = parseInt(fort.value);
	charisma = parseInt(cha.value);
	intelligence = parseInt(str.value);
	dexterity = parseInt(dex.value);
	luck = parseInt(luk.value);
	
	shock = 2 * (intelligence + fortitude - 6);
	willsave =  2 * (charisma + fortitude - 6);
	reflex =  2 * (perception + dexterity - 6);
	
	total = strength + perception + dexterity + fortitude + charisma + intelligence + luck;
	
	shk.value = shock;
	ref.value = reflex;
	will.value = willsave;
	
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

})();