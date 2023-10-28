from typing import Optional

import yaml

from src.client import VJNInteraction
from src.domain.entity.Config import Config


def get_list_products(config: Config) -> str:
    res = "Liste des produits que vous pouvez supprimer:\n"
    for cat in config.categories:
        res += f"- `{cat.name}`\n"
        if cat.toppings:
            for topping in cat.toppings.options:
                res += f"  - `{topping.name}`\n"
            for topping in cat.toppings.recommandations:
                res += f"  - `{topping.name}`\n"
    return res


async def remove_product(interaction: VJNInteraction, product: Optional[str]):
    config: Config = interaction.client.config
    if product is None:
        res = get_list_products(config)
        await interaction.response.send_message(res, ephemeral=True)
        return

    product = product.lower()
    found = False
    for cat in config.categories:
        if cat.name.lower() == product:
            config.categories.remove(cat)
            found = True
            break
        if cat.toppings is None:
            continue
        for topping in cat.toppings.options:
            if topping.name.lower() == product:
                cat.toppings.options.remove(topping)
                found = True
                break
        for topping in cat.toppings.recommandations:
            if topping.name.lower() == product:
                cat.toppings.recommandations.remove(topping)
                found = True
                break
    # update config file
    if found:
        interaction.client.config = config
        with open("config.yaml", "w") as f:
            f.write(yaml.dump(config.model_dump()))
        await interaction.response.send_message(f"Le produit `{product}` a été supprimé", ephemeral=True)
    else:
        await interaction.response.send_message(f"Le produit `{product}` n'existe pas", ephemeral=True)



