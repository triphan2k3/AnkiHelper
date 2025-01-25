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
- your files will be save with the names as follow (at least hold true for cambridge):
  + vocabulary_us.mp3
  + vocabulary_uk.mp3
  + as a Linux user, I consider space being unacceptable, 
  so if the vocabulary is more than one word, 
  those words will be separated by _ (underscore character)
  + For ex: smoke_and_mirrors_us.mp3
  + "-" is also replaced by "_"
  + For ex: single_handed_us.mp3 instead of single-handed_us.mp3 
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
const curUrl = window.location.href; // get current url
if (curUrl.includes("cambridge")) {
    // case cambridge dictionary
    const srcElement = document.getElementsByTagName("source");
    let vocab = "";
    let title = document.title;
    for (let i = 0; title[i + 1] != "|"; i++) {
        if (isAlpha(title[i])) vocab = vocab + title[i].toLowerCase();
        else if (title[i] == " ") vocab = vocab + "_";
    }
    // console.log(vocab);
    for (let i = 0; i < srcElement.length; i++) {
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
    audioElements.forEach((el, key) => {
        srcMp3 = el.getAttribute("data-src-mp3");
        title = el.getAttribute("title");
        let type = "_uk";
        let dump = 22;
        if (title[title.length - 1] == "n") {
            dump++;
            type = "_us";
        }

        let fileName = "";
        // there are other 20 space :))
        // look stupid, i'll fix... in someday :))
        for (let i = 0; i < title.length - dump - 20; i++) {
            if (title[i] == " ") fileName = fileName + "_";
            else fileName = fileName + title[i];
        }
        fileName = fileName + type;

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
    let vocab = "";
    let title = document.title;
    for (let i = 0; title[i + 1] != "|"; i++) {
        if (isAlpha(title[i])) {
            if (isLowerCase(title[i])) break;
            vocab = vocab + title[i].toLowerCase();
        } else vocab = vocab + "_";
    }
    if (vocab[vocab.length - 1] == "_") vocab = vocab.slice(0, -1);

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
