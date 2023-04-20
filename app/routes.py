from flask import Flask, flash, redirect, render_template, request, url_for, session
from app import app
from .forms import PokemonForm
import requests
from flask_login import current_user
from .models import db, MyPokemon, Pokemon

# Set the secret key for session management
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
    pokemon = session.get('pokemon_data', None)  #creates pokemon
    if request.method == 'POST':
        if form.validate():
            pokemon_name = form.pokemon_name.data.lower()
            print(pokemon_name)
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                pokemon_data = {
                    # 'stats': data['stats'],
                    'name': data['name'],
                    'hp': data['stats'][0]['base_stat'],
                    'attack': data['stats'][2]['base_stat'],
                    'defense': data['stats'][1]['base_stat'],
                    'image': data['sprites']['front_shiny'],
                    'ability': data['abilities'][0]['ability']['name'],
                    'types': ", ".join([t['type']['name'] for t in data['types']]),
                }
                session['pokemon_data'] = pokemon_data
                pokemon = pokemon_data  #updates pokemon
                if 'catch' in request.form:
                    return redirect(url_for('my_pokemon'))  #redirects if user clicked on catch
            else:
                flash('Pokemon not found!')

    return render_template('pokemon_form.html', form=form, pokemon=pokemon)



@app.route('/my_pokemon', methods=['GET', 'POST'])
def my_pokemon():
    user_id = current_user.id

    #gets caught pokemon details
    caught_pokemon = db.session.query(MyPokemon).filter_by(user_id=user_id).all()

    #gets newly caught pokemon details
    pokemon_data = session.get('pokemon_data')
    if pokemon_data:
        try:
            pokemon = Pokemon(
                # stats=pokemon_data['stats'],
                name=pokemon_data['name'],
                hp=pokemon_data['stats'][0]['base_stat'],
                attack=pokemon_data['stats'][1]['base_stat'],
                defense=pokemon_data['stats'][2]['base_stat'],
                image=pokemon_data['sprites']['front_shiny'],
                ability=pokemon_data['abilities'][0]['ability']['name'],
                types=", ".join([t['type']['name'] for t in pokemon_data['types']])
            )
        except KeyError as e:
            flash(f"Error: Missing key '{e.args[0]}' in pokemon_data dictionary.")
            return redirect(url_for('pokemon_form'))

        db.session.add(pokemon)
        db.session.commit()
        session.pop('pokemon_data', None)
        caught_pokemon.append(pokemon)
    else:
        pokemon = None

    return render_template('my_pokemon.html', pokemon_list=caught_pokemon, pokemon=pokemon)


@app.route('/catch_pokemon', methods=['GET'])
def catch_pokemon():
    pokemon_data = session.get('pokemon_data')
    if pokemon_data:
        flash('You have already caught a pokemon!')
        return redirect(url_for('my_pokemon'))
    else:
        #gets newly caught pokemon from request
        pokemon_name = request.args.get('pokemon_name', None)
        if pokemon_name:
            #ask api for pokemon data
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                pokemon_data = {
                    # 'stats': data['stats'],
                    'name': data['name'],
                    'hp': data['stats'][0]['base_stat'],
                    'attack': data['stats'][2]['base_stat'],
                    'defense': data['stats'][1]['base_stat'],
                    'image': data['sprites']['front_shiny'],
                    'ability': data['abilities'][0]['ability']['name'],
                    'types': ", ".join([t['type']['name'] for t in data['types']])
                }
                session['pokemon_data'] = pokemon_data
                return redirect(url_for('my_pokemon', pokemon_data=pokemon_data))
            else:
                flash('Pokemon not found!')
        else:
            flash('No pokemon data found!')
        return redirect(url_for('pokemon_form'))

