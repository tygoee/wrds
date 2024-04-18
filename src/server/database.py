# WRDS: Learning words online
# Copyright (C) 2024  Tygo Everts
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from sqlite3 import connect, Cursor
from random import randint
from os import path, getcwd
from json import load
from typing import TypedDict

try:
    from constants import DATA_PUBLIC, INDEX_DB, LISTS_DB
except ImportError:
    from .constants import DATA_PUBLIC, INDEX_DB, LISTS_DB

if not getcwd().endswith('src'):
    raise OSError("Please cd to src/")


class MetaIndex(TypedDict):
    name: str
    owner: int
    subject: int
    lang1: str
    lang2: str


class Index(MetaIndex):
    id: int
    length: int


IndexT = tuple[int, int, str, int, int, str, str]


def table_exists(cursor: Cursor, table: int | str) -> bool:
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,)
    )

    return cursor.fetchone() is not None


def validate_list_id(list_id: int) -> None:
    if not type(list_id) is int or not len(str(list_id)) == 8:
        raise TypeError("list_id should be an int of 8 digits")


class index:
    def __init__(self, fp: str = INDEX_DB) -> None:
        self.connection = connect(fp)
        self.cursor = self.connection.cursor()

    def add(self, index: MetaIndex, list_id: int, length: int) -> None:
        if not table_exists(self.cursor, 'lists'):
            self.cursor.execute(' '.join("""
                CREATE TABLE lists (
                    id UNSIGNED INT PRIMARY KEY,
                    length UNSIGNED SMALLINT,
                    name TEXT,
                    owner UNSIGNED INT,
                    subject UNSIGNED TINYINT,
                    lang1 TEXT,
                    lang2 TEXT
                )
            """.split()))

        self.cursor.execute(
            f"INSERT INTO lists VALUES (?, ?, ?, ?, ?, ?, ?)",
            (list_id, length, index['name'], index['owner'],
             index['subject'], index['lang1'], index['lang2'])
        )

        self.connection.commit()

    def get(self, list_id: int) -> Index:
        validate_list_id(list_id)

        self.cursor.execute(
            f"SELECT * FROM lists WHERE id = ?",
            (list_id,)
        )

        fetched: IndexT = self.cursor.fetchone()
        return {
            'id': fetched[0],
            'length': fetched[1],
            'name': fetched[2],
            'owner': fetched[3],
            'subject': fetched[4],
            'lang1': fetched[5],
            'lang2': fetched[6]
        }

    def search(self, name: str) -> list[int]:
        self.cursor.execute(
            f"SELECT id FROM lists WHERE name = ?",
            (name,)
        )

        return [list_id[0] for list_id in self.cursor.fetchall()]


class lists:
    def __init__(self, fp: str = LISTS_DB) -> None:
        self.connection = connect(fp)
        self.cursor = self.connection.cursor()

    def add(self, data: dict[str, str]) -> int:
        while True:
            list_id = randint(10000000, 99999999)

            if not table_exists(self.cursor, list_id):
                break

        self.cursor.execute(' '.join(f"""
            CREATE TABLE '{list_id}' (
                id UNSIGNED SMALLINT PRIMARY KEY,
                lang1 TEXT,
                lang2 TEXT
            )
        """.split()))

        for word_id, (lang1, lang2) in enumerate(data.items(), 1):
            self.cursor.execute(
                f"INSERT INTO '{list_id}' (id, lang1, lang2) VALUES (?, ?, ?)",
                (word_id, lang1, lang2)
            )

        self.connection.commit()

        return list_id

    def get(self, list_id: int) -> dict[str, str]:
        validate_list_id(list_id)

        self.cursor.execute(f"SELECT lang1, lang2 FROM '{list_id}'")
        fetched: list[tuple[str, str]] = self.cursor.fetchall()

        return {pair[0]: pair[1] for pair in fetched}


if __name__ == "__main__":
    # Import json sample data in form {"lang1": "lang2"}
    for wordlist in ('3.2', '3.3', '3.4'):
        with open(
            path.join(DATA_PUBLIC, 'sample', f'{wordlist}.json'),
            'r', encoding='utf-8'
        ) as fp:
            data: dict[str, str] = load(fp)

            list_id = lists().add(data)
            index().add({
                'name': wordlist,
                'owner': 19823732,  # random
                'subject': 1,
                'lang1': 'en',
                'lang2': 'nl'
            },
                list_id, len(data)
            )
