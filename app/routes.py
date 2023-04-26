from flask import Flask, flash, redirect, render_template, request, url_for, session
from app import app
from .forms import PokemonForm
import requests
from flask_login import current_user
from .models import db, Pokemon, User

#sets secret key
app.secret_key = 'my_secret_key'

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
    pokemon_data = session.get('pokemon_data', None)  # creates pokemon
    if request.method == 'POST':
        if form.validate():
            pokemon_name = form.pokemon_name.data.lower()
            print(pokemon_name)
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
            response = requests.get(url)
            data = response.json()
            if not response.ok:
                flash('That pokemon isnt in our database yet, try again in a few years', 'danger')
            else:
                pokemon_data = {
                    'name': data['name'],
                    'hp': data['stats'][0]['base_stat'],
                    'attack': data['stats'][2]['base_stat'],
                    'defense': data['stats'][1]['base_stat'],
                    'img_url': data['sprites']['front_shiny'],
                    'ability': data['abilities'][0]['ability']['name'],
                    'type': ", ".join([t['type']['name'] for t in data['types']]),
                    'id': data['id']
                }
                if not Pokemon.known_pokemon(pokemon_data['name']):
                    pokemon = Pokemon()
                    pokemon.from_dict(pokemon_data)
                    pokemon.saveToDB()

                session['pokemon_data'] = pokemon_data

    return render_template('pokemon_form.html', form=form, pokemon=pokemon_data)





@app.route('/my_pokemon', methods=['GET', 'POST'])
def my_pokemon():
    return render_template('my_pokemon.html', team=current_user.pokemon.all(), user = current_user)


@app.route('/catch_pokemon/<name>')
def catch_pokemon(name):
    pokemon=Pokemon.query.filter_by(name=name).first()
    if pokemon in current_user.pokemon:
        flash('You already have caught that pokemon.', 'warning')
        return redirect(url_for('my_pokemon'))
    elif current_user.pokemon.count() == 5:
        flash('Your team is full, if you want to catch a new pokemon, release one.', "danger")
        return redirect(url_for('my_pokemon'))
    else:
        flash('Added to your team.', "success")
        current_user.pokemon.append(pokemon)
        db.session.commit()
        return redirect(url_for('my_pokemon'))

        
@app.route('/battle/<id>')
def battle(id):
    """for pokemon battle

    Returns:
        result: this func is for simulating a battle between two Pokemon,
        then displaying the result for the user
    """
    op = User.query.filter_by(id = id).first()
    player1_pokemon = current_user.pokemon
    player2_pokemon = op.pokemon
    p1_total = 0
    p2_total = 0
    for pokemon in player1_pokemon:
        p1_total += pokemon.hp
        p1_total += pokemon.attack
        p1_total += pokemon.defense
    for pokemon in player2_pokemon:
        p2_total += pokemon.hp
        p2_total += pokemon.attack
        p2_total += pokemon.defense
    if p2_total > p1_total:
        flash(f'{op.username} won', 'success')
    elif p1_total > p2_total:
        flash(f'{current_user.username} won', 'success')
    return render_template('show_users.html')
        
    

        
    
    
@app.route('/show_users')
def show_users():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('show_users.html', users = users)


@app.route('/op_team/<id>')
def op_team(id):
    user = User.query.filter_by(id = id).first()

    return render_template('my_pokemon.html', team=user.pokemon.all(), user = user)

    
    




    

#"""    flask run --port 8000    """