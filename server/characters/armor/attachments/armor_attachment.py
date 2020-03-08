
class Armor_Attachment:

    Select_Predicate = "SELECT pk_id, \
        name, \
        shield_capacity,\
        recharge_rate,\
        recharge_delay,\
        cloaking_dc,\
        hardpoints\
        FROM armor_attachments"

    def __init__(self, line):
        self.pk_id = int(line[0])
        self.name = line[1]
        self.shield_capacity = int(line[2])
        self.recharge_rate = int(line[3])
        self.recharge_delay = int(line[4])
        self.cloaking_dc = int(line[5])
        self.hardpoints = int(line[6])

    def __repr__(self):
        return_me = {"name":self.name, "shield_capacity":self.shield_capacity, 
            "pk_id":self.pk_id, "recharge_rate": self.recharge_rate, 
            "recharge_delay":self.recharge_delay, "cloaking_dc":self.cloaking_dc,
            "hardpoints":self.hardpoints}
        return return_me

    def __str__(self):
        return "{name:%s}" % self.name


