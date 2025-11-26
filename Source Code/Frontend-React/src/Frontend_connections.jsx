//Frontend_connections.jsx

//this is where the api will communicate with the frontend

//these were mostly copied from another project of mine so they should work but ill debug them more when everything is all set up
export async function fetchRecipes() {
  try {
    const content = await fetch(`http://localhost:5000/api/recipes`);
    if (!content.ok) throw new Error("Failed to fetch recipes");
    return await content.json();
  } catch (error_info) {
    console.error(error_info);
    return [];
  }
}


export async function addRecipe(recipe) {
  try {
    const content = await fetch(`http://localhost:5000/api/recipes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(recipe),
    });
    if (!content.ok) throw new Error("Failed to add recipe");
    return await content.json();
  } catch (error_info) {
    console.error(error_info);
    return null;
  }
}

export async function SearchRecipe(search) {
  try {
    const content = await fetch(`http://localhost:5000/api/recipes/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(search),
    });
    if (!content.ok) throw new Error("Failed to add recipe");
    return await content.json();
  } catch (error_info) {
    console.error(error_info);
    return null;
  }
}

export async function editRecipe(id, edit) {
  try {
    const content = await fetch(`http://localhost:5000/api/recipes/edit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(id, edit),
    });
    if (!content.ok) throw new Error("Failed to add recipe");
    return await content.json();
  } catch (error_info) {
    console.error(error_info);
    return null;
  }
}


export async function fetch_user_by_id(id) {
  try {
    const content = await fetch(`http://localhost:5000/api/users/${id}`);
    if (!content.ok) throw new Error("Failed to fetch user");
    return await content.json();
  } catch (error_info) {
    console.error(error_info);
    return [];
  }
}

export async function authenticate(userid, password) {
  try {
    const content = await fetch(`http://localhost:5000/api/users/authenticate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userid, password),
    });
    if (!content.ok) throw new Error("Failed to add recipe");
    return await content.json();
  } catch (error_info) {
    console.error(error_info);
    return null;
  }
}
