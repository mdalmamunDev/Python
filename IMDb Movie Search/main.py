from imdb import IMDb
import tkinter as tk
from tkinter import ttk, messagebox

# Initialize IMDb instance
ia = IMDb()

# Function to search and display movie details
def search_movie():
    movie_title = entry.get().strip()
    if not movie_title:
        messagebox.showerror("Error", "Please enter a movie title.")
        return

    # Clear previous result
    result_text.set("")
    loading_label.pack(pady=5)  # Show the loading message
    root.update_idletasks()  # Update UI to show loader

    try:
        movies = ia.search_movie(movie_title)
        if movies:
            # Get details of the first movie
            first_movie = movies[0]
            movie_id = first_movie.movieID
            full_info = ia.get_movie(movie_id)

            # Format movie details
            details = (
                f"Title: {full_info.get('title')}\n"
                f"Year: {full_info.get('year')}\n"
                f"Genres: {', '.join(full_info.get('genres', []))}\n"
                f"Director: {', '.join(str(d) for d in full_info.get('directors', []))}\n"
                f"Cast: {', '.join(str(c) for c in full_info.get('cast', [])[:5])}\n"
                f"Plot: {full_info.get('plot outline', 'N/A')}\n"
                f"Runtime: {full_info.get('runtimes', ['N/A'])[0]} minutes"
            )
            result_text.set(details)
        else:
            result_text.set("No movies found with that title.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        loading_label.pack_forget()  # Hide the loading message

def clear_fields():
    entry.delete(0, tk.END)
    result_text.set("")

# Create the main Tkinter window
root = tk.Tk()
root.title("IMDb Movie Search")
root.geometry("500x500")

# Widgets
label = tk.Label(root, text="Enter Movie Title:", font=("Arial", 14))
label.pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=search_movie, font=("Arial", 12), bg="blue", fg="white")
search_button.pack(pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_fields, font=("Arial", 12), bg="gray", fg="white")
clear_button.pack(pady=5)

result_label = tk.Label(root, text="Movie Details:", font=("Arial", 14))
result_label.pack(pady=10)

# Loading Label
loading_label = tk.Label(root, text="Loading...", font=("Arial", 12), fg="red")

# Scrollable Text Area for Results
result_frame = tk.Frame(root)
result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.StringVar()
result_display = tk.Text(result_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=("Arial", 12))
result_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=result_display.yview)

# Link result_text to the Text widget
def update_result_text(*args):
    result_display.delete(1.0, tk.END)
    result_display.insert(tk.END, result_text.get())

result_text.trace("w", update_result_text)

# Run the Tkinter event loop
root.mainloop()
