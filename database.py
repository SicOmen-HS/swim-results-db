import psycopg2
from config import DB


def get_connection():
    return psycopg2.connect(
        host=DB["host"],
        port=DB["port"],
        dbname=DB["dbname"],
        user=DB["user"],
        password=DB["password"]
    )


def save_results(results):

    conn = get_connection()
    cursor = conn.cursor()

    for row in results:

        # Spara tävling
        cursor.execute(
            """
            INSERT INTO competitions (
                id,
                name,
                city,
                competition_date
            )
            VALUES (%s, %s, %s, %s)

            ON CONFLICT(id)
            DO NOTHING
            """,
            (
                row["competition_id"],
                row["competition_name"],
                row["competition_city"],
                row.get("competition_date")
            )
        )

        # Spara lopp/event
        cursor.execute(
            """
            INSERT INTO events (
                competition_id,
                event_number,
                event_name
            )
            VALUES (%s, %s, %s)

            ON CONFLICT(
                competition_id,
                event_number,
                event_name
            )
            DO NOTHING
            """,
            (
                row["competition_id"],
                row["event_number"],
                row["event_name"]
            )
        )

        # Hämta event-id
        cursor.execute(
            """
            SELECT id
            FROM events
            WHERE
                competition_id=%s
                AND event_number=%s
                AND event_name=%s
            """,
            (
                row["competition_id"],
                row["event_number"],
                row["event_name"]
            )
        )

        event_id = cursor.fetchone()[0]

        # Spara klubb
        cursor.execute(
            """
            INSERT INTO clubs (
                id,
                name
            )
            VALUES (%s, %s)

            ON CONFLICT(id)
            DO NOTHING
            """,
            (
                row["club_id"],
                row["club_name"]
            )
        )

        # Spara simmare
        cursor.execute(
            """
            INSERT INTO competitors (
                id,
                name,
                club_id
            )
            VALUES (%s, %s, %s)

            ON CONFLICT(id)
            DO NOTHING
            """,
            (
                row["competitor_id"],
                row["competitor_name"],
                row["club_id"]
            )
        )

        # Spara resultat
        cursor.execute(
            """
            INSERT INTO results (
                event_id,
                competitor_id,
                result_text,
                result_value
            )
            VALUES (%s, %s, %s, %s)

            ON CONFLICT(
                event_id,
                competitor_id
            )
            DO NOTHING
            """,
            (
                event_id,
                row["competitor_id"],
                row["time"],
                row["time_value"]
            )
        )

    conn.commit()

    cursor.close()
    conn.close()