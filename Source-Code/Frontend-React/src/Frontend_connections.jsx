//Frontend_connections.jsx

//this is where the api will communicate with the frontend


//TODO: Sort into Command vs Query later


const API_URL = import.meta.env.VITE_API_URL;

export async function fetchRecipes() {
  try {
    const response = await fetch(`${API_URL}/api/recipes`);
    if (!response.ok) throw new Error("Failed to fetch recipes");
    return await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
    return [];
  }
}


export async function addRecipe(recipe) {
  try {
    const response = await fetch(`${API_URL}/api/recipes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(recipe),
    });
    if (!response.ok) throw new Error("Failed to add recipe");
    return await response.json();
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function fetchRecipeById(id) {
  try {
    const response = await fetch(`${API_URL}/api/recipes/${id}`);
    if (!response.ok) throw new Error("Failed to fetch recipe");
    return await response.json();
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function SearchRecipe(search) {
  try {
    const content = await fetch(`${API_URL}/api/recipes/search`, {
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
    const content = await fetch(`${API_URL}/api/recipes/edit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({recipe_id: id, ...edit}),
    });
    if (!content.ok) throw new Error("Failed to add recipe");
    return await content.json();
  } catch (error_info) {
    console.error(error_info);
    return null;
  }
}

export async function saveRecipe(userId, recipeId) {
  try {
    const response = await fetch(`${API_URL}/api/saved-recipes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, recipe_id: recipeId }),
    });
    if (!response.ok) throw new Error("Failed to save recipe");
    return await response.json();
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function unsaveRecipe(userId, recipeId) {
  try {
    const response = await fetch(`${API_URL}/api/saved-recipes`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, recipe_id: recipeId }),
    });
    if (!response.ok) throw new Error("Failed to unsave recipe");
    return await response.json();
  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function getSavedRecipes(userId) {
  try {
    const response = await fetch(`${API_URL}/api/saved-recipes/${userId}`);
    if (!response.ok) throw new Error("Failed to fetch saved recipes");
    return await response.json();
  } catch (error) {
    console.error(error);
    return [];
  }
}


export async function fetch_user_by_id(id) {
  try {
    const content = await fetch(`${API_URL}/api/users/${id}`);
    if (!content.ok) throw new Error("Failed to fetch user");
    return await content.json();
  } catch (error_info) {
    console.error(error_info);
    return [];
  }
}



export async function loginUser(email, password) {
  try {
    const response = await fetch(`${API_URL}/api/users/authenticate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password_hash: password }),
    });
    if (!response.ok) throw new Error("Invalid credentials");
    return await response.json();
  } catch (error) {
    console.error('Login error:', error);
    return null;
  }
}


export async function registerUser(userData) {
  try {
    const response = await fetch(`${API_URL}/api/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });
    if (!response.ok) throw new Error("Registration failed");
    return await response.json();
  } catch (error) {
    console.error('Registration error:', error);
    return null;
  }
}