from flask import Blueprint, render_template, request, redirect, url_for

from ..extensions import db

from ..models.book import Book, Section

import json

book = Blueprint('book', __name__)


@book.route("/")
def index():
    sections = Section.query.all()
    return render_template("index.html", sections=sections)

@book.route("/add_books")
def create_table():
    with open('books_catalog.json', 'r') as file:
        data = json.load(file)
    for item in data:
        new_book = Book(title=item["title"], author=item["author"], price=item["price"], genre=item["genre"],
                        cover=item["cover"], description=item["description"], rating=item["rating"],
                        year=item["year"])  # Создаем объект задачи
        db.session.add(new_book)
    db.session.commit()
    return render_template("index.html")

@book.route("/list_books", methods = ["GET"])
def list_books():
    sections = Section.query.all()

    genre = request.args.get('genre', None)

    if genre:
        books = Book.query.filter(Book.genre.ilike(f'%{genre}%')).all()
    else:
        books = Book.query.all()

    return render_template("list_books.html", books=books, sections=sections, selected_genre=genre)