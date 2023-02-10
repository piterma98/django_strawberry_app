from application.graphql_api import schema


def test_query():
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

    result = schema.execute_sync(
        query,
    )

    assert result.errors is None
    assert result.data == {
        "books": [{"title": "Jurassic Park", "author": {"name": "Michael Crichton"}}]
    }
