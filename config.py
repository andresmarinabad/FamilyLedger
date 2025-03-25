import yaml


class Config:

    def __init__(self):
        with open("concepts.yml", "r", encoding="utf-8") as file:
            self.concepts = yaml.safe_load(file)['items']

        with open("translations.yml", "r", encoding="utf-8") as file:
            self.translations = yaml.safe_load(file)
            if self.translations is None:
                self.translations = {}

    def save_translations(self):
        with open('translations.yml', "w", encoding="utf-8") as file:
            yaml.dump(self.translations, file, default_flow_style=False, allow_unicode=True)


config = Config()
