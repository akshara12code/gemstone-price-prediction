from flask import Flask, render_template, jsonify, request, redirect, flash
from src.pipeline.prediction_pipeline import PredictionPipeline, CustomData
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static",
    template_folder="templates"
)

# Secret key needed for flash messages
app.secret_key = 'your_secret_key_here'

# ------------------ Home Page ------------------
@app.route('/')
def home_page():
    return render_template("index.html")


# ------------------ Prediction Route ------------------
@app.route("/predict", methods=["POST"])
def predict_datapoint():
    try:
        data = CustomData(
            carat=float(request.form.get("carat")),
            depth=float(request.form.get("depth")),
            table=float(request.form.get("table")),
            x=float(request.form.get("x")),
            y=float(request.form.get("y")),
            z=float(request.form.get("z")),
            cut=request.form.get("cut"),
            color=request.form.get("color"),
            clarity=request.form.get("clarity")    
        )
        final_data = data.get_data_as_dataframe()
        predict_pipeline = PredictionPipeline()
        pred = predict_pipeline.predict(final_data)
        result = round(pred[0], 2)
        return render_template("result.html", final_result=result)
    except Exception as e:
        print("Prediction error:", e)
        flash("Failed to make prediction.", "error")
        return redirect('/')


# ------------------ Contact Form Route ------------------
@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Email configuration
        sender_email = "your_email@gmail.com"
        sender_password = "your_app_password_here"  # Gmail App Password
        receiver_email = "akshara12082005@gmail.com"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"Contact Form Message from {name}"

        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        # Sending the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        flash("Message sent successfully!", "success")
    except Exception as e:
        print("Email sending error:", e)
        flash("Failed to send message.", "error")

    return redirect('/#contact')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
