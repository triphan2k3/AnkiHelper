/* 
How to use:
- open a dictionary site in which the vocabulary is defined, such as:
  + https://dictionary.cambridge.org/vi/dictionary/english/humble
  + https://www.oxfordlearnersdictionaries.com/definition/english/charged
  + https://www.collinsdictionary.com/dictionary/english/scenic-beauty
- enter F12 to go to dev mode/dev tool
- Click on button Console
- pass all code to the console and enter
  + If it's your first time, you have to type "allow pasting" in advance
- your files will be save with the pattern as follow (at least hold true for cambridge):
  + vocabulary_us.mp3
  + vocabulary_uk.mp3
  + where vocabulary is the part of the link after the last slash ("/") with "-" replaced by "_"
*/

// helper functions
var isAlpha = function (ch) {
    return typeof ch === "string" && ch.length === 1 && /[A-Za-z]/.test(ch);
};

var isUpperCase = function (ch) {
    return typeof ch === "string" && ch.length === 1 && /[A-Z]/.test(ch);
};

var isLowerCase = function (ch) {
    return typeof ch === "string" && ch.length === 1 && /[a-z]/.test(ch);
};

// main code

// get current url, remove query string
const curUrl = window.location.href.split("#")[0].split("?")[0]; 
if (curUrl.includes("cambridge")) {
    // case cambridge dictionary
    const srcElement = document.getElementsByTagName("source");
    // prefix of filename
    let vocab = "CAMBRIDGE_" + curUrl.split("/").pop().replace(/-/g, "_");
    for (let i = 0; i < srcElement.length; i++) {
        // based on the observation that the first and third src elements is what we need
        if (i == 0 || i == 2) {
            const src = srcElement[i].getAttribute("src");
            const link = document.createElement("a");

            let type = src.includes("uk_pron") ? "_uk" : "_us"; // us or uk
            // if (src.includes("uk_pron")) type = "_uk";
            // else type = "_us";

            link.href = "https://dictionary.cambridge.org" + src;
            link.download = vocab + type + ".mp3";
            document.body.appendChild(link);
            link.click();
            // console.log("https://dictionary.cambridge.org" + src);
            document.body.removeChild(link);
        }
    }
} else if (curUrl.includes("oxford")) {
    // case oxford dictionary
    const audioElements = document.querySelectorAll(".sound.audio_play_button");
    // prefix of filename
    let vocab = "OXFORD_" + curUrl.split("/").pop().replace(/-/g, "_");

    // in this case, two first data-src-mp3 are what we need
    audioElements.forEach((el, key) => {
        srcMp3 = el.getAttribute("data-src-mp3");
        title = el.getAttribute("title");
        let type = "_uk";
        let dump = 22;
        if (title[title.length - 1] == "n") {
            dump++;
            type = "_us";
        }

        let fileName = vocab + type;

        if (key < 2) {
            const link = document.createElement("a");
            link.href = srcMp3;
            link.download = fileName + ".mp3";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    });
} else {
    // case collins dictionary
    let vocab = "COLLINS_" + curUrl.split("/").pop().replace(/-/g, "_");

    // console.log(vocab);
    const audioElements = document.querySelectorAll(
        ".hwd_sound.sound.audio_play_button"
    );
    let lang = "_uk";
    audioElements.forEach((el, key) => {
        if (key < 2) {
            fileName = vocab + lang;
            srcMp3 = el.getAttribute("data-src-mp3");
            const link = document.createElement("a");
            link.href = srcMp3;
            link.download = fileName + ".mp3";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            lang = "_us";
        }
    });
}
