from flask import Flask, render_template, request, session
import random, pickle, operator, time

app = Flask(__name__)  # "dunder name".


@app.route("/")
@app.route("/displayform")
def display_form():
    tv = time.time()
    formatTime = time.ctime()
    session["timeStarted"] = tv
    randomWords = open("large_words.txt", "w")
    realWords = open("small_words.txt", "w")
    with open("words.txt") as words:
        for w in words:
            w2 = w.strip()
            len_w2 = len(w2)
            if len_w2 >= 7:
                print(w2, file=randomWords)

    with open("words.txt") as words:
        for w in words:
            w2 = w.strip()
            len_w2 = len(w2)
            if len_w2 >= 3:
                print(w2, file=realWords)
    realWords = [line.strip() for line in open("small_words.txt")]
    randomWords = [line.strip() for line in open("large_words.txt")]
    session["randomWord"] = random.choice(randomWords)
    return render_template(
        "form.html",
        the_title="Word Game!",
        random_Word=session["randomWord"],
        formatTime=formatTime,
    )


@app.route("/processform", methods=["POST"])
def process_form():
    inWords = []
    tv2 = time.time()
    session["TimeFinished"] = tv2  # store finished time
    # deduct start time from finish time
    finishTime = session["TimeFinished"] - session["timeStarted"]
    finishTime = str(finishTime)

    for x in request.form.values():
        inWords.append(x)
        session["inWords"] = inWords
        val = realWords(i=session["inWords"])

    if val != "":
        return render_template("thanks.html", the_title="Word Game", val=val)
    else:
        return render_template("won.html", the_title="Word Game", finishTime=finishTime)


def realWords(i):
    vw = i
    error = ""
    outputError = []
    count = 0
    words = 0
    x = 0
    l = 0
    # Are the words in the sourceword
    for wrd in vw:
        for w in wrd:
            if w in session["randomWord"]:
                count += 1
        if len(wrd) != count:
            outputError.append(wrd + " is not in the source word. <> ")
        count = 0

    # Is the word the source Word
    for wrd in vw:
        if wrd == session["randomWord"]:
            outputError.append("Source word cannot be used. <> ")

    # Was seven words entered.
    for wrd in vw:
        if wrd == "":
            outputError.append("Please enter seven words. <> ")

    # Are the words entered real words
    realWords = open("small_words.txt", "w")
    with open("words.txt") as words:
        for w in words:
            w2 = w.strip()
            len_w2 = len(w2)
            if len_w2 >= 3:
                print(w2, file=realWords)
    realWords = [line.strip() for line in open("small_words.txt")]
    for wrd in vw:
        if wrd not in realWords:
            outputError.append(wrd + " is not a real word. <> ")

    # Are there any duplicate words
    s = set()
    duplicates = set(x.lower() for x in vw if x.lower() in s or s.add(x))
    if len(s) != 7:
        outputError.append("No duplicate words allowed. ")

    error = "".join(outputError)
    return error


if __name__ == "__main__":
    app.config["SECRET_KEY"] = "YOUWILLNEVERGUESSMYSECRETKEY"
    app.run(debug=True)
