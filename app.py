from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"


@app.route("/")
def show_index():
    """Shows the user the title of survey,
    instructions, and button to start survey"""

    session[RESPONSES_KEY] = []

    return render_template(
        "survey_start.html", 
        title=survey.title, 
        instructions=survey.instructions
    )


@app.route("/questions/<int:q_id>")
def show_question(q_id):
    """Shows a question in the survey
    for a given question id number."""

    if len(session[RESPONSES_KEY]) == 0 and q_id != 0:
        # No questions have been answered yet and user was browsing out of order
        return redirect("/questions/0")
    elif q_id == len(session[RESPONSES_KEY]):
        # This is a valid question to show as it is in order
        q = survey.questions[q_id]
        return render_template(
            "question.html", 
            q_id=q_id, 
            question=q.question, 
            choices=q.choices
        )
    elif len(session[RESPONSES_KEY]) == len(survey.questions):
        # check if the last question has been answered
        return redirect("/thankyou")
    else:
        next_q_id = len(session[RESPONSES_KEY])
        flash("Please answer questions in order!")
        return redirect(f"/questions/{next_q_id}")


@app.route("/answer/<int:q_id>", methods=["POST"])
def save_answer_and_redirect(q_id):
    """Saves the answer to RESPONSES_KEY list and redirects the user."""

    append_to_session(RESPONSES_KEY, request.form.get("answer"))

    if len(session[RESPONSES_KEY]) == len(survey.questions):
        return redirect("/thankyou")
    else:
        return redirect(f"/questions/{q_id + 1}")


@app.route("/thankyou")
def show_thanks():
    """Shows thank you page once user has
    completed all questions of survey"""

    return render_template("completion.html")


def append_to_session(key, value):
    """ Helper function for rebinding session for RESPONSES_KEY"""
    
    data_list = session[key]
    data_list.append(value)
    session[key] = data_list
