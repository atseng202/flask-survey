from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

# Will replace with session
responses = []


@app.route("/")
def show_index():
    """Shows the user the title of survey,
    instructions, and button to start survey"""

    session["responses"] = []
    session["answered"] = []

    return render_template(
        "survey_start.html", title=survey.title,
        instructions=survey.instructions)


@app.route("/questions/<int:q_id>")
def show_question(q_id):
    """Shows a question in the survery
    for a given question id number."""

    if len(session["answered"]) == 0 and q_id != 0:
        q_id = 0
        return redirect("/questions/0")

    if ((q_id - 1 in session["answered"] and q_id not in session["answered"])
            or (q_id == 0 and 0 not in session["answered"])):
        q = survey.questions[q_id]
        return render_template(
            "question.html", q_id=q_id, question=q.question, choices=q.choices
        )
    else:
        # check if the last question has been answered
        last_answered_id = session["answered"][-1]
        final_question_id = len(survey.questions)-1
        if final_question_id in session["answered"]:
            return redirect("/thankyou")
        else:
            next_q_id = last_answered_id + 1
            q = survey.questions[next_q_id]
            flash("Please answer questions in order!")
            return redirect(f"/questions/{next_q_id}")


@app.route("/answer/<int:q_id>", methods=["POST"])
def save_answer_and_redirect(q_id):
    """Saves the answer to the answer to responses list
    and redirects the user."""

    save_to_session("answered", q_id)
    save_to_session("responses", request.form.get("answer"))

    redirect_id = q_id + 1
    if redirect_id >= len(survey.questions):
        return redirect("/thankyou")
    else:
        return redirect(f"/questions/{redirect_id}")


@app.route("/thankyou")
def show_thanks():
    return render_template("completion.html")


def save_to_session(key, value):
    """ Helper function for rebinding session responses """
    data_list = session[key]
    data_list.append(value)
    session[key] = data_list
