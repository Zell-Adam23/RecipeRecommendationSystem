# search_recipes_by_pantry.py - Query to annotate recipes with pantry match info

from ..Supabase_client import get_supabase_client

supabase_connection = get_supabase_client()

def search_recipes_by_pantry(user_id):
    """Get all recipes with ingredient matching info based on user's pantry"""
    if not user_id:
        return []

    try:
        # 1. Get user's pantry ingredient names
        pantry_items = supabase_connection.table("USER_PANTRY_ITEM")\
            .select("ingredient_id")\
            .eq("user_id", user_id)\
            .execute()

        # Build pantry lookup map: ingredient_name -> True
        pantry_lookup = {}
        if pantry_items.data:
            for item in pantry_items.data:
                ingredient = supabase_connection.table("INGREDIENT")\
                    .select("name")\
                    .eq("ingredient_id", item["ingredient_id"])\
                    .single()\
                    .execute()
                if ingredient.data:
                    pantry_lookup[ingredient.data["name"].lower()] = ingredient.data["name"]

        # 2. Get all public recipes
        all_recipes = supabase_connection.table("RECIPE")\
            .select("recipe_id, title, short_description")\
            .eq("is_public", True)\
            .execute()

        if not all_recipes.data:
            return []

        # 3. For each recipe, get ingredients and annotate with pantry matches
        annotated_recipes = []

        for recipe in all_recipes.data:
            recipe_id = recipe["recipe_id"]

            # Get all ingredients for this recipe
            recipe_ingredients = supabase_connection.table("RECIPE_INGREDIENT")\
                .select("ingredient_id, quantity, unit, optional")\
                .eq("recipe_id", recipe_id)\
                .execute()

            # Annotate each ingredient with pantry match info
            ingredients_list = []
            required_count = 0
            matched_count = 0

            for rec_ing in recipe_ingredients.data:
                ingredient = supabase_connection.table("INGREDIENT")\
                    .select("name")\
                    .eq("ingredient_id", rec_ing["ingredient_id"])\
                    .single()\
                    .execute()

                if ingredient.data:
                    ing_name = ingredient.data["name"]
                    ing_name_lower = ing_name.lower()

                    # Check for exact match in pantry
                    pantry_match = pantry_lookup.get(ing_name_lower)

                    # Check for similar match (word-based)
                    similar_match = None
                    match_type = "none"

                    if pantry_match:
                        match_type = "exact"
                    else:
                        # Check if any pantry ingredient words match recipe ingredient words
                        recipe_words = set(ing_name_lower.split())
                        for pantry_ing_lower, pantry_ing_name in pantry_lookup.items():
                            pantry_words = set(pantry_ing_lower.split())

                            # If there's word overlap (e.g., "pork" in both "pork" and "ground pork")
                            if pantry_words.intersection(recipe_words):
                                similar_match = pantry_ing_name
                                match_type = "similar"
                                break

                    ingredients_list.append({
                        "name": ing_name,
                        "quantity": rec_ing["quantity"],
                        "unit": rec_ing["unit"],
                        "optional": rec_ing["optional"],
                        "in_pantry": pantry_match is not None,
                        "pantry_name": pantry_match if pantry_match else similar_match,
                        "match_type": match_type
                    })

                    if not rec_ing["optional"]:
                        required_count += 1
                        if pantry_match:
                            matched_count += 1

            # Calculate match percentage for required ingredients
            match_percentage = (matched_count / required_count * 100) if required_count > 0 else 100

            annotated_recipes.append({
                "recipe_id": recipe["recipe_id"],
                "title": recipe["title"],
                "short_description": recipe["short_description"],
                "ingredients": ingredients_list,
                "required_ingredients_count": required_count,
                "matched_ingredients_count": matched_count,
                "match_percentage": round(match_percentage, 1)
            })

        # Sort by match percentage (highest first)
        annotated_recipes.sort(key=lambda x: x["match_percentage"], reverse=True)

        return annotated_recipes

    except Exception as e:
        print(f"Error searching recipes by pantry: {e}")
        return []
