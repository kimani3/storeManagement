from flask import Flask, render_template, request, send_file
import database
import pandas as pd
import os

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login_check', methods=["GET", "POST"])
def login_check():
    username = request.form['username']
    password = request.form['pass']

    if username == "admin" and password == "admin":
        return render_template('home.html')
    else:

        return render_template('login.html', error="Please enter valid login credentials!")


@app.route('/theHome')
def home():
    # Heading for the data]
    try:
        os.remove('data.xlsx')

    except:
        pass
    headings = ('Product Name', 'Inventory', 'Edit Time', 'Edit Date')
    data = list(database.show_all_data())
    return render_template('home.html', headings=headings, data=data)



@app.route('/edit_inventory')
def edit():
    return render_template('edit.html')


@app.route('/edit_inventory_resp', methods=["GET", "POST"])
def edit_resp():
    name = request.form['name']
    inventory = request.form['inventory']
    database.update_inventory(name.capitalize(), inventory)
    if database.is_present(name.capitalize()):
        return render_template('edit.html')
    return render_template('edit.html', error="No such bag found!")


@app.route('/add_product')
def add_product():
    return render_template('add_bag.html')


@app.route('/add_bag_resp', methods=["GET", "POST"])
def add_product_resp():
    name = request.form['name']
    inventory = request.form['inventory']
    if database.is_present(name.capitalize()):
        return render_template('add_bag.html', error="Bag with similar name found!")
    else:
        database.insert_data(name.capitalize(), inventory)
        return render_template('add_bag.html')


@app.route('/edit_product_name')
def edit_name():
    return render_template('edit_name.html')


@app.route('/edit_product_name_resp',  methods=["GET", "POST"])
def edit_name_resp():
    name = request.form['name']
    new_name = request.form['new_name']

    if not database.is_present(name):
        return render_template('edit_name.html', error=f'[{name}] No such product found!')

    if database.is_present(new_name):
        return render_template('edit_name', error="Select a different name.")

    database.change_name(name, new_name)

    return render_template('home.html')


@app.route('/delete_product')
def delete_product():
    return render_template('delete.html')


@app.route('/delete_product_resp', methods=["GET", "POST"])
def delete_product_resp():
    name = request.form['name']
    if database.is_present(name.capitalize()):
        database.delete_product(name.capitalize())
        return render_template('home.html')
    else:
        return render_template('delete.html', error="No such product found!")


@app.route('/download_data')
def download_data():
    data = database.show_all_data()
    df = pd.DataFrame(data, columns=['Product Name', 'Inventory', 'Time', 'Date'])
    df = df.set_index('Product Name')
    # df.to_csv('data.csv')
    df.to_excel('data.xlsx')
    return send_file('data.xlsx', attachment_filename='data.xlsx', as_attachment=True)


if __name__ == "__main__":
    app.run()  # host="0.0.0.0", port=5000
