from flask import Flask, redirect, render_template, request, url_for
from app import app
from .forms import PokemonForm
import requests
from .forms import LoginForm, SignUpForm
from .models import User
from flask_login import login_user


'''
need to make forms in forms.py, need to add routes in routes.py

'''


@app.route('/', methods=['GET'])
def home():
    return render_template('base.html')


@app.route('/search', methods=['POST', 'GET'])
def pokemon_form():
    """code for pokemon card info

    Returns:
        card: this func is for getting the pokemon info from the pokemon api
        and then displaying it in the card for the user
    """
    form = PokemonForm()
    if request.method == 'POST':
        if form.validate():
            pokemon_name = form.pokemon_name.data.lower()
            print(pokemon_name)
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                pokemon_data = {
                    'name': data['name'],
                    'hp': data['stats'][0]['base_stat'],
                    'defense': data['stats'][1]['base_stat'],
                    'attack': data['stats'][2]['base_stat'],
                    'image': data['sprites']['front_shiny'],
                    'ability': data['abilities'][0]['ability']['name']
                }
                return render_template('pokemon_form.html', pokemon=pokemon_data, form=form)
        else:
            return ('Pokemon not found!')
        return render_template('pokemon_form.html', pokemon=pokemon_data, form=form)
    return render_template('pokemon_form.html', form=form)


@app.route('/signup', methods = ["GET", "POST"])
def signuppage():
    form = SignUpForm()
    
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            
            user = User(email, username, password)
            
            user.save_to_db()
            account = {
                'email': email,
                'username': username
            }
        return render_template('signup.html', form = form, account = account)
    return render_template('signup.html', form = form)


@app.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            print('im here')
            username = form.username.data
            password = form.password.data
            
            user = User.query.filter_by(username=username).first()
            print(user)
            if user:
                print(user)
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    print('invalid username or password')
            else:
                print('Invalid username or password')
                
    return render_template('login.html', form = form)


    







# if __name__ == '__main__':
#     app.run(debug=True)
