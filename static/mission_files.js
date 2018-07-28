// To add your mission, copy the template variable, fill in all the fields, and de-comment it.
// Rename your new template to reflect your mission, and add its name to the end of the missions array.
// Then add your linked files to the repository.

(function(){
	/*var template = {
		title:"Template",
		rLevel:"",
		rPartySize:"",
		environment:"",
		combat:"High, Medium, or Low",
		puzzle:"High, Medium, or Low",
		rp:"High, Medium, or Low",
		linkCard1: [
			["/filepath", "Name of Link"],
		],
		linkCard2: [
			["/filepath", "Name of Link"],
		],
		description: "Summarize!",
		author:"You!"
	};*/
	
	var cassandra = {
		title:"The <i>Cassandra</i>",
		rLevel:"&lt 5",
		rPartySize:"4-5",
		environment:"Spaceship Interior",
		combat:"High",
		puzzle:"Medium",
		rp:"Low",
		linkCard1: [
			["static/files/cassandra/script.pdf", "Mission Script"],
			["static/files/cassandra/roomlist.pdf", "Room Listing"],
			["static/files/cassandra/loottables.pdf", "Loot Tables"]
		],
		linkCard2: [
			["static/files/cassandra/b-schematics.pdf", "Blank Schematics"],
			["static/files/cassandra/a-schematics.pdf", "Annotated Schematics"]
		],
		description: "A privately owned and operated freighter, The <i>Cassandra</i>, carrying \
						(among other things) some cargo of value to WY Corp has been hijacked \
						by pirates. They have been spotted at an orbital transfer station \
						above Vecnasai in the Alabaster system. Players will be contracted to \
						re-hijack the freighter and deliver it and all of its cargo to the WY \
						Corporate docks in the near-ish Mendel system.",
		author:"Turtlelord"
	};

	var hive_mission = {
		title: "The Hive",
		rLevel: "&lt 5",
		rPartySize: "4-6",
		environment: "Spaceport",
		combat: "High",
		puzzle: "Low",
		rp: "Medium",
		linkCard1: [
			["static/files/the_hive/script.pdf","Mission Script"],
			["static/files/the_hive/rewards.pdf","Rewards"]
		],
		linkCard2: [
			["static/files/the_hive/simple map.pdf","Simple Map"]
		],
		description: "The small town of Orrton has a terrible pest problem. \
			Local Antlions have been eating people in the streets and have\
			set up their hive in the spaceport that the town uses to get \
			much-needed supplies. A brave band of heros are needed to take back\
			the vital space port! And if altruistic heros are in short supply,\
			the town's mayor is offering a handsome reward...",
		author: "Bleehu"
	};
	
	var missions = [
		cassandra
	];
	
	function populateLinkCard(css, linkCardData) {
		var linkCard = $("<ul></ul>").attr({
			"class" : css
		});
		for(j = 0; j < linkCardData.length; j++) {
			linkCard.append(
				$("<li></li>").append(
					$("<a></a>").attr({
						"href" : linkCardData[j][0]
					})
					.html(linkCardData[j][1])
				)
			);
		}
		return linkCard;
	}
	
	$(document).ready(function(){
		
		for (i = 0; i < missions.length; i++) {
			
			var newCLink = $("<a></a>").attr({
				"class" : "list-group-item list-group-item-action",
				"href" : "#" + missions[i].title + "panel"
			})
			.html(missions[i].title);
			$("#missionToC").append(newCLink);
			
			//Above builds the Table of Contents, below builds the cards.
			
			var newCard = $("<div></div>").attr({
				"class" : "card text-white bg-secondary mb-3",
				"id" : missions[i].title + "panel"
			});
			
			var newCardHeader = $("<div></div>").attr({
				"class" : "card-header"
			})
			.html(missions[i].title);
			
			var newCardBody = $("<div></div>").attr({
				"class" : "card-body"
			});
			
			var row1 = $("<div></div>").attr({
				"class" : "row"
			})
			.append(
				$("<dl></dl>").attr({
					"class" : "col-lg-6 col-md-6"
				}).append(
					$("<dt></dt>").html("Recommended Level"), $("<dd></dd>").html(missions[i].rLevel),
					$("<dt></dt>").html("Recommended Party Size"), $("<dd></dd>").html(missions[i].rPartySize),
					$("<dt></dt>").html("Environment"), $("<dd></dd>").html(missions[i].environment),
					$("<dt></dt>").html("Combat"), $("<dd></dd>").html(missions[i].combat),
					$("<dt></dt>").html("Puzzle"), $("<dd></dd>").html(missions[i].puzzle),
					$("<dt></dt>").html("Roleplay"), $("<dd></dd>").html(missions[i].rp)
				),
			);
			row1.append(populateLinkCard("col-lg-2 col-md-3 col-sm-4", missions[i].linkCard1), 
						populateLinkCard("col-lg-3 col-md-3 col-sm-4", missions[i].linkCard2));
			var row2 = $("<div></div>").attr({
				"class" : "row"
			})
			.append(
				$("<div></div>").attr({
					"class" : "col-lg-9"
				})
				.append(
					$("<p></p>").html(missions[i].description)
				)
			);
			
			var row3 = $("<div></div>").attr({
				"class" : "col-lg-8"
			})
			.append(
				$("<p></p>").html("This mission compiled and published by " + missions[i].author + "."),
				$("<p></p>").append(
					$("<a></a>").attr({
						"href" : "#top",
						"class" : "btn btn-info btn-xs"
					})
					.html("Back to Top")
				)
			);
			
			newCardBody.append(row1, row2, row3);
			newCard.append(newCardHeader, newCardBody);
			$("#missionSpot").append(newCard);
		}
	});
})();