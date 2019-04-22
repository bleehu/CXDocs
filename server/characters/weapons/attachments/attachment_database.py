from ....database import database
from ....cxExceptions import cxExceptions
from attachments import WeaponAttachment

class AttachmentDatabase(database.CXDatabase):

    PROPERTY_LIST = "pk_id, name, slot, description, full_auto_mod, r1_mod, r2_mod, r3_mod, hipfire_mod, reflex_mod"

    def __init__(self, config, log):
        #set defaults
        config_map = {"port": 5432, "db_host":"localhost", "db_name":"mydb"}
        for key in config:
            config_map[key] = config[key]
        self.log = log
        super(AttachmentDatabase, self).__init__(config_map) #do whatever initialization all CX Databases do

    def get_all_available_attachments(self):
        query_string = "SELECT %s FROM available_attachments ORDER BY slot, name;" % AttachmentDatabase.PROPERTY_LIST
        available_attachments = []
        results = self.fetch_all(query_string)
        for line in results:
            attachment_map = tuple_to_attachment_map(line)
            new_attachment = WeaponAttachment(attachment_map)
            available_attachments.append(new_attachment)
        return available_attachments

    def get_available_attachment_by_id(self, pk_id):
        query_string = "SELECT %s FROM available_attachments WHERE pk_id = %s;" % (AttachmentDatabase.PROPERTY_LIST, pk_id)
        result = self.fetch_first(query_string)
        attachment_map = tuple_to_attachment_map(result)
        new_attachment = WeaponAttachment(attachment_map)
        return new_attachment

def tuple_to_attachment_map(line):
    attachment_map = {'name': line[1]}
    attachment_map['pk_id'] = int(line[0])
    attachment_map['slot'] = line[2]
    attachment_map['description'] = line[3]
    attachment_map['fullAutoMod'] = int_or_none(line[4])
    attachment_map['r1Mod'] = int_or_none(line[5])
    attachment_map['r2Mod'] = int_or_none(line[6])
    attachment_map['r3Mod'] = int_or_none(line[7])
    attachment_map['hipfireMod'] = int_or_none(line[8])
    attachment_map['reflexMod'] = int_or_none(line[9])
    return attachment_map

def int_or_none(int_string):
    if int_string is None:
        return 0
    else:
        return int(int_string)

#testing
if __name__ == '__main__':
    test_db = AttachmentDatabase({"username":"searcher","password":"Gzp8po1UFNq7"}, None)
    feats = test_db.get_all_available_attachments()

