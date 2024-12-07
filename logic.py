from random import randint
import requests

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)
        
        # Получаем данные из API
        data = self.fetch_data()
        if data:
            self.name = data.get('name', 'Unknown')
            self.img = data.get('sprites', {}).get('front_default', 'No Image')
            self.height = data.get('height', 0)
            self.weight = data.get('weight', 0)
            self.types = [t['type']['name'] for t in data.get('types', [])]
            self.abilities = [a['ability']['name'] for a in data.get('abilities', [])]
        else:
            self.name = "Pikachu"
            self.img = "No Image"
            self.height = 0
            self.weight = 0
            self.types = []
            self.abilities = []
        
        Pokemon.pokemons[pokemon_trainer] = self

    def fetch_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def info(self):
        types = ", ".join(self.types) if self.types else "Unknown"
        abilities = ", ".join(self.abilities) if self.abilities else "None"
        return (f"Имя: {self.name}\n"
                f"Рост: {self.height / 10} м\n"
                f"Вес: {self.weight / 10} кг\n"
                f"Типы: {types}\n"
                f"Способности: {abilities}")
    
    def show_img(self):
        return self.img

    # Методы для изменения свойств
    def set_name(self, new_name):
        self.name = new_name

    def set_height(self, new_height):
        self.height = new_height

    def set_weight(self, new_weight):
        self.weight = new_weight

    def add_ability(self, ability):
        if ability not in self.abilities:
            self.abilities.append(ability)

    def add_type(self, new_type):
        if new_type not in self.types:
            self.types.append(new_type)
