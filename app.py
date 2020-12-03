from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def show_index():
    """Shows the user the title of survey,
    instructions, and button to start survey"""

    return render_template(
        "survey_start.html",
        title=survey.title,
        instructions=survey.instructions
    )


@app.route("/questions/<q_id>")
def show_question(q_id):
    """Shows a question in the survery
    for a given question id number. """
    q = survey.questions[int(q_id)]
    return render_template("question.html",
                           q_id=q_id,
                           question=q.question,
                           choices=q.choices)


@app.route("/answer/<q_id>", methods=["POST"])
def save_answer_and_redirect(q_id):
    """ Saves the answer to the answer to responses list
    and redirects the user. """

    redirect_id = int(q_id) + 1
    if redirect_id >= len(survey.questions):
        return redirect("/thankyou")
    else:
        responses.append(request.form.get("answer"))
        return redirect(f"/questions/{redirect_id}")


@app.route("/thankyou")
def show_thanks():
    return render_template("completion.html")
