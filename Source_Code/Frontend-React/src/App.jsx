//App.jsx - the main frontend file

import { useState, useEffect } from 'react';
import { fetchRecipes, addRecipe, loginUser, registerUser, fetchRecipeById, saveRecipe, unsaveRecipe, getSavedRecipes } from './Frontend_connections';


// ============================================
// LOGIN/SIGNUP COMPONENT
// ============================================

function AuthPage({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    display_name: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setError('');
    setLoading(true);

    if (isLogin) {
      // LOGIN
      const result = await loginUser(formData.email, formData.password);
      if (result && result.user_id) {
        onLogin(result);
      } else {
        setError('Invalid email or password');
      }
    } else {
      // SIGNUP
      if (!formData.display_name || !formData.email || !formData.password) {
        setError('Please fill in all required fields');
        setLoading(false);
        return;
      }
      
      const userData = {
        display_name: formData.display_name,
        email: formData.email,
        password_hash: formData.password
      };
      
      const result = await registerUser(userData);
      if (result && result.user_id) {
        onLogin(result);
      } else {
        setError('Registration failed. Email might already exist.');
      }
    }
    
    setLoading(false);
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #f0f9e8 0%, #fffbea 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div style={{
        background: '#ffffff',
        borderRadius: '16px',
        padding: '40px',
        maxWidth: '420px',
        width: '100%',
        boxShadow: '0 8px 32px rgba(76, 175, 80, 0.15)',
        border: '1px solid rgba(76, 175, 80, 0.1)'
      }}>
        <h1 style={{ 
          color: '#2d5016', 
          marginTop: 0, 
          textAlign: 'center',
          fontSize: '28px',
          fontWeight: '600',
          marginBottom: '8px'
        }}>
          Recipe Recommender
        </h1>
        <p style={{
          textAlign: 'center',
          color: '#7cb342',
          fontSize: '14px',
          marginTop: 0,
          marginBottom: '30px'
        }}>
          Discover and save your favorite recipes
        </p>
        
        <div style={{ 
          display: 'flex', 
          gap: '10px', 
          marginBottom: '30px',
          borderBottom: '2px solid #e8f5e9'
        }}>
          <button
            onClick={() => setIsLogin(true)}
            style={{
              flex: 1,
              padding: '12px',
              background: 'none',
              border: 'none',
              borderBottom: isLogin ? '3px solid #4caf50' : 'none',
              color: isLogin ? '#2d5016' : '#9e9e9e',
              fontWeight: '600',
              cursor: 'pointer',
              fontSize: '16px',
              transition: 'all 0.3s'
            }}
          >
            Login
          </button>
          <button
            onClick={() => setIsLogin(false)}
            style={{
              flex: 1,
              padding: '12px',
              background: 'none',
              border: 'none',
              borderBottom: !isLogin ? '3px solid #4caf50' : 'none',
              color: !isLogin ? '#2d5016' : '#9e9e9e',
              fontWeight: '600',
              cursor: 'pointer',
              fontSize: '16px',
              transition: 'all 0.3s'
            }}
          >
            Sign Up
          </button>
        </div>

        {error && (
          <div style={{
            padding: '12px',
            background: '#ffebee',
            border: '1px solid #ef5350',
            borderRadius: '8px',
            color: '#c62828',
            marginBottom: '20px',
            fontSize: '14px'
          }}>
            {error}
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          {!isLogin && (
            <input
              type="text"
              placeholder="Display Name"
              value={formData.display_name}
              onChange={(e) => setFormData({...formData, display_name: e.target.value})}
              style={{
                padding: '14px',
                border: '2px solid #e0e0e0',
                borderRadius: '8px',
                fontSize: '15px',
                background: '#fafafa',
                color: '#333',
                transition: 'border 0.3s',
                outline: 'none'
              }}
              onFocus={(e) => e.target.style.border = '2px solid #4caf50'}
              onBlur={(e) => e.target.style.border = '2px solid #e0e0e0'}
            />
          )}
          
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            style={{
              padding: '14px',
              border: '2px solid #e0e0e0',
              borderRadius: '8px',
              fontSize: '15px',
              background: '#fafafa',
              color: '#333',
              transition: 'border 0.3s',
              outline: 'none'
            }}
            onFocus={(e) => e.target.style.border = '2px solid #4caf50'}
            onBlur={(e) => e.target.style.border = '2px solid #e0e0e0'}
          />
          
          <input
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            style={{
              padding: '14px',
              border: '2px solid #e0e0e0',
              borderRadius: '8px',
              fontSize: '15px',
              background: '#fafafa',
              color: '#333',
              transition: 'border 0.3s',
              outline: 'none'
            }}
            onFocus={(e) => e.target.style.border = '2px solid #4caf50'}
            onBlur={(e) => e.target.style.border = '2px solid #e0e0e0'}
          />
          
          <button
            onClick={handleSubmit}
            disabled={loading}
            style={{
              padding: '14px',
              background: loading ? '#c8e6c9' : 'linear-gradient(135deg, #66bb6a 0%, #4caf50 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              marginTop: '10px',
              boxShadow: loading ? 'none' : '0 4px 12px rgba(76, 175, 80, 0.3)',
              transition: 'all 0.3s'
            }}
          >
            {loading ? 'Please wait...' : (isLogin ? 'Login' : 'Create Account')}
          </button>
        </div>

        <p style={{ 
          textAlign: 'center', 
          marginTop: '24px', 
          fontSize: '14px', 
          color: '#666' 
        }}>
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <span 
            onClick={() => setIsLogin(!isLogin)}
            style={{ color: '#4caf50', cursor: 'pointer', fontWeight: '600' }}
          >
            {isLogin ? 'Sign Up' : 'Login'}
          </span>
        </p>
      </div>
    </div>
  );
}

// ============================================
// MAIN APP COMPONENT
// ============================================

function App() {
  const [user, setUser] = useState(null);
  const [recipes, setRecipes] = useState([]);
  const [savedRecipes, setSavedRecipes] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [viewMode, setViewMode] = useState('all'); // 'all', 'my', 'saved'
  
  const [newRecipe, setNewRecipe] = useState({
    title: '',
    short_description: '',
    is_public: true
  });

  useEffect(() => {
    if (user) {
      loadRecipes();
      //loadCreatedRecipes() - could be future implementation
      loadSavedRecipes();
    }
  }, [user]);

  async function loadRecipes() {
    setLoading(true);
    const data = await fetchRecipes();
    setRecipes(data);
    setLoading(false);
  }

  async function loadSavedRecipes() {
    const saved = await getSavedRecipes(user.user_id);
    setSavedRecipes(saved.map(s => s.recipe_id));
  }

  async function handleRecipeClick(recipeId) {
    setLoading(true);
    const fullRecipe = await fetchRecipeById(recipeId);
    setSelectedRecipe(fullRecipe);
    setLoading(false);
  }

  async function handleAddRecipe() {
    if (!newRecipe.title.trim()) return;
    
    setLoading(true);
    const recipeData = {
      ...newRecipe,
      creator_user_id: user.user_id
    };
    
    const result = await addRecipe(recipeData);
    if (result) {
      await loadRecipes();
      setShowAddForm(false);
      setNewRecipe({ title: '', short_description: '', is_public: true });
    }
    setLoading(false);
  }

  async function handleSaveRecipe(recipeId) {
    const isSaved = savedRecipes.includes(recipeId);

    const result = isSaved
      ? await unsaveRecipe(user.user_id, recipeId)
      : await saveRecipe(user.user_id, recipeId);

    if (result) {
      await loadSavedRecipes();
    }
  }

  function handleLogout() {
    setUser(null);
    setRecipes([]);
    setSavedRecipes([]);
    setSelectedRecipe(null);
  }

  if (!user) {
    return <AuthPage onLogin={setUser} />;
  }

  const filteredRecipes = recipes.filter(recipe => {
    if (viewMode === 'my') return recipe.creator_user_id === user.user_id;
    if (viewMode === 'saved') return savedRecipes.includes(recipe.recipe_id);
    return true;
  });

  return (
    <div style={{ 
      minHeight: '100vh',
      height: '100%',
      background: 'linear-gradient(135deg, #f0f9e8 0%, #fffbea 100%)',
      padding: '0',
      margin: '0'
    }}>
      <div style={{ 
        width: '100%',
        height: '100%',
        minHeight: '100vh',
        margin: '0',
        padding: '30px',
        boxSizing: 'border-box'
      }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '30px',
          background: '#ffffff',
          padding: '24px 30px',
          borderRadius: '12px',
          boxShadow: '0 4px 16px rgba(76, 175, 80, 0.1)',
          border: '1px solid rgba(76, 175, 80, 0.1)'
        }}>
          <div>
            <h1 style={{ 
              color: '#2d5016', 
              margin: 0, 
              fontSize: '32px',
              fontWeight: '600'
            }}>
              Recipe Recommender
            </h1>
            <p style={{ color: '#7cb342', margin: '8px 0 0 0', fontSize: '16px' }}>
              Welcome back, {user.display_name || user.email}
            </p>
          </div>
          <button
            onClick={handleLogout}
            style={{
              padding: '12px 24px',
              background: '#fff',
              color: '#d32f2f',
              border: '2px solid #d32f2f',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '600',
              transition: 'all 0.3s'
            }}
            onMouseEnter={(e) => {
              e.target.style.background = '#d32f2f';
              e.target.style.color = '#fff';
            }}
            onMouseLeave={(e) => {
              e.target.style.background = '#fff';
              e.target.style.color = '#d32f2f';
            }}
          >
            Logout
          </button>
        </div>

        <div style={{ display: 'flex', gap: '12px', marginBottom: '24px', flexWrap: 'wrap' }}>
          <button 
            onClick={() => setShowAddForm(!showAddForm)}
            style={{
              padding: '14px 28px',
              background: showAddForm ? '#fff' : 'linear-gradient(135deg, #fdd835 0%, #fbc02d 100%)',
              color: showAddForm ? '#f57f17' : '#fff',
              border: showAddForm ? '2px solid #f57f17' : 'none',
              borderRadius: '10px',
              cursor: 'pointer',
              fontSize: '15px',
              fontWeight: '600',
              boxShadow: showAddForm ? 'none' : '0 4px 12px rgba(251, 192, 45, 0.3)',
              transition: 'all 0.3s'
            }}
          >
            {showAddForm ? 'Cancel' : 'Add New Recipe'}
          </button>

          <button 
            onClick={() => setViewMode('all')}
            style={{
              padding: '14px 28px',
              background: viewMode === 'all' ? 'linear-gradient(135deg, #66bb6a 0%, #4caf50 100%)' : '#fff',
              color: viewMode === 'all' ? '#fff' : '#4caf50',
              border: viewMode === 'all' ? 'none' : '2px solid #4caf50',
              borderRadius: '10px',
              cursor: 'pointer',
              fontSize: '15px',
              fontWeight: '600',
              boxShadow: viewMode === 'all' ? '0 4px 12px rgba(76, 175, 80, 0.3)' : 'none',
              transition: 'all 0.3s'
            }}
          >
            All Recipes
          </button>

          <button 
            onClick={() => setViewMode('my')}
            style={{
              padding: '14px 28px',
              background: viewMode === 'my' ? 'linear-gradient(135deg, #66bb6a 0%, #4caf50 100%)' : '#fff',
              color: viewMode === 'my' ? '#fff' : '#4caf50',
              border: viewMode === 'my' ? 'none' : '2px solid #4caf50',
              borderRadius: '10px',
              cursor: 'pointer',
              fontSize: '15px',
              fontWeight: '600',
              boxShadow: viewMode === 'my' ? '0 4px 12px rgba(76, 175, 80, 0.3)' : 'none',
              transition: 'all 0.3s'
            }}
          >
            My Recipes
          </button>

          <button 
            onClick={() => setViewMode('saved')}
            style={{
              padding: '14px 28px',
              background: viewMode === 'saved' ? 'linear-gradient(135deg, #66bb6a 0%, #4caf50 100%)' : '#fff',
              color: viewMode === 'saved' ? '#fff' : '#4caf50',
              border: viewMode === 'saved' ? 'none' : '2px solid #4caf50',
              borderRadius: '10px',
              cursor: 'pointer',
              fontSize: '15px',
              fontWeight: '600',
              boxShadow: viewMode === 'saved' ? '0 4px 12px rgba(76, 175, 80, 0.3)' : 'none',
              transition: 'all 0.3s'
            }}
          >
            Saved ({savedRecipes.length})
          </button>
        </div>

        {showAddForm && (
          <div style={{
            background: '#ffffff',
            padding: '24px',
            borderRadius: '12px',
            marginBottom: '30px',
            border: '1px solid rgba(76, 175, 80, 0.2)',
            boxShadow: '0 4px 16px rgba(76, 175, 80, 0.1)'
          }}>
            <h3 style={{ marginTop: 0, color: '#2d5016', fontSize: '20px', fontWeight: '600' }}>
              Add New Recipe
            </h3>
            
            <input
              type="text"
              placeholder="Recipe Title"
              value={newRecipe.title}
              onChange={(e) => setNewRecipe({...newRecipe, title: e.target.value})}
              style={{
                width: '100%',
                padding: '14px',
                marginBottom: '12px',
                borderRadius: '8px',
                border: '2px solid #e0e0e0',
                fontSize: '15px',
                boxSizing: 'border-box',
                background: '#fafafa',
                color: '#333',
                outline: 'none',
                transition: 'border 0.3s'
              }}
              onFocus={(e) => e.target.style.border = '2px solid #4caf50'}
              onBlur={(e) => e.target.style.border = '2px solid #e0e0e0'}
            />
            
            <textarea
              placeholder="Short Description"
              value={newRecipe.short_description}
              onChange={(e) => setNewRecipe({...newRecipe, short_description: e.target.value})}
              style={{
                width: '100%',
                padding: '14px',
                marginBottom: '12px',
                borderRadius: '8px',
                border: '2px solid #e0e0e0',
                fontSize: '15px',
                minHeight: '100px',
                boxSizing: 'border-box',
                background: '#fafafa',
                color: '#333',
                outline: 'none',
                resize: 'vertical',
                transition: 'border 0.3s',
                fontFamily: 'inherit'
              }}
              onFocus={(e) => e.target.style.border = '2px solid #4caf50'}
              onBlur={(e) => e.target.style.border = '2px solid #e0e0e0'}
            />
            
            <label style={{ 
              display: 'flex', 
              alignItems: 'center', 
              marginBottom: '18px', 
              color: '#555',
              fontSize: '15px',
              cursor: 'pointer'
            }}>
              <input
                type="checkbox"
                checked={newRecipe.is_public}
                onChange={(e) => setNewRecipe({...newRecipe, is_public: e.target.checked})}
                style={{ marginRight: '10px', width: '18px', height: '18px', cursor: 'pointer' }}
              />
              Make recipe public (others can see it)
            </label>
            
            <button onClick={handleAddRecipe} style={{
              padding: '12px 28px',
              background: 'linear-gradient(135deg, #66bb6a 0%, #4caf50 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '15px',
              fontWeight: '600',
              boxShadow: '0 4px 12px rgba(76, 175, 80, 0.3)',
              transition: 'all 0.3s'
            }}>
              Save Recipe
            </button>
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          <div>
            <h2 style={{ 
              color: '#2d5016',
              fontSize: '22px',
              fontWeight: '600',
              marginBottom: '16px'
            }}>
              {viewMode === 'all' && `All Recipes (${filteredRecipes.length})`}
              {viewMode === 'my' && `My Recipes (${filteredRecipes.length})`}
              {viewMode === 'saved' && `Saved Recipes (${filteredRecipes.length})`}
            </h2>
            {loading && <p style={{ color: '#7cb342' }}>Loading...</p>}
            {filteredRecipes.length === 0 && !loading && (
              <p style={{ color: '#9e9e9e' }}>No recipes found.</p>
            )}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {filteredRecipes.map((recipe) => (
                <div
                  key={recipe.recipe_id}
                  style={{
                    padding: '18px',
                    background: selectedRecipe?.recipe_id === recipe.recipe_id ? 'linear-gradient(135deg, #66bb6a 0%, #4caf50 100%)' : '#ffffff',
                    color: selectedRecipe?.recipe_id === recipe.recipe_id ? 'white' : '#333',
                    borderRadius: '10px',
                    cursor: 'pointer',
                    transition: 'all 0.3s',
                    border: selectedRecipe?.recipe_id === recipe.recipe_id ? 'none' : '1px solid rgba(76, 175, 80, 0.2)',
                    position: 'relative',
                    boxShadow: selectedRecipe?.recipe_id === recipe.recipe_id ? '0 4px 16px rgba(76, 175, 80, 0.3)' : '0 2px 8px rgba(0, 0, 0, 0.05)'
                  }}
                  onClick={() => handleRecipeClick(recipe.recipe_id)}
                  onMouseEnter={(e) => {
                    if (selectedRecipe?.recipe_id !== recipe.recipe_id) {
                      e.currentTarget.style.background = '#f1f8f4';
                      e.currentTarget.style.boxShadow = '0 4px 12px rgba(76, 175, 80, 0.15)';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (selectedRecipe?.recipe_id !== recipe.recipe_id) {
                      e.currentTarget.style.background = '#ffffff';
                      e.currentTarget.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.05)';
                    }
                  }}
                >
                  <h3 style={{ 
                    margin: '0 0 6px 0',
                    fontSize: '18px',
                    fontWeight: '600'
                  }}>
                    {recipe.title}
                  </h3>
                  <p style={{ 
                    margin: 0, 
                    fontSize: '14px', 
                    opacity: selectedRecipe?.recipe_id === recipe.recipe_id ? 0.95 : 0.7,
                    lineHeight: '1.5'
                  }}>
                    {recipe.short_description || 'No description'}
                  </p>
                  {recipe.creator_user_id === user.user_id && (
                    <span style={{ 
                      fontSize: '12px', 
                      opacity: 0.8, 
                      fontStyle: 'italic',
                      display: 'block',
                      marginTop: '6px'
                    }}>
                      Your recipe
                    </span>
                  )}
                  {savedRecipes.includes(recipe.recipe_id) && (
                    <span style={{ 
                      position: 'absolute', 
                      top: '14px', 
                      right: '14px', 
                      fontSize: '18px',
                      background: selectedRecipe?.recipe_id === recipe.recipe_id ? 'rgba(255,255,255,0.2)' : '#fff9c4',
                      padding: '6px 10px',
                      borderRadius: '6px',
                      fontWeight: '600',
                      color: selectedRecipe?.recipe_id === recipe.recipe_id ? '#fff' : '#f57f17'
                    }}>
                      Saved
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 style={{ 
              color: '#2d5016',
              fontSize: '22px',
              fontWeight: '600',
              marginBottom: '16px'
            }}>
              Recipe Details
            </h2>
            {!selectedRecipe ? (
              <div style={{ 
                padding: '60px 40px', 
                textAlign: 'center', 
                color: '#9e9e9e',
                background: '#ffffff',
                borderRadius: '10px',
                border: '1px solid rgba(76, 175, 80, 0.2)',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)'
              }}>
                Click a recipe to view details
              </div>
            ) : (
              <div style={{
                background: '#ffffff',
                padding: '24px',
                borderRadius: '10px',
                border: '1px solid rgba(76, 175, 80, 0.2)',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <h3 style={{ 
                    color: '#2d5016', 
                    marginTop: 0,
                    fontSize: '24px',
                    fontWeight: '600'
                  }}>
                    {selectedRecipe.title}
                  </h3>
                  {selectedRecipe.creator_user_id !== user.user_id && (
                    <button
                      onClick={() => handleSaveRecipe(selectedRecipe.recipe_id)}
                      style={{
                        padding: '10px 20px',
                        background: savedRecipes.includes(selectedRecipe.recipe_id) ? '#ff9800' : 'linear-gradient(135deg, #fdd835 0%, #fbc02d 100%)',
                        color: '#fff',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontWeight: '600',
                        boxShadow: '0 4px 12px rgba(251, 192, 45, 0.3)',
                        transition: 'all 0.3s'
                      }}
                    >
                      {savedRecipes.includes(selectedRecipe.recipe_id) ? 'Unsave Recipe' : 'Save Recipe'}
                    </button>
                  )}
                </div>
                
                <p style={{ 
                  color: '#555', 
                  marginBottom: '24px',
                  lineHeight: '1.6',
                  fontSize: '15px'
                }}>
                  {selectedRecipe.short_description}
                </p>

                {selectedRecipe.ingredients && selectedRecipe.ingredients.length > 0 && (
                  <div style={{ marginBottom: '24px' }}>
                    <h4 style={{ 
                      color: '#2d5016',
                      fontSize: '18px',
                      fontWeight: '600',
                      marginBottom: '12px'
                    }}>
                      Ingredients
                    </h4>
                    <ul style={{ 
                      color: '#555',
                      lineHeight: '1.8',
                      paddingLeft: '20px'
                    }}>
                      {selectedRecipe.ingredients.map((ing, idx) => (
                        <li key={idx}>
                          {ing.quantity} {ing.unit} {ing.name}
                          {ing.optional && ' (optional)'}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {selectedRecipe.equipment && selectedRecipe.equipment.length > 0 && (
                  <div style={{ marginBottom: '24px' }}>
                    <h4 style={{ 
                      color: '#2d5016',
                      fontSize: '18px',
                      fontWeight: '600',
                      marginBottom: '12px'
                    }}>
                      Equipment
                    </h4>
                    <ul style={{ 
                      color: '#555',
                      lineHeight: '1.8',
                      paddingLeft: '20px'
                    }}>
                      {selectedRecipe.equipment.map((eq, idx) => (
                        <li key={idx}>{eq.name}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div style={{
                  background: '#f1f8f4',
                  padding: '18px',
                  borderRadius: '8px',
                  marginBottom: '20px',
                  border: '1px solid #c8e6c9'
                }}>
                  <h4 style={{
                    marginTop: 0,
                    marginBottom: '12px',
                    color: '#2d5016',
                    fontSize: '18px',
                    fontWeight: '600'
                  }}>
                    Recipe Info
                  </h4>
                  <p style={{ color: '#555', margin: '6px 0', fontSize: '15px' }}>
                    <strong>Prep Time:</strong> {selectedRecipe.metadata?.prep_time_min || 'N/A'} min
                  </p>
                  <p style={{ color: '#555', margin: '6px 0', fontSize: '15px' }}>
                    <strong>Cook Time:</strong> {selectedRecipe.metadata?.cook_time_min || 'N/A'} min
                  </p>
                  <p style={{ color: '#555', margin: '6px 0', fontSize: '15px' }}>
                    <strong>Total Time:</strong> {selectedRecipe.metadata?.total_time_min || 'N/A'} min
                  </p>
                  <p style={{ color: '#555', margin: '6px 0', fontSize: '15px' }}>
                    <strong>Servings:</strong> {selectedRecipe.metadata?.servings || 'N/A'}
                  </p>
                  <p style={{ color: '#555', margin: '6px 0', fontSize: '15px' }}>
                    <strong>Difficulty:</strong> {selectedRecipe.metadata?.difficulty || 'N/A'}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
