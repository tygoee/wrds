/*
 * WRDS: Learning words online
 * Copyright (C) 2024 Tygo Everts
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

let question = document.getElementById("question");
let input = document.getElementById("question-input");
let form = document.getElementById("question-form");
let correct = document.getElementById("correct");

/** @param {[string, string]} words */
function* wordsTest(words) {
  for (let word in words) {
    yield word;
  }
}

/** @param {string} word */
async function checkWord(word) {
  return input.value == word ? "right" : "wrong";
}

/** @param {IteratorResult<string, void>} result */
async function nextWord(result) {
  correct.innerHTML = "";
  input.value = "";

  if (!result.done) {
    question.innerHTML = result.value;
    return result.value;
  }
}

/** @param {[string, string]} words */
async function setupTest(words) {
  let timeout = null;

  let iterator = wordsTest(words);
  let word = await nextWord(iterator.next());

  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    correct.innerHTML = await checkWord(words[word]);

    if (timeout !== null) {
      clearTimeout(timeout);
      word = await nextWord(iterator.next());
      timeout = null;
      return;
    }

    timeout = setTimeout(async () => {
      word = await nextWord(iterator.next());
      timeout = null;
    }, 1500);
  });
}

fetch("/words")
  .then((response) => response.json())
  .then((words) => setupTest(words));
