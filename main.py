from scraper import get_competition_results
from database import save_results


def import_competition(competition_id):

    results = get_competition_results(
        competition_id
    )

    save_results(results)

    print(
        f"Sparade {len(results)} resultat"
    )


if __name__ == "__main__":

    competition_id = input(
        "Ange competition id: "
    )

    import_competition(
        competition_id
    )