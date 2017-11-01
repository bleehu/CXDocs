import pdb
import psycopg2

def get_characters():


def validate_character(form, user):
	
	return newCharacter

def insert_character():


def update_character():



"""CREATE SEQUENCE characters_pk_seq NO CYCLE;    
    CREATE TABLE characters (
        pk_id int primary key default nextval('monsters_pk_seq'),
        name text NOT NULL,
        health int NOT NULL CHECK (health > 0),
        nanites int NOT NULL CHECK (nanites > 0),
        strength int NOT NULL CHECK (strength > 0),
        perception int NOT NULL CHECK (perception > 0),
        fortitude int NOT NULL CHECK (fortitude > 0),
        charisma int NOT NULL CHECK (charisma > 0),
        intelligence int NOT NULL CHECK (intelligence > 0),
        dexterity int NOT NULL CHECK (dexterity > 0),
        luck int NOT NULL CHECK (luck > 0),
        level int NOT NULL CHECK (level > -1),
        shock int NOT NULL,
        will int NOT NULL,
        reflex int NOT NULL,
        description text,
    	race text NOT NULL,
    	class text NOT NULL,
        fk_owner_id int references users(pk_id) ON DELETE CASCADE,
        int money default 0,
        created_at timestamp NOT NULL DEFAULT now()
    );
INSERT INTO characters (fk_owner_id, name, health, nanites, strength, perception, fortitude, charisma, intelligence, dexterity, luck, level, shock, will, reflex, race, class) VALUES
(1, 'test', 100, 110, 8, 5, 6, 7, 8, 6, 2, 1, 12, 12, 12, 'Human', 'Gunslinger');



    """