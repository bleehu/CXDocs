
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


    def __str__():
        return "{name:%s}" % self.name


