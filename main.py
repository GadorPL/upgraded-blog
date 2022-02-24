from flask import Flask, render_template, request
import requests
import smtplib
import os

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

all_posts = requests.get("https://api.npoint.io/810908ef58fd7ee20b48").json()
print(all_posts)

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", posts=all_posts)


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in all_posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route('/about')
def get_about():
    return render_template("about.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject:New msg form blog reader!\n\nName: {name}\n"
                    f"Email: {email}\nPhone: {phone}\nMessage: {message}".encode()
            )
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
