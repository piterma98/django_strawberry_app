import pytest


def test_query(graphql_client):
    query = """
        query TestQuery{
            books{
                title
                author{
                    name
                }
            }
        }
    """

    result = graphql_client.query(
        query=query,
    )

    assert result.errors is None
    assert result.data == {
        "books": [{"title": "Jurassic Park", "author": {"name": "Michael Crichton"}}],
    }


@pytest.mark.django_db
def test_me_query(user_factory, graphql_client):
    user = user_factory()
    query = """
        query User{
          user
        }
    """

    with graphql_client.login(user):
        result = graphql_client.query(
            query=query,
        )

    assert result.errors is None
    assert result.data == {"user": str(user)}


@pytest.mark.django_db
def test_authors_query(user_factory, graphql_client):
    user = user_factory()
    query = """
        query Authors{
                authors{
            name
            }
        }
    """

    with graphql_client.login(user):
        result = graphql_client.query(
            query=query,
        )

    assert result.errors is None
    assert result.data == {"authors": [{"name": "Michael Crichton"}]}


@pytest.mark.django_db
def test_authors_query_unauthorized(graphql_client):
    query = """
        query Authors{
                authors{
                    name
            }
        }
    """

    result = graphql_client.query(
        query=query,
        asserts_errors=False,
    )

    assert len(result.errors) == 1
