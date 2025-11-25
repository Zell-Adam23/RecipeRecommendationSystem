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


export async function addPerson(recipe) {
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