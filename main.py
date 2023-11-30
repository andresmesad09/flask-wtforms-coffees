from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from pathlib import Path


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    url = URLField(label='Cafe location on Google Maps (URL)', validators=[DataRequired(), URL(message="enter a valid url")])
    open_time = StringField(label='open time e.g 8am', validators=[DataRequired()])
    close_time = StringField(label='closing time e.g 8pm', validators=[DataRequired()])
    coffee_rating = SelectField(label='coffe rating', validators=[DataRequired()], choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'])
    wifi_rating = SelectField(label='wifi rating', validators=[DataRequired()], choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    power_rating = SelectField(label='power socket availability', validators=[DataRequired()], choices=['🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')

cafe_file = Path().cwd() / "cafe-data.csv"

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = [
            form.cafe.data,
            form.url.data,
            form.open_time.data,
            form.close_time.data,
            form.coffee_rating.data,
            form.wifi_rating.data,
            form.power_rating.data
        ]
        with open(cafe_file, mode="a", encoding="utf-8") as file:
            file.write(f"{','.join(new_cafe)}\n")
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
