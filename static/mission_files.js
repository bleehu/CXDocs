var template = {
	title:"Template",
	rLevel:"",
	rPartySize:"",
	environment:"",
	combat:"High, Medium, or Low",
	puzzle:"High, Medium, or Low",
	rp:"High, Medium, or Low",
	linkCard1: [
		["/", "Name of Link"],
	],
	linkCard2: [
		["/", "Name of Link"],
	],
	description: "Summarize!",
	author:"You!"
};

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

var missions = [
	template,
	cassandra
];

$(document).ready(function(){
	
	for (i = 0; i < missions.length; i++) {
		
		var newCLink = $("<a></a>").attr({
			"class" : "list-group-item list-group-item-action",
			"href" : "#" + missions[i].title + "panel"
		})
		.html(missions[i].title);
		$("#missionToC").append(newCLink);
		
		<!-- Above builds the Table of Contents, below builds the cards. -->
		
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
				$("<dt></dt>").html("Recommended Level"), $("<dd></dd>").html(missions[i].rLevel), "\n",
				$("<dt></dt>").html("Recommended Party Size"), $("<dd></dd>").html(missions[i].rPartySize), "\n",
				$("<dt></dt>").html("Environment"), $("<dd></dd>").html(missions[i].environment), "\n",
				$("<dt></dt>").html("Combat"), $("<dd></dd>").html(missions[i].combat), "\n",
				$("<dt></dt>").html("Puzzle"), $("<dd></dd>").html(missions[i].puzzle), "\n",
				$("<dt></dt>").html("Roleplay"), $("<dd></dd>").html(missions[i].rp)
			),
		);
		var linkCard1 = $("<ul></ul>").attr({
			"class" : "col-lg-2 col-md-3 col-sm-4"
		});
		for(j = 0; j < missions[i].linkCard1.length; j++) {
			linkCard1.append(
				$("<li></li>").append(
					$("<a></a>").attr({
						"href" : missions[i].linkCard1[j][0]
					})
					.html(missions[i].linkCard1[j][1])
				)
			);
		}
		var linkCard2 = $("<ul></ul>").attr({
			"class" : "col-lg-3 col-md-3 col-sm-4"
		});
		for(k = 0; k < missions[i].linkCard2.length; k++) {
			linkCard2.append(
				$("<li></li>").append(
					$("<a></a>").attr({
						"href" : missions[i].linkCard2[k][0]
					})
					.html(missions[i].linkCard2[k][1])
				)
			);
		}
		row1.append(linkCard1, linkCard2);
		
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