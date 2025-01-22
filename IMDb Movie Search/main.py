from imdb import IMDb

ia = IMDb()

while True:
    user_input = input("Enter the movie title or exit(e): ")
    
    if user_input == "e": break
    
    movies = ia.search_movie(user_input)

    if movies:
        first_movie = movies[0]
        movie_id = first_movie.movieID
        full_info = ia.get_movie(movie_id)
        
        print("\n--- Movie Details ---")
        print(f"Title: {full_info.get('title')}")
        print(f"Year: {full_info.get('year')}")
        print(f"Genres: {', '.join(full_info.get('genres', []))}")
        print(f"Director: {', '.join(str(d) for d in full_info.get('directors', []))}")
        print(f"Cast: {', '.join(str(c) for c in full_info.get('cast', [])[:5])}")  # Top 5 cast members
        print(f"Plot: {full_info.get('plot outline', 'N/A')}")
        print(f"Runtime: {full_info.get('runtimes', ['N/A'])[0]} minutes")
    else:
        print("No movies found with that title.")
    
    print('\n\n')
