import requests
from config import GRAPHQL_URL, HASURA_PUBLIC_SECRET_KEY


def run_query(query, variables=None):

    headers = {
        "x-hasura-public-secret-key": HASURA_PUBLIC_SECRET_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        GRAPHQL_URL,
        json={
            "query": query,
            "variables": variables or {}
        },
        headers=headers
    )

    response.raise_for_status()

    return response.json()