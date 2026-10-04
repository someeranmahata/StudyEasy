from flask import Flask, render_template, request, session, redirect, url_for
from pipeline import chain, config
from rich import print
import uuid
import secrets
app = Flask(__name__)

# Required for Flask session
app.secret_key = secrets.token_hex(32)


@app.route("/", methods=["GET", "POST"])
def home():

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":

        text = request.form.get("message", "").strip()

        pdf = request.files.get("pdf")
        pdf_name = ""

        if pdf and pdf.filename:
            pdf_name = pdf.filename

        if not text and not pdf_name:
            return redirect(url_for("home"))

        # -------------------------
        # Add USER message
        # -------------------------

        user_content = text

        if pdf_name:
            if user_content:
                user_content += f"\n\n📎 Attached: {pdf_name}"
            else:
                user_content = f"📎 Attached: {pdf_name}"

        history = session["history"]

        history.append({
            "role": "user",
            "content": user_content
        })

        # -------------------------
        # Call AI
        # -------------------------

        response = chain.invoke(
            {
                "topic": f"{text} {pdf_name}"
            },
            config
        )

        print(response)

        ai_message = response["messages"][-1].content

        # -------------------------
        # Add AI message
        # -------------------------

        history.append({
            "role": "assistant",
            "content": ai_message
        })

        # Save updated history
        session["history"] = history
        session.modified = True

        return redirect(url_for("home"))

    return render_template(
        "index.html",
        history=session.get("history", [])
    )


@app.route("/clear", methods=["POST"])
def clear_chat():

    session["history"] = []
    session.modified = True

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)