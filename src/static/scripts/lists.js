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
function shuffle(words) {
  // The Fisher-Yates shuffle modified for an object
  let keys = Object.keys(words);
  let idx = keys.length;
  let random;

  // While there are still elements
  while (idx) {
    // Pick a random one
    random = Math.floor(Math.random() * idx--);

    // And swap it with the current one
    [keys[idx], keys[random]] = [keys[random], keys[idx]];
  }

  // Transform the array into an object
  let shuffled = {};
  keys.forEach((key) => {
    shuffled[key] = words[key];
  });

  return shuffled;
}

/** @param {[string, string]} words */
function* wordsTest(words) {
  // Base generator for a words test
  words = shuffle(words);

  // Yield the next word
  for (const word in words) {
    yield word;
  }
}

/** @param {string} word */
async function checkWord(word) {
  // TODO: Some more complex logic for non-exact matching
  // like disregarding brackets, allowing one side of slashes
  return input.value == word ? "right" : `wrong, it was ${word}`;
}

/** @param {IteratorResult<string, void>} result */
async function nextWord(result) {
  // Clear all fields
  correct.innerHTML = "";
  input.value = "";

  // Set the next question
  if (!result.done) {
    question.innerHTML = result.value;
    return result.value;
  }
}

/** @param {[string, string]} words */
async function setupTest(words) {
  let timeout = null;

  // Create the iterator and the first word
  let iterator = wordsTest(words);
  let word = await nextWord(iterator.next());

  form.addEventListener("submit", async function (event) {
    // Prevent the default submit action (GET request)
    event.preventDefault();

    // Check if the input is right and display that
    correct.innerHTML = await checkWord(words[word]);

    // Allow cancelling any timeout with another submit
    if (timeout !== null) {
      clearTimeout(timeout);
      word = await nextWord(iterator.next());
      timeout = null;
      return;
    }

    // Otherwise, set a timeout
    timeout = setTimeout(async () => {
      word = await nextWord(iterator.next());
      timeout = null;
    }, 1500);
  });
}

// Fetch the word list
fetch(`/api/lists/${list_id}/words`)
  .then((response) => response.json())
  .then((words) => setupTest(words));
