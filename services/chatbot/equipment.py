import requests

url = "https://exercise-db-fitness-workout-gym.p.rapidapi.com/list/mechanic"

headers = {
	"x-rapidapi-key": "3a1357336bmsh23043507c9757d5p1ab00ajsn6605ce93c419",
	"x-rapidapi-host": "exercise-db-fitness-workout-gym.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())