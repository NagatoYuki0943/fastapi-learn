from ruamel.yaml import YAML

yaml = YAML(typ="safe")

with open("app/envs.yaml", "r") as file:
    ENVS: dict = yaml.load(file)

print(ENVS)
