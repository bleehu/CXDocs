import feats_database
import pdb

class Feat:
    """A Character's feat."""

    def __init__(self, line):
        self.pk_id = int(line[0])
        self.name = line[1]
        self.title = line[1]
        prereqs = parse_prereq_list(line[2])
        self.prerequisites = prereqs
        self.description = line[3]
        self.author = line[4]
        self.created_at = line[5]
        self.private = line[6]
        self.nanite_cost = int(line[7])


def parse_prereq_list(prereq_string):
    if prereq_string == "[]":
        return []
    the_splits = prereq_string.split(',')
    prereqs = []
    for prereq in the_splits:
        trimmed = prereq.strip()
        prereqs.append(trimmed)
    return prereqs

