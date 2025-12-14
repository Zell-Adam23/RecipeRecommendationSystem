from Supabase_client import supabase_connection


def get_recipe_by_id(recipe_id):
    """get full recipe"""

    #fetch recipe
    recipe = (supabase_connection.table("RECIPE").select("*").eq("recipe_id", recipe_id).single().execute()).data
    if not recipe:
        return None

    #fetch metadata
    try:
        metadata = (supabase_connection.table("RECIPE_METADATA").select("*").eq("recipe_id", recipe_id).single().execute()).data
        recipe["metadata"] = metadata
    except:
        recipe["metadata"] = None

    #fetch cuisine
    cuisine_tags = (supabase_connection.table("RECIPE_CUISINE_TAG").select("cuisine_id").eq("recipe_id", recipe_id).execute()).data
    cuisine_ids = [x["cuisine_id"] for x in cuisine_tags]

    if cuisine_ids:
        cuisines = (supabase_connection.table("CUISINE_TAG").select("*").in_("cuisine_id", cuisine_ids).execute()).data
    else:
        cuisines = []
    
    recipe["cuisine_tags"] = cuisines

    #fetch diet
    diet_tags = (supabase_connection.table("RECIPE_DIET_TAG").select("diet_tag_id").eq("recipe_id", recipe_id).execute()).data
    diet_ids = [x["diet_tag_id"] for x in diet_tags]

    if diet_ids:
        diets = (supabase_connection.table("DIET_TAG").select("*").in_("diet_tag_id", diet_ids).execute()).data
    else:
        diets = []

    recipe["diet_tags"] = diets

    #fetch equipment
    equipment_tags = (supabase_connection.table("RECIPE_EQUIPMENT").select("equipment_id").eq("recipe_id", recipe_id).execute()).data
    equipment_ids = [x["equipment_id"] for x in equipment_tags]

    if equipment_ids:
        equipment = (supabase_connection.table("EQUIPMENT").select("*").in_("equipment_id", equipment_ids).execute()).data
    else:
        equipment = []

    recipe["equipment"] = equipment

    #fetch ingredients
    ingredient_tags = (supabase_connection.table("RECIPE_INGREDIENT").select("*").eq("recipe_id", recipe_id).execute()).data
    ingredient_ids = [x["ingredient_id"] for x in ingredient_tags]

    if ingredient_ids:
        ingredients = (supabase_connection.table("INGREDIENT").select("*").in_("ingredient_id", ingredient_ids).execute()).data
    else:
        ingredients = []

    ingredients_with_quantities = []
    for current in ingredient_tags:
        x = next((y for y in ingredients if y["ingredient_id"] == current["ingredient_id"]), None)
        ingredients_with_quantities.append({
            "ingredient_id": current["ingredient_id"],
            "name": x["name"],
            "quantity": current["quantity"],
            "unit": current["unit"],
            "optional": current["optional"]
        })

    recipe["ingredients"] = ingredients_with_quantities

    #fetch ratings
    ratings = (supabase_connection.table("RECIPE_RATING").select("*").eq("recipe_id", recipe_id).execute()).data

    recipe["ratings"] = ratings

    return recipe
