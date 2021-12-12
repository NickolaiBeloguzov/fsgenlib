import os
from fsgenlib.colored_output import Color
from fsgenlib.user import UserInteraction
import math
import csv

class DataUnit:
    def __init__(self, name: str, coefficient: float) -> None:
        self.name = name
        self.coef = coefficient
        self.people = 0
        self.share = 0

    def percentage(self, _from: int) -> None:
        p = (self.people / _from) * 100
        self.share = float("%.2f" % p)

    def format_for_csv(self) -> list:
        return [self.name, self.people, "{}%".format(self.share)]



class FSGenerator:
    def __init__(self, total_pool: int, parties: list[DataUnit]) -> None:
        self.parties = parties
        self.pool = total_pool
        self.parties_num = len(self.parties)

    def generate(self) -> list[DataUnit]:
        print(Color.cyan("[info]") + " Generating...")
        parties_portion = self.pool / self.parties_num


        computed_pool = 0
        for _, k in enumerate(self.parties):
            computed_local_pool = math.ceil(parties_portion * k.coef)
            k.people = computed_local_pool
            computed_pool += computed_local_pool
            print(Color.cyan("[info] ") + "Party '{}': {} people ({} * {})".format(k.name, computed_local_pool, int(parties_portion), k.coef))


        pool_diff = computed_pool - self.pool
        parties_pool_correction = math.ceil(pool_diff / self.parties_num)

        UserInteraction.print_warn("Correcting parties pools by {} people".format(abs(parties_pool_correction)))

        corrected_pool = 0

        for _, k in enumerate(self.parties):
            k.people = k.people - parties_pool_correction
            corrected_pool += k.people
        print(Color.cyan("[info] ") + "Total pool: {} people".format(corrected_pool))

        correction_delta = self.pool - corrected_pool
        if correction_delta > 0:
            self.parties.append(DataUnit("Unsure/Invalid", 1))
            self.parties[-1].people = correction_delta
        
        for _, k in enumerate(self.parties):
            k.percentage(corrected_pool)
            print(Color.cyan('[info] ') + "Party '{}': {}% from {} people".format(k.name, k.share, corrected_pool))

    def dump(self, path: str) -> None:
        file_exists = (os.path.exists(path) and os.path.isfile(path) and path.split('.')[-1] == "csv")
        if file_exists:
            UserInteraction.print_warn("File '{}' exists and will be overwritten".format(path))
        with open(path, 'w' if file_exists else 'x') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'No. of people', "Percentage"])
            for _, k in enumerate(self.parties):
                print(Color.cyan("[info] ") + "Writing party {} into a file".format(k.name))
                writer.writerow(k.format_for_csv())
            print(Color.green('[success] ') + "Done!")


def initialize() -> FSGenerator:
    pool = UserInteraction.ask("Total number of people", lambda x: True if x and int(x) > 0 else False, "People count is empty or less than 0", int)
    parties_num = UserInteraction.ask("Number of parties", lambda x: True if x and int(x) > 0 else False, "Number of parties is empty or less than 0", int)
    parties = []
    parties_names = []

    if pool % parties_num != 0:
        pool = pool + (parties_num - (pool % parties_num))
        UserInteraction.print_warn("Pool will be corrected to {}".format(pool))

    for i in range(parties_num):
        name = UserInteraction.ask("Party #{}'s name".format(i + 1), lambda x: True if x and x not in parties_names else False, "Partie's name is empty or is duplicate")
        parties_names.append(name)
        _r = input("Partie #{}'s coefficient (default: 1): ".format(i+1))
        if not _r or float(_r) <= 0.0:
            UserInteraction.print_warn("Invalid coefficient. Defaulting to 1")
        coef = (float(_r)) if _r or float(_r) >= 0.0 else 1
        parties.append(DataUnit(name, coef))


    return FSGenerator(pool, parties)
