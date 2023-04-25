from flask import Flask, flash, redirect, render_template, request, url_for, session
from app import app
from .forms import PokemonForm
import requests
from flask_login import current_user
from .models import db, Pokemon

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
    pokemon = session.get('pokemon_data', None)  #creates pokemon
    if request.method == 'POST':
        if form.validate():
            pokemon_name = form.pokemon_name.data.lower()
            print(pokemon_name)
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
            response = requests.get(url)
            data = response.json()
            if not response.ok:
                flash('That pokemon isnt in our database yet, try again in a few years', 'danger')
            for pokemon in data:
                pokemon_data = {}
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
                    pokemon=Pokemon()
                    pokemon.from_dict(pokemon_data)
                    pokemon.saveToDB()
                    
            
        
        return render_template('pokemon_form.html', form=form, pokemon=pokemon_data)

    return render_template('pokemon_form.html', form=form)



@app.route('/my_pokemon', methods=['GET', 'POST'])
def my_pokemon():
    return render_template('my_pokemon.html', team=current_user.pokemon.all())


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


@app.route('/battle', methods=['GET', 'POST'])
def battle():
    """for pokemon battle

    Returns:
        result: this func is for simulating a battle between two Pokemon,
        then displaying the result for the user
    """
    player1_pokemon = session.get('player1_pokemon', None)
    player2_pokemon = session.get('player2_pokemon', None)

    if player1_pokemon and player2_pokemon:
        player1_hp = player1_pokemon.hp
        player2_hp = player2_pokemon.hp

        #does math
        while player1_hp > 0 and player2_hp > 0:
            player2_hp -= player1_pokemon.attack
            if player2_hp <= 0:
                break
            player1_hp -= player2_pokemon.attack

        #determines the winner based on who has more HP
        if player1_hp > player2_hp:
            winner = player1_pokemon.name
        elif player2_hp > player1_hp:
            winner = player2_pokemon.name
        else:
            winner = "It's a tie!"

        return render_template('battle.html', winner=winner)
    else:
        return redirect(url_for('pokemon_form'))



    

#"""    flask run --port 8000    """