from flask import Flask, flash, render_template, redirect, session, json
from flask_share import Share
import requests
from configparser import ConfigParser


config = ConfigParser()
config.read('keys_config.cfg')
token = config.get('RapidAPI', 'api_key')


app = Flask(__name__) #Defining our app
app.config['SECRET_KEY'] = "SuperSecretKey"
share = Share(app)


def Attributestore(): #This function holds the attributes for: RecipeID, CookingTime,RecipeName,Directions, Ingredients and URL to an image of the Recipename
	pass

 #Calling the GetNewReci


def GetNewRecipe(): #function that will get a new recipe from the API and fetch an Image, then store all the variables in the Attributestore for later use
	print("Function Running... \nFetching new recipe...  \nCalling the BreakFast API for a new Recipe and Searching for an image \n#############################################\n\n ")
	response = requests.get(url='https://breakfastapi.fun/')
	recipe = response.json()
	#Breaking out different parameters from the JSON response that we get from the breakfast API
	RecipeID = (recipe['recipe']['id'])
	CookingTime = (recipe['recipe']['total_duration'])
	RecipeName = (recipe['recipe']['name'])
	Directions = (recipe['recipe']['directions'])
	Ingredients = (recipe['recipe']['ingredients'])
	print("\n#############################################\n\n Recipe found: " + RecipeName)
	#Fetching a picture based on the RecipeName // Commented out so I don't burn through my image search credit
	
	url = "https://bing-image-search1.p.rapidapi.com/images/search"
	querystring = {"q":RecipeName,"count":"1"}
	headers = {
		'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
		'x-rapidapi-key': token
		}
	Image = requests.request("GET", url, headers=headers, params=querystring)
	Image = Image.json()
	ImageURL = (Image["value"][0]["contentUrl"])
	setattr(Attributestore, 'ImageURL', ImageURL) #Enable this line to set Reset the Image URL again
	#Adding the Variables to def AttributeStore
	#This line sets a hardcoded imageURL to a picture of an avocado
	#setattr(Attributestore, 'ImageURL', "https://learnenglishteens.britishcouncil.org/sites/teens/files/styles/article/public/rs7776_thinkstockphotos-856586464_1-low.jpg")
	setattr(Attributestore, 'RecipeID', RecipeID)
	setattr(Attributestore, 'CookingTime', CookingTime)
	setattr(Attributestore, 'RecipeName', RecipeName)
	setattr(Attributestore, 'Directions', Directions)
	setattr(Attributestore, 'Ingredients', Ingredients)
	setattr(Attributestore, 'Recipe', recipe)
	
def CountRecipesServed(): #Counting how many Recipes were served and updating the number stored in Attributestore
	GettingRecipeServed = getattr(Attributestore, "RecipeServed")
	AddedOne = GettingRecipeServed + 1
	setattr(Attributestore, 'RecipeServed', AddedOne)

def CountButtonNewRecipePressed(): #Counting how many times this user taps get new recipe
	ButtonPressed = getattr(Attributestore, "ButtonPressed")
	if ButtonPressed >= 5:
		setattr(Attributestore, 'ButtonPressed', 0)
	else:
		AddedOne = ButtonPressed + 1
		setattr(Attributestore, 'ButtonPressed', AddedOne)
	

@app.route("/add_to_favourites") #Add the current recipe on display to the favourites list that is stored in session
def add_to_cart():
	CurrentRecipeName = getattr(Attributestore, "Recipe") #Adds the recipe ID of the current Recipe and adds it to the session of the user. After that the user is redirected to the favourites page
	CurrentImageURL = getattr(Attributestore, "ImageURL") #Adds the Image URL
	if 'cart' not in session: #If no items exist in the session we'll create a list called cart
		session['cart'] = []

	if CurrentRecipeName in session['cart']: #If the current recipe already exists in the cart, then we flash a warning 
		flash("You already added this recipe to your favourites, check them out!", "warning")
	else:
		CurrentRecipeName['recipe']["ImageUrl"] = CurrentImageURL
		session['cart'].append(CurrentRecipeName) #Else we add the recipe to the list of favourites and flash a confirmation message
		flash("Nice! This recipe was added to your favourites", "success")
	print(session)

	return redirect("/")

@app.route("/delete_favourites") #This dumps all the data in session
def delete_favourites():
	session.pop("cart")
	flash("Your favourites are deleted, get a new recipe if you're ready to try something new!", "danger")
	return render_template("favourites.html", session=session, RecipeServed=getattr(Attributestore, "RecipeServed"))

@app.route("/delete_one_favourite") #This dumps all the data in session
def delete_one_favourite():
	session.pop("cart")
	flash("You deleted one of your favourites", "danger")
	return render_template("favourites.html", session=session, RecipeServed=getattr(Attributestore, "RecipeServed"))

@app.route("/favourites") #This is the page that shows the recipes
def favourites():
	return render_template("favourites.html", session=session, RecipeServed=getattr(Attributestore, "RecipeServed"))    

@app.route("/new")  # If the user hits the /new endpoint we'll fetch a new recipe and return that recipe to the index page. 
def new():
	GetNewRecipe(); #Fetching the new recipe using the function
	CountRecipesServed(); #adding one to the Countrecipe counter
	CountButtonNewRecipePressed()
	ButtonCount = getattr(Attributestore, "ButtonPressed")
	if ButtonCount >= 5:
		flash("Holy guacamole! You seem to really love InstaRecipe, Did you know you can save the recipes you, like by tapping: Save this Recipe",  "info")
	else:
		flash("Here is your brand new recipe, enjoy! ", "success")
	return render_template("index.html", header="Instant Recipe", RecipeName=getattr(Attributestore, "RecipeName"), Ingredients=getattr(Attributestore, "Ingredients"), Directions=getattr(Attributestore, "Directions"), RecipeID = getattr(Attributestore, "RecipeID"), CookingTime = getattr(Attributestore, "CookingTime"), ImageURL = getattr(Attributestore, "ImageURL"),RecipeServed=getattr(Attributestore, "RecipeServed"))

@app.route("/")  # Defining the landing page of our site
def home():
	CountRecipesServed(); #adding one to the Countrecipe counter
	flash("If you don't like this recipe, simply tap: 'New Recipe', to try something else! ", "info")
	return render_template("index.html", header="Instant Recipe", RecipeName=getattr(Attributestore, "RecipeName"), Ingredients=getattr(Attributestore, "Ingredients"), Directions=getattr(Attributestore, "Directions"), RecipeID = getattr(Attributestore, "RecipeID"), CookingTime = getattr(Attributestore, "CookingTime"), ImageURL = getattr(Attributestore, "ImageURL"), RecipeServed=getattr(Attributestore, "RecipeServed"))

@app.route("/about")  # Creating the About page 
def about():
	print("\n#############################################\n\n A user visited the previous page")	
	return render_template("about.html")    # some basic inline html

@app.route('/recipe/<SpecificRecipe>')
def GetSpecificRecipe(SpecificRecipe=0):
	print(SpecificRecipe)
	print(type(SpecificRecipe))
	url = "https://breakfastapi.fun/"
	UrlPlusRequestedRecipe = url + SpecificRecipe
	print(UrlPlusRequestedRecipe)
	response = requests.get(url=UrlPlusRequestedRecipe)
	print(response)
	recipe = response.json()
	#Breaking out different parameters from the JSON response that we get from the breakfast API
	
	RecipeID = (recipe['recipe']['id'])
	CookingTime = (recipe['recipe']['total_duration'])
	RecipeName = (recipe['recipe']['name'])
	Directions = (recipe['recipe']['directions'])
	Ingredients = (recipe['recipe']['ingredients'])
	print("\n#############################################\n\n Recipe found: " + RecipeName)
	#Fetching a picture based on the RecipeName // Commented out so I don't burn through my image search credit
	
	url = "https://bing-image-search1.p.rapidapi.com/images/search"
	querystring = {"q":RecipeName,"count":"1"}
	headers = {
		'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
		'x-rapidapi-key': token
		}
	Image = requests.request("GET", url, headers=headers, params=querystring)
	Image = Image.json()
	ImageURL = (Image["value"][0]["contentUrl"])
	setattr(Attributestore, 'ImageURL', ImageURL) #Enable this line to set Reset the Image URL again
	#Adding the Variables to def AttributeStore
	#This line sets a hardcoded imageURL to a picture of an avocado
	#setattr(Attributestore, 'ImageURL', "https://learnenglishteens.britishcouncil.org/sites/teens/files/styles/article/public/rs7776_thinkstockphotos-856586464_1-low.jpg")
	setattr(Attributestore, 'RecipeID', RecipeID)
	setattr(Attributestore, 'CookingTime', CookingTime)
	setattr(Attributestore, 'RecipeName', RecipeName)
	setattr(Attributestore, 'Directions', Directions)
	setattr(Attributestore, 'Ingredients', Ingredients)
	setattr(Attributestore, 'Recipe', recipe)
	
	return render_template("index.html", header="Instant Recipe", RecipeName=getattr(Attributestore, "RecipeName"), Ingredients=getattr(Attributestore, "Ingredients"), Directions=getattr(Attributestore, "Directions"), RecipeID = getattr(Attributestore, "RecipeID"), CookingTime = getattr(Attributestore, "CookingTime"), ImageURL = getattr(Attributestore, "ImageURL"),RecipeServed=getattr(Attributestore, "RecipeServed"))

#initializing
setattr(Attributestore, 'RecipeServed', 231)
setattr(Attributestore, 'ButtonPressed', 4)
GetNewRecipe();


if __name__ == "__main__": #Run the app
	setattr(Attributestore, 'RecipeServed', 231)
	setattr(Attributestore, 'ButtonPressed', 4)
	GetNewRecipe(); #Calling the GetNewRecipe function, so we set a first Recipe on startup
	app.run(host='0.0.0.0', debug=True)

