from flask import Flask, request, render_template
import sys
import signal


# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function
@app.route("/", methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        product_name = request.form.get("pname")
        start_price = request.form.get("start")
        end_price = request.form.get("end")
        sorted = request.form.get("sorting")

        try:
            file_data = open("search.txt", "r")
            search_str = file_data.read().split(",")
            print(search_str)
        except FileNotFoundError:
            with open("search.txt", "w") as t:
                t.write(
                    product_name + "," + start_price + "," + end_price + "," + sorted
                )
            t.close()
        return "check tele"

    return render_template("form.html")


if __name__ == "__main__":
    app.run()
