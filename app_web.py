from flask import Flask, render_template, request
from groq import Groq
import os

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

messages = [
    {
        "role": "system",
        "content": """You are a friendly customer service assistant for Tasty Bites Restaurant.

Menu:
- Grilled Chicken - $12
- Beef Burger - $10
- Veggie Pizza - $9
- Pasta - $8
- Fish and Chips - $11

Special Offer:
- 20% off every Tuesday

Opening Hours:
- Monday to Sunday
- 10:00 AM - 11:00 PM

Reservations:
Call 0711111111.
"""
    }
]


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        user_input = request.form["message"]

        messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )

            reply = chat.choices[0].message.content

        except Exception as e:
            reply = f"Error: {e}"

        messages.append({
            "role": "assistant",
            "content": reply
        })

    return render_template(
        "index.html",
        messages=messages[1:]
    )


if __name__ == "__main__":
    app.run(debug=True)