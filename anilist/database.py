import csv
from tempfile import NamedTemporaryFile
import shutil
from typing import Dict
from anilist.tools import get_matching_title

from anilist.status import AniListType


# NOTE: currently a cvs file, but in the future it should use sqlight
class Database:
    ANILIST_CSV = (
        "/home/agsayan/Documents/Workspace/Github/WallabagAutomation/anilist.csv"
    )
    TEMP = "/tmp/anilist.csv"
    FIELDNAMES = ["Query", "Result", "ID", "TYPE"]

    # columns
    QUERY = "Query"
    ANILIST_TITLE = "Result"
    ANILIST_ID = "ID"
    ANILIST_TYP = "TYPE"
    # TODO: rename
    cvs_file = None

    def __init__(self, anilist_csv=""):
        if anilist_csv:
            self.ANILIST_CSV = anilist_csv

    # TEST: does this work
    def update_entry(self, search_query: str, result: str, id: int, typ: AniListType):
        tempfile = NamedTemporaryFile(mode="w", delete=False)
        with open(self.ANILIST_CSV, "r") as csvfile, tempfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", quotechar="|", fieldnames=self.FIELDNAMES
            )
            writer = csv.DictWriter(
                tempfile,
                delimiter=";",
                quotechar="|",
                fieldnames=self.FIELDNAMES,
                escapechar="\n",
            )

            for row in reader:
                if row[self.QUERY] == search_query:
                    print("updating row", row)
                    (
                        row[self.QUERY],
                        row[self.ANILIST_TITLE],
                        row[self.ANILIST_ID],
                        row[self.ANILIST_TYP],
                    ) = (search_query, result, id, typ.name)
                row = {
                    self.QUERY: row[self.QUERY],
                    self.ANILIST_TITLE: row[self.ANILIST_TITLE],
                    self.ANILIST_ID: row[self.ANILIST_ID],
                    self.ANILIST_TYP: row[self.ANILIST_TYP],
                }

                writer.writerow(row)
        shutil.move(tempfile.name, self.ANILIST_CSV)

    def save_media(self, search_query: str, media: Dict):
        titles = list(media["title"].values()) + media["synonyms"]
        title = get_matching_title(search_query, titles)
        media_type = AniListType(media["type"])
        id = media["id"]
        self.save(search_query, title, id, media_type)

    def save(self, search_query: str, result: str, id: int, typ: AniListType):
        assert isinstance(search_query, str)
        assert isinstance(result, str)
        assert isinstance(id, int)
        assert isinstance(typ, AniListType)

        title = self.get_title(search_query=search_query, type=typ)
        cvs_id = self.get_id(search_query=search_query, type=typ)

        if title and id > 0:
            return

        if title and cvs_id == -1 and id > 0:
            print(
                "Updating entry:\nsearch_query = {}\nresult = {}\ntyp = {}".format(
                    search_query, result, typ.value, typ.value
                )
            )
            self.update_entry(search_query, result, id, typ)
            return

        # skipping, there is already an entry of it
        if title and title == result:
            return

        with open(self.ANILIST_CSV, "a") as f:
            f.write("{};{};{};{}\n".format(search_query, result, id, typ.value)) # TEST: must work like the old one

    def get_title(self, search_query: str, type: AniListType) -> str:
        title = self.read_row(search_query, type, self.ANILIST_TITLE)
        return title

    def get_id(self, search_query: str, type: AniListType, filter_column=QUERY) -> int:
        id = self.read_row(
            search_query, type, self.ANILIST_ID, filter_column=filter_column
        )
        if id == "":
            return -1
        return int(id)


    def get_cvs_file(self):
        if self.cvs_file:
            return self.cvs_file
        with open(self.ANILIST_CSV, "r") as f:
            spamreader = csv.DictReader(
                f, delimiter=";", quotechar="|", fieldnames=self.FIELDNAMES
            )
            self.cvs_file = [row for row in spamreader]
        return self.cvs_file

    # FIX: TO SLOW
    def read_row(
        self, search_query: str, typ: AniListType, column: int, filter_column=QUERY
    ) -> str:
        search_query = search_query.lower()
        try:
            for row in self.get_cvs_file():
                query = row[filter_column].lower()
                anilist_title = row[self.ANILIST_TITLE].lower()
                anilist_type = AniListType[row[self.ANILIST_TYP].lower()]

                query = query.lower()
                anilist_title = anilist_title.lower()
                search_query_with_strokes = search_query.replace(" ", "-")
                if (
                    query == search_query
                    or anilist_title == search_query
                    or query == search_query_with_strokes
                ) and anilist_type == typ:
                    return row[column]

        except IOError:
            return ""

        return ""