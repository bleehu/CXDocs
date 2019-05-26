import pdb

ATTACHMENT_SLOTS = ["Optics", 
    "Rail",
    "Laser", 
    "Muzzle", 
    "Barrel", 
    "Sling"]

class WeaponAttachment:

    def __init__(self, attachmentMap = None):
        if attachmentMap is not None:
            self.name = attachmentMap['name']
            self.description = attachmentMap['description']
            self.slot = attachmentMap['slot']
            self.fullAutoMod = int(attachmentMap['fullAutoMod'])
            self.r1Mod = int(attachmentMap['r1Mod'])
            self.r2Mod = int(attachmentMap['r2Mod'])
            self.r3Mod = int(attachmentMap['r3Mod'])
            self.hipfireMod = int(attachmentMap['hipfireMod'])
            self.reflexMod = int(attachmentMap['reflexMod'])
        else:
            self.name = "Unnamed"
            self.description = "Description Missing"
            self.slot = "Rail"
            self.fullAutoMod = 0
            self.r1Mod = 0
            self.r2Mod = 0
            self.r3Mod = 0
            self.hipfireMod = 0
            self.reflexMod = 0

    def map(self):
        returnMe = {'name': self.name}
        returnMe['description'] = self.description
        returnMe['slot'] = self.slot
        returnMe['fullAutoMod'] = self.fullAutoMod
        returnMe['r1Mod'] = self.r1Mod
        returnMe['r2Mod'] = self.r2Mod
        returnMe['r3Mod'] = self.r3Mod
        returnMe['hipfireMod'] = self.hipfireMod
        returnMe['reflexMod'] = self.reflexMod
        return returnMe

    def __repr__(self):
        return str(self.map())



