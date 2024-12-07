from random import randint
import requests

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = self.random_pokemon_number()
        self.level = 1
        self.experience = 0
        self.hunger = 50  # Начальный уровень сытости (0–100)
        self.is_rare = False
        
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

    def random_pokemon_number(self):
        # С шансом 5% генерируем редкого покемона
        self.is_rare = randint(1, 100) <= 5
        return randint(1, 1000)

    def fetch_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def info(self):
        rarity = "Редкий" if self.is_rare else "Обычный"
        types = ", ".join(self.types) if self.types else "Unknown"
        abilities = ", ".join(self.abilities) if self.abilities else "None"
        return (f"Имя: {self.name}\n"
                f"Редкость: {rarity}\n"
                f"Уровень: {self.level}\n"
                f"Опыт: {self.experience}\n"
                f"Сытость: {self.hunger}\n"
                f"Рост: {self.height / 10} м\n"
                f"Вес: {self.weight / 10} кг\n"
                f"Типы: {types}\n"
                f"Способности: {abilities}")

    def show_img(self):
        return self.img

    # Методы для взаимодействия
    def feed(self):
        if self.hunger < 100:
            self.hunger = min(self.hunger + 20, 100)
            return "Покемон накормлен! Сытость увеличилась."
        return "Покемон уже сыт!"

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        return f"Поздравляем! {self.name} достиг уровня {self.level}!"

    def check_hunger(self):
        if self.hunger > 0:
            self.hunger -= 5  # Уменьшаем сытость со временем
        else:
            return f"{self.name} голоден! Скоро он перестанет расти."

    def add_achievement(self):
        return f"Поздравляем! Вы получили достижение за владение редким покемоном: {self.name}!"


