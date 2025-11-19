from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# --- HTML + CSS + JS (Everything in one file for Docker) ---
GAME_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>Guess The Number Game</title>
    <style>
        body {
            font-family: 'Arial';
            background: linear-gradient(to right, #2c5364, #203a43, #0f2027);
            color: white;
            text-align: center;
            padding-top: 50px;
        }
        h1 {
            font-size: 40px;
            margin-bottom: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            width: 400px;
            padding: 30px;
            margin: auto;
            border-radius: 20px;
            box-shadow: 0 0 20px rgba(255,255,255,0.2);
        }
        input {
            padding: 10px;
            width: 60%;
            border-radius: 10px;
            border: none;
            margin-bottom: 20px;
            font-size: 18px;
        }
        button {
            padding: 10px 20px;
            background: #00c6ff;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            cursor: pointer;
        }
        button:hover {
            background: #0072ff;
        }
        .msg {
            margin-top: 20px;
            font-size: 22px;
            font-weight: bold;
        }
    </style>

    <script>
        async function checkGuess() {
            let guess = document.getElementById("guess").value;

            let response = await fetch("/check", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ guess: guess })
            });

            let data = await response.json();
            document.getElementById("message").innerText = data.message;
        }
    </script>
</head>
<body>
    <h1>🎮 Guess The Number (1–20)</h1>

    <div class="container">
        <p>Try to guess the hidden number!</p>
        <input id="guess" type="number" placeholder="Enter your guess">
        <br>
        <button onclick="checkGuess()">Submit</button>

        <div class="msg" id="message"></div>
    </div>

</body>
</html>
"""

# Game number stored globally
secret_number = random.randint(1, 20)


@app.route("/")
def game_page():
    return render_template_string(GAME_UI)


@app.route("/check", methods=["POST"])
def check():
    global secret_number
    guess = int(request.json["guess"])
    
    if guess == secret_number:
        secret_number = random.randint(1, 20)
        return jsonify({"message": "🎉 Correct! New number generated!"})
    elif guess < secret_number:
        return jsonify({"message": "⬆️ Too Low!"})
    else:
        return jsonify({"message": "⬇️ Too High!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
