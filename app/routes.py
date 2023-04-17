from flask import Flask, flash, redirect, render_template, request, url_for
from app import app
from .forms import PokemonForm
import requests
from .forms import LoginForm, SignUpForm, EditProfileForm
from .models import User
from flask_login import current_user, login_user, logout_user, login_required
import os
from .models import db



'''
need to add profile page and edit profile page

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
                    'ability': data['abilities'][0]['ability']['name'],
                    'types': ", ".join([t['type']['name'] for t in data['types']])

                }
                return render_template('pokemon_form.html', pokemon=pokemon_data, form=form)
        else:
             flash('Pokemon not found!')
        return render_template('pokemon_form.html', form=form)
    return render_template('pokemon_form.html', form=form)

#signup
@app.route('/signup', methods = ["GET", "POST"])
def signuppage():
    form = SignUpForm()
    
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            bio = form.bio.data
            img_url = form.img_url.data
            user = User(email, username, password, bio, img_url)
            
            user.save_to_db()
            account = {
                'email': email,
                'username': username
            }
        return redirect(url_for('login'))
    return render_template('signup.html', form = form)

#auth
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

#auth
@app.route('/logout')
def logMeOut():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user')
@login_required
def user():
    
    return render_template('user.html', user=current_user)


#auth
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == "POST" and form.validate_on_submit():
        print('here')
        edited_user_data = {
        'email':form.email.data,
        'username':form.username.data,
        'password':form.password.data,
        'bio':form.bio.data,
        'img_url':form.img_url.data
        }
        user = User.query.filter_by(email = edited_user_data['email']).first()
        if user and user.email != current_user.email:
            flash('email is already in use', "danger")
            return redirect(url_for('edit_profile'))
        try:
            current_user.from_dict(edited_user_data)
            current_user.save_to_db()
            flash('profile updated', "success")
               
        except:
            flash('error updating profile', 'danger')
            return redirect(url_for('edit_profile'))
        return redirect(url_for('user'))
    return render_template('edit_profile.html', form = form)



    







# if __name__ == '__main__':
#     app.run(debug=True)
