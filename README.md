# 🥘 🥣 InstaRecipe -- 12.000 recipes served instantly
_InstaRecipe is a Flask webapplication that serves 12.000 recipes instantly, it gets it's recipes from the [breakfast API](https://github.com/MariiaSizova/breakfastapi) and based on the name of the recipe it fetches an image using RapidAPI ._ 

**Check out the demo:** https://flask-service.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/

# Why such a fuss for such a simple app? 
If you're reading this you probably have more experience developing software than I do. To be frank: It took me more than a week to build this app, spending many late hours googling the most basic questions on stackoverflow. Anyway: I'm genuinly very proud as it's the first time I built something with so many moving parts. For now it will serve as a portfolio project as it's currently the pinacle of my softwaredevelopment skillset. But most of all it is a reminder to myself that I am capable of


it was the perfect project to better understand some new (to me) technologies. 

These were my goals: 
- Build a webapp with a backend -- I used flask for the very first time
- Do some kind of session related logic -- In my case I ended up storing favourites in the session
- Use an API -- Breakfast API was very convenient as it did not deal with authentication and returns very straight forward fields. 
- Use a frontend framework -- In this case Bootstrap
- Use AWS for hosting -- I developed using an EC2 instance and later I used Lightsail to host a docker image. 

What I did not get to work yet:
- Setting a javascript spinner in the button on getting a new Recipe
- Storing the current recipe in the session -- these
