from flask import Flask, render_template, request
from app import app
from .forms import PokemonForm


@app.route('/', methods=['GET'])
def home():
    return render_template('base.html')

@app.route('/search', methods=['GET', 'POST'])
def pokemon_form():
    form = PokemonForm()
    if request.method == 'POST':
        if form.validate():
            pokemon_name = form.pokemon_name.data
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
            response = request.get(url)
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
                return render_template('pokemon_form.html', pokemon=pokemon_data, form = form)
            else:
                return('Pokemon not found!')
        return render_template('pokemon_form.html', form = form)
    return render_template('pokemon_form.html', form = form)


# if __name__ == '__main__':
#     app.run(debug=True)
