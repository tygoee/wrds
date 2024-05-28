/*
 * WRDS: Learning words online
 * Copyright (C) 2024 Tygo Everts
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

/** @param {object} list */
async function makeListItem(list) {
  const a = document.createElement("a");
  console.log(list);
  a.href = `/lists/${list.id}/test`;
  a.textContent = list.name;

  // Create an li with the href
  const li = document.createElement("li");
  li.appendChild(a);

  // Add the li to the list
  return li;
}

/** @param {int[]} lists */
async function displayList(lists) {
  const ul = document.getElementById("lists");
  for (let list of lists) {
    const response = await fetch(`/api/lists/${list}/meta`);
    const listJson = await response.json();

    ul.appendChild(await makeListItem(listJson));
  }
}

// Fetch the lists
fetch(`/api/lists`)
  .then((response) => response.json())
  .then((lists) => displayList(lists));
