import strawberry


def get_author_for_book() -> "Author":
    return Author(name="Michael Crichton")


@strawberry.type
class Book:
    title: str
    author: "Author" = strawberry.field(resolver=get_author_for_book)


def get_books_for_author() -> list[Book]:
    return [Book(title="Jurassic Park")]


@strawberry.type
class Author:
    name: str
    books: list[Book] = strawberry.field(resolver=get_books_for_author)


def get_authors() -> list[Author]:
    return [Author(name="Michael Crichton")]


@strawberry.type
class BookQuery:
    authors: list[Author] = strawberry.field(resolver=get_authors)
    books: list[Book] = strawberry.field(resolver=get_books_for_author)
