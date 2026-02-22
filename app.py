from flask import Flask, render_template, request, redirect, url_for, flash, session

import mysql.connector
import re
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "secret123"  # session secret

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_youtube_url(url):
    if not url:
        return False
    return (
        url.startswith("https://www.youtube.com/watch?v=") or
        url.startswith("https://youtube.com/watch?v=") or
        url.startswith("https://youtu.be/")
    )

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',          # MySQL server (usually localhost)
        user='root',               # your MySQL username
        password='Reema2005',   # your MySQL password
        database='Cinema'          # your database name
    )
    return conn

# ------------------ DATA MODELS  ------------------

class User:
    def __init__(self, user_id, first_name, last_name, email, phone, password):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password


class Admin:
    def __init__(self, admin_id, first_name, last_name, email, phone, password):
        self.admin_id = admin_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password


class Movie:
    def __init__(self, movie_id, title, description, duration, genre, age_rating, poster):
        self.movie_id = movie_id
        self.title = title
        self.description = description
        self.duration = duration
        self.genre = genre
        self.age_rating = age_rating
        self.poster = poster


class Showtime:
    def __init__(self, showtime_id, movie_id, hall_number, show_date, show_time):
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.hall_number = hall_number
        self.show_date = show_date
        self.show_time = show_time


class Booking:
    def __init__(self, booking_id, user_id, showtime_id, booking_date, total_price, payment_status):
        self.booking_id = booking_id
        self.user_id = user_id
        self.showtime_id = showtime_id
        self.booking_date = booking_date
        self.total_price = total_price
        self.payment_status = payment_status


class Payment:
    def __init__(self, payment_id, booking_id, payment_method, amount, status):
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.payment_method = payment_method
        self.amount = amount
        self.status = status


# ----- Home -----
@app.route('/')
def home():
    return render_template('home.html')

# ----- Sign In (Guest) -----
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        first_name = request.form.get("first_name").strip()
        last_name = request.form.get("last_name").strip()
        email = request.form.get("email").strip()
        phone = request.form.get("phone").strip()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validate required fields
        if not first_name or not last_name or not email or not password or not confirm_password:
            flash("All fields except phone are required.")
            return redirect(url_for('sign_in'))

        # Email must be @gmail.com
        if not re.match(r'^[\w\.-]+@gmail\.com$', email):
            flash("Email must be a valid Gmail address (something@gmail.com).")
            return redirect(url_for('sign_in'))

        # Password rules: letters + number + special char, at least 6 chars
        if len(password) < 6 or \
           not re.search(r'[A-Za-z]', password) or \
           not re.search(r'\d', password) or \
           not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            flash("Password must be at least 6 characters long and include letters, numbers, and a special character.")
            return redirect(url_for('sign_in'))

        # Check passwords match
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('sign_in'))

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM Users WHERE Email_u = %s", (email,))
        if cursor.fetchone():
            flash("Email already registered.")
            cursor.close()
            conn.close()
            return redirect(url_for('sign_in'))

        # Insert new user
        cursor.execute(
            "INSERT INTO Users (First_Name_u, Last_Name_u, Email_u, Phone_Number_u, Pass_u) VALUES (%s,%s,%s,%s,%s)",
            (first_name, last_name, email, phone, password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Account created! Please log in.")
        return redirect(url_for('guest_login'))

    return render_template('sign_in.html')


@app.route('/profile')
def profile():
    # must be logged in as either guest or admin
    if session.get("logged_in_as") not in ["guest", "admin"]:
        flash("Please log in first.")
        return redirect(url_for('sign_in'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if session.get("logged_in_as") == "admin":
        # admin stored in admin_id
        cursor.execute("""
            SELECT First_Name_a AS first_name, Last_Name_a AS last_name,
                   Email_a AS email, Phone_Number_a AS phone
            FROM Admins
            WHERE Admin_Id = %s
        """, (session.get("admin_id"),))
    else:
        # guest stored in user_id
        cursor.execute("""
            SELECT First_Name_u AS first_name, Last_Name_u AS last_name,
                   Email_u AS email, Phone_Number_u AS phone
            FROM Users
            WHERE User_Id = %s
        """, (session.get("user_id"),))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        flash("User not found.")
        return redirect(url_for('home'))

    return render_template("profile.html", user=user)




# ----- Guest Login -----
@app.route('/guest_login', methods=['GET', 'POST'])
def guest_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE Email_u = %s AND Pass_u = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session["logged_in_as"] = "guest"
            session["user_id"] = user["User_Id"]
            flash(f"Guest login successful! Welcome {user['First_Name_u']}")
            return redirect(url_for('movies_page'))
        else:
            flash("Incorrect email or password.")
            return redirect(url_for('guest_login'))

    return render_template('guest_login.html')


# ----- Admin Login -----
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    session.pop('_flashes',None)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Admins WHERE Email_a = %s AND Pass_a = %s", (email, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if admin:
            session["logged_in_as"] = "admin"
            session["admin_id"] = admin["Admin_Id"]
            flash(f"Welcome Admin {admin['First_Name_a']}")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin credentials.")
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # Only admins can access
    if session.get("logged_in_as") != "admin":
        flash("Please log in as admin first.")
        return redirect(url_for("admin_login"))

    admin_id = int(session.get("admin_id"))

    # Connect to DB to get admin info if needed
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Admins WHERE Admin_Id = %s", (admin_id,))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('admin_dashboard.html', admin=admin)


# ----- Movies Page -----
@app.route('/movies')
def movies_page():
    # Only logged in users can see movies
    if session.get("logged_in_as") not in ["guest", "admin"]:
        flash("Please log in first.")
        return redirect(url_for("home"))

    # Connect to MySQL
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get movies from database
    cursor.execute("SELECT Movie_Id, Title, Description_, Duration, Genre, age_rating, Poster FROM Movie")
    movies_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("movies.html", movies=movies_list)


@app.route('/movies/<int:movie_id>/showtimes')
def movie_showtimes(movie_id):
    if session.get("logged_in_as") not in ["guest", "admin"]:
        flash("Please log in first.")
        return redirect(url_for("home"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get movie info
    cursor.execute("SELECT * FROM Movie WHERE Movie_Id = %s", (movie_id,))
    movie = cursor.fetchone()
    if not movie:
        flash("Movie not found.")
        return redirect(url_for("movies_page"))

    # Get showtimes for this movie
    cursor.execute("SELECT * FROM Showtimes WHERE Movie_Id = %s", (movie_id,))
    showtimes = cursor.fetchall()

    # Filter out showtimes that are fully booked
    available_showtimes = []
    for s in showtimes:
        hall = s['Hall_Number']
        # Total seats in this hall
        cursor.execute("SELECT COUNT(*) AS total FROM Seats WHERE Hall_Number = %s", (hall,))
        total_seats = cursor.fetchone()['total']

        # Booked seats for this showtime
        cursor.execute("""
            SELECT COUNT(*) AS booked
            FROM Booking_Seat bs
            JOIN Bookings b ON bs.Booking_Id = b.Booking_Id
            WHERE b.Showtime_Id = %s
        """, (s['Showtime_Id'],))
        booked_seats = cursor.fetchone()['booked']

        if booked_seats < total_seats:
            available_showtimes.append(s)

    cursor.close()
    conn.close()

    return render_template("showtimes.html", movie=movie, showtimes=available_showtimes)


@app.route('/showtimes/<int:showtime_id>/seats')
def seat_selection_showtime(showtime_id):
    if session.get("logged_in_as") not in ["guest", "admin"]:
        flash("Please log in first.")
        return redirect(url_for("home"))

    # Connect to MySQL
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
            SELECT Showtimes.Showtime_Id, Showtimes.Hall_Number, Showtimes.Show_Date, Showtimes.Show_Time, Movie.Movie_Id, Movie.Title
            FROM Showtimes
            JOIN Movie ON Showtimes.Movie_Id = Movie.Movie_Id
            WHERE Showtimes.Showtime_Id = %s
        """, (showtime_id,))
    showtime = cursor.fetchone()

    if not showtime:
        flash("Showtime not found.")
        return redirect(url_for("movies_page"))

    hall = showtime["Hall_Number"]
    movie_id = showtime["Movie_Id"]

    # Get all seats in that hall
    cursor.execute("SELECT Seat_Id, Seat_Row, Seat_Column FROM Seats WHERE Hall_Number = %s", (hall,))
    all_seats = cursor.fetchall()

    seat_map = {s["Seat_Id"]: f"{s['Seat_Row']}{s['Seat_Column']}" for s in all_seats}

    # Get booked seats for this showtime
    cursor.execute("""
            SELECT Seat_Id 
            FROM Booking_Seat 
            JOIN Bookings ON Booking_Seat.Booking_Id = Bookings.Booking_Id
            WHERE Bookings.Showtime_Id = %s
        """, (showtime_id,))
    booked_rows = cursor.fetchall()
    booked_seats = {seat_map[row["Seat_Id"]] for row in booked_rows}

    cursor.close()
    conn.close()

    return render_template(
        "seat_selection.html",
        movie=showtime,
        movie_id=movie_id,
        booked_seats=booked_seats,
        showtime_id=showtime_id
    )

@app.route('/booking/confirmation', methods=['GET','POST'])
def booking_confirmation():
    if session.get("logged_in_as") not in ["guest", "admin"]:
        flash("Please log in first.")
        return redirect(url_for("home"))

    if request.method == "GET":
        # Get query params from seat selection
        movie_id = request.args.get("movie_id")
        showtime_id = request.args.get("showtime_id")
        selected_seats = request.args.get("selected_seats", "").split(',')

        if not selected_seats or selected_seats == ['']:
            flash("No seats selected.")
            return redirect(url_for("movies_page"))

        total_price = 20 * len(selected_seats)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Title FROM Movie WHERE Movie_Id=%s", (movie_id,))
        movie = cursor.fetchone()
        cursor.execute("SELECT Show_Date, Show_Time FROM Showtimes WHERE Showtime_Id=%s", (showtime_id,))
        showtime = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template("booking_confirmation.html",
                               movie_title=movie['Title'],
                               show_date=showtime['Show_Date'],
                               show_time=showtime['Show_Time'],
                               seats=selected_seats,
                               total_price=total_price,
                               movie_id=movie_id,
                               showtime_id=showtime_id,
                               booking_confirmed=False)

    # POST: Process payment and insert booking
    movie_id = request.form.get("movie_id")
    showtime_id = request.form.get("showtime_id")
    seats_list = request.form.get("selected_seats").split(',')
    payment_method = request.form.get("payment_method")
    total_price = float(request.form.get("total_price"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch movie info
    cursor.execute("SELECT Title FROM Movie WHERE Movie_Id=%s", (movie_id,))
    movie = cursor.fetchone()

    # Insert booking
    cursor.execute("""
        INSERT INTO Bookings (User_Id, Showtime_Id, Booking_Date, Total_Price, Payment_Status)
        VALUES (%s, %s, CURDATE(), %s, 'Completed')
    """, (session["user_id"], showtime_id, total_price))
    booking_id = cursor.lastrowid

    # Insert seats
    for seat_id in seats_list:
        cursor.execute("""
            SELECT Seat_Id FROM Seats 
            WHERE Hall_Number = (SELECT Hall_Number FROM Showtimes WHERE Showtime_Id=%s) 
            AND CONCAT(Seat_Row, Seat_Column) = %s
        """, (showtime_id, seat_id))
        seat_db_id = cursor.fetchone()['Seat_Id']
        cursor.execute("INSERT INTO Booking_Seat (Booking_Id, Seat_Id) VALUES (%s,%s)", (booking_id, seat_db_id))

    # Insert payment
    cursor.execute("""
        INSERT INTO Payments (Booking_Id, Payment_Method, Amount, Payment_Status)
        VALUES (%s, %s, %s, 'Completed')
    """, (booking_id, payment_method, total_price))

    conn.commit()
    cursor.close()
    conn.close()

    return render_template("booking_confirmation.html",
                           movie_title=movie['Title'],
                           show_date=request.form.get("show_date"),
                           show_time=request.form.get("show_time"),
                           seats=seats_list,
                           total_price=total_price,
                           booking_confirmed=True)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    booking_id = request.form.get('booking_id')
    payment_method = request.form.get('payment_method')
    total_price = float(request.form.get('total_price'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert payment record
    cursor.execute("""
        INSERT INTO Payments (Booking_Id, Payment_Method, Amount, Payment_Status)
        VALUES (%s, %s, %s, 'Completed')
    """, (booking_id, payment_method, total_price))

    # Update booking status to Completed
    cursor.execute("""
        UPDATE Bookings
        SET Payment_Status = 'Completed'
        WHERE Booking_Id = %s
    """, (booking_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return render_template("booking_confirmation.html",
                           booking_confirmed=True,
                           movie_title=request.form.get('movie_title'),
                           show_date=request.form.get('show_date'),
                           show_time=request.form.get('show_time'),
                           seats=request.form.get('selected_seats').split(','),
                           total_price=total_price,
                           booking_id=booking_id)

@app.route('/guest/booking/history')
def guest_booking_history():
    # Only allow guests
    if session.get("logged_in_as") != "guest":
        flash("Only guests can view booking history.")
        return redirect(url_for("home"))  # this should be guest login or home

    user_id = session.get("user_id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch guest's bookings
    cursor.execute("""
        SELECT b.Booking_Id, b.Booking_Date, b.Total_Price, b.Payment_Status,
               m.Title AS Movie_Title, s.Show_Date, s.Show_Time, s.Hall_Number
        FROM Bookings b
        JOIN Showtimes s ON b.Showtime_Id = s.Showtime_Id
        JOIN Movie m ON s.Movie_Id = m.Movie_Id
        WHERE b.User_Id = %s
        ORDER BY b.Booking_Date DESC
    """, (user_id,))
    bookings = cursor.fetchall()

    # Fetch seats for each booking
    for booking in bookings:
        cursor.execute("""
            SELECT CONCAT(seat.Seat_Row, seat.Seat_Column) AS Seat
            FROM Booking_Seat bs
            JOIN Seats seat ON bs.Seat_Id = seat.Seat_Id
            WHERE bs.Booking_Id = %s
            ORDER BY seat.Seat_Row, seat.Seat_Column
        """, (booking["Booking_Id"],))
        booking["Seats"] = [row["Seat"] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return render_template("guest_booking_history.html", bookings=bookings)

@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if session.get("logged_in_as") != "guest":
        flash("You must be logged in as a guest to cancel a booking.")
        return redirect(url_for("home"))

    user_id = session.get("user_id")  # Make sure you store the logged-in guest's ID in session

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check that the booking belongs to the logged-in guest
        cursor.execute("SELECT Booking_Id FROM Bookings WHERE Booking_Id = %s AND User_Id = %s", (booking_id, user_id))
        booking = cursor.fetchone()
        if not booking:
            flash("Booking not found or you are not allowed to cancel it.")
            return redirect(url_for("guest_booking_history"))

        # Update the booking status to 'Cancelled'
        cursor.execute("UPDATE Bookings SET Payment_Status = 'Cancelled' WHERE Booking_Id = %s", (booking_id,))
        cursor.execute("DELETE FROM Booking_Seat WHERE Booking_Id = %s", (booking_id,))

        conn.commit()
        flash("Booking cancelled successfully!")
        return redirect(url_for("guest_booking_history"))
    except mysql.connector.Error as err:
        print(err)
        flash("An error occurred while cancelling the booking.")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("guest_booking_history"))


@app.route('/admin/manage_movies',  methods=['GET', 'POST'] , endpoint='admin_manage_movies')
def manage_movies():
    # Only admins
    if session.get("logged_in_as") != "admin":
        flash("Please log in as admin first.")
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Handle Add or Update
    if request.method == 'POST':
        movie_id = request.form.get('movie_id')  # will be empty for new movies
        title = request.form.get('title')
        description = request.form.get('description')
        duration = request.form.get('duration')
        genre = request.form.get('genre')
        age_rating = request.form.get('age_rating')
        trailer_url = request.form.get('trailer_url')
        poster_file = request.files.get('poster')

        poster_filename = None
        if poster_file and allowed_file(poster_file.filename):
            poster_filename = secure_filename(poster_file.filename)
            poster_file.save(os.path.join(app.config['UPLOAD_FOLDER'], poster_filename))

        # Validate YouTube URL
        if trailer_url and not is_valid_youtube_url(trailer_url):
            flash("Invalid trailer URL. Only YouTube links are allowed.")
            return redirect(url_for('admin_manage_movies'))

        if movie_id:  # Update existing movie
            if movie_id:  # Update existing movie
                updates = []
                values = []

                if title:
                    updates.append("Title = %s")
                    values.append(title)

                if description:
                    updates.append("Description_ = %s")
                    values.append(description)

                if duration:
                    updates.append("Duration = %s")
                    values.append(duration)

                if genre:
                    updates.append("Genre = %s")
                    values.append(genre)

                if age_rating:
                    updates.append("age_rating = %s")
                    values.append(age_rating)

                if trailer_url:
                    updates.append("Trailer_URL = %s")
                    values.append(trailer_url)

                if poster_filename:  # Only if a new poster was uploaded
                    updates.append("Poster = %s")
                    values.append(poster_filename)

                # If NOTHING was filled → avoid empty update
                if not updates:
                    flash("No changes were made.")
                    return redirect(url_for('admin_manage_movies'))

                # Add movie_id to values for WHERE
                values.append(movie_id)

                query = "UPDATE Movie SET " + ", ".join(updates) + " WHERE Movie_Id = %s"
                cursor.execute(query, values)

                flash("Movie updated successfully!")

        else:  # Add new movie
            if not title or not duration or not genre or not age_rating:
                flash("Title, Duration, Genre, and Age Rating are required.")
                return redirect(url_for('admin_manage_movies'))

            if not poster_file or not allowed_file(poster_file.filename):
                flash("Poster is required for a new movie!")
                return redirect(url_for('admin_manage_movies'))

            cursor.execute("""
                   INSERT INTO Movie (Title, Description_, Duration, Genre, age_rating,Poster,Trailer_URL)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
               """, (title, description, duration, genre, age_rating,poster_filename,trailer_url))
            flash("New movie added successfully!")

        conn.commit()
        return redirect(url_for('admin_manage_movies'))

    # Get all movies to display
    cursor.execute("SELECT * FROM Movie")
    movies = cursor.fetchall()

    cursor.close()
    conn.close()

    age_options = ['G', 'PG', 'PG-13', '14+', '17+', '18+', 'R']
    genre_options = [
        'Adventure', 'Horror', 'Sci-Fi', 'Comedy', 'Family',
        'Drama', 'Fantasy', 'Musical', 'Action', 'Romance'
    ]

    return render_template('manage_movies.html', movies=movies, age_options=age_options, genre_options=genre_options)

@app.route('/admin/manage_showtimes', methods=['GET', 'POST'])
def manage_showtimes():
    if session.get("logged_in_as") != "admin":
        flash("Please log in as admin first.")
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        movie_id = request.form.get("movie_id")
        hall_number = request.form.get("hall_number")
        show_date = request.form.get("show_date")
        show_time = request.form.get("show_time")

        if not movie_id or not hall_number or not show_date or not show_time:
            flash("All fields are required to add a showtime.")
            return redirect(url_for("manage_showtimes"))

        # Check if the hall is free at that date and time
        cursor.execute("""
            SELECT * FROM Showtimes
            WHERE Hall_Number = %s AND Show_Date = %s AND Show_Time = %s
        """, (hall_number, show_date, show_time))
        existing = cursor.fetchone()

        if existing:
            flash(f"{hall_number} is already booked at {show_date} {show_time}.")
            return redirect(url_for("manage_showtimes"))

        # If free, insert new showtime
        cursor.execute("""
            INSERT INTO Showtimes (Movie_Id, Hall_Number, Show_Date, Show_Time)
            VALUES (%s, %s, %s, %s)
        """, (movie_id, hall_number, show_date, show_time))
        conn.commit()
        flash("New showtime added successfully!")
        return redirect(url_for("manage_showtimes"))

    # GET request: fetch all movies and showtimes
    cursor.execute("SELECT Movie_Id, Title FROM Movie")
    movies = cursor.fetchall()

    cursor.execute("""
        SELECT s.Showtime_Id, s.Hall_Number, s.Show_Date, s.Show_Time, m.Title
        FROM Showtimes s
        JOIN Movie m ON s.Movie_Id = m.Movie_Id
        ORDER BY s.Showtime_Id
    """)
    showtimes = cursor.fetchall()

    cursor.close()
    conn.close()

    halls = [f"Hall{i}" for i in range(1, 11)]

    return render_template("manage_showtimes.html", movies=movies, showtimes=showtimes, halls=halls)

@app.route('/admin/booking_history')
def booking_history():
    if session.get("logged_in_as") != "admin":
        flash("Please log in as admin first.")
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.Booking_Id, b.Booking_Date, b.Total_Price, b.Payment_Status,
               s.Show_Date, s.Show_Time, s.Hall_Number, m.Title,
               u.First_Name_u AS User_Name
        FROM Bookings b
        JOIN Showtimes s ON b.Showtime_Id = s.Showtime_Id
        JOIN Movie m ON s.Movie_Id = m.Movie_Id
        JOIN Users u ON b.User_Id = u.User_Id
        ORDER BY b.Booking_Date DESC
    """)
    bookings = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('booking_history.html', bookings=bookings)

@app.route('/admin/manage_admins', methods=['GET', 'POST'])
def manage_admins():
    if session.get("logged_in_as") != "admin":
        flash("Please log in as admin first.")
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # --- HANDLE POST ACTIONS ---
    if request.method == "POST":
        action = request.form.get("action")
        user_id = request.form.get("user_id")

        if action == "grant":
            # get user from Users table
            cursor.execute("SELECT * FROM Users WHERE User_Id = %s", (user_id,))
            user = cursor.fetchone()

            if not user:
                flash("User not found.")
                return redirect(url_for("manage_admins"))

            # check if already granted by email
            cursor.execute("SELECT * FROM Admins WHERE  Email_a = %s", (user["Email_u"],))
            existing_admin = cursor.fetchone()

            if existing_admin:
                flash("This user is already an admin.")
                return redirect(url_for("manage_admins"))

            # insert into Admins table (NEW ACCOUNT)
            cursor.execute("""
                INSERT INTO Admins (First_Name_a, Last_Name_a, Email_a, Phone_Number_a, Pass_a)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                user["First_Name_u"],
                user["Last_Name_u"],
                user["Email_u"],
                user["Phone_Number_u"],
                user["Pass_u"]
            ))

            flash(f"{user['First_Name_u']} {user['Last_Name_u']} granted admin access.")

        elif action == "revoke":
            admin_id = request.form.get("user_id")
            cursor.execute("DELETE FROM Admins WHERE Admin_Id = %s", (admin_id,))
            flash("Admin access revoked.")

        conn.commit()
        return redirect(url_for("manage_admins"))

    # --- LOAD DATA INTO TABLES ---
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()

    # Only show admins who also exist in Users (granted users)
    cursor.execute("""
            SELECT A.*
            FROM Admins A
            JOIN Users U ON A.Email_a = U.Email_u
        """)
    granted_admins = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("manage_admins.html", users=users, granted_admins=granted_admins)

@app.route('/logout')
def logout():
    session.clear()  # clears all session data
    flash("You have been logged out.")
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
