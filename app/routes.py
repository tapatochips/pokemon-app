from flask import Flask, flash, redirect, render_template, request, url_for
from app import app
from .forms import PokemonForm
import requests
from flask_login import current_user
from .models import db, MyPokemon, Pokemon


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




@app.route('/my_pokemon', methods = ['GET', 'POST'])
def my_pokemon():
    # get the ID of the current user
    user_id = current_user.id

    # retrieve a list of caught pokemon for the current user
    caught_pokemon = db.session.query(MyPokemon).filter_by(user_id=user_id).all()

    # get details of each caught Pokemon
    pokemon_list = []
    for caught in caught_pokemon:
        pokemon = db.session.query(Pokemon).filter_by(id=caught.pokemon_id).first()
        pokemon_list.append(pokemon)

    # render the list of caught Pokemon in a template
    return render_template('my_pokemon.html', pokemon_list=pokemon_list)

#make button to catch and release and save/ delete respectively.






    







# if __name__ == '__main__':
#     app.run(debug=True)
