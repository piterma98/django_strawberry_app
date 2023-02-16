import pytest


def test_query(graphql_client) -> None:
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
        query,
    )

    assert result.errors is None
    assert result.data == {
        "books": [{"title": "Jurassic Park", "author": {"name": "Michael Crichton"}}]
    }


@pytest.mark.django_db
def test_me_query(user_factory, graphql_client) -> None:
    user = user_factory()
    query = """
        query User{
          user
        }
    """

    graphql_client.client.force_login(user)
    result = graphql_client.query(
        query=query,
    )

    assert result.errors is None
    assert result.data == {"user": str(user)}
