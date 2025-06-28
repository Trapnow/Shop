from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from ..functions import calculate_average_rating
from ..extensions import db

from ..models.book import Book, Section, Comment

import json

book = Blueprint('book', __name__)


@book.route("/")
def index():
    top_books = Book.query.order_by(Book.sales_count.desc()).limit(3).all()
    sections = Section.query.all()
    return render_template('index.html', top_books=top_books, sections=sections)


@book.route("/add_books")
def create_table():
    with open('books_catalog.json', 'r') as file:
        data = json.load(file)
    for item in data:
        new_book = Book(title=item["title"], author=item["author"], price=item["price"], genre=item["genre"],
                        cover=item["cover"], description=item["description"],
                        year=item["year"])
        db.session.add(new_book)
    db.session.commit()
    return render_template("index.html")


@book.route("/list_books", methods=["GET"])
def list_books():
    sections = Section.query.all()

    genre = request.args.get('genre', None)
    query = request.args.get('query', '')


    if genre:
        books = Book.query.filter(
            Book.genre.ilike(f'%{genre}%')
        )
    else:
        books = Book.query


    if query:
        books = books.filter(
            (Book.title.ilike(f'%{query}%')) |
            (Book.author.ilike(f'%{query}%'))
        )

    books = books.all()

    return render_template(
        "list_books.html",
        books=books,
        sections=sections,
        selected_genre=genre,
        search_query=query
    )


@book.route('/book/<int:book_id>', methods=['GET'])
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('detail.html', book=book)


@book.route('/book/<int:book_id>/comment', methods=['POST'])
@login_required
def add_comment(book_id):
    book = Book.query.get_or_404(book_id)

    if not current_user.is_authenticated:
        return redirect(url_for('book.book_detail', book_id=book_id))

    content = request.form.get('content')
    rating = request.form.get('rating', type=int)

    new_comment = Comment(
        user_id=current_user.id,
        book_id=book_id,
        content=content,
        rating=rating,
        created_at=datetime.utcnow()
    )

    db.session.add(new_comment)

    book.rating = book.average_rating

    db.session.commit()

    calculate_average_rating(book)

    return redirect(url_for('book.book_detail', book_id=book_id))
