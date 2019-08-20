from ..server.characters.weapons.attachments.attachments import WeaponAttachment

def test_weapon_attachments():
    red_laser = WeaponAttachment()
    red_laser.name = "Red Laser"
    red_laser.description = "This is a very red laser."
    red_laser.hipfireMod = -2
    assert red_laser.hipfireMod == -2