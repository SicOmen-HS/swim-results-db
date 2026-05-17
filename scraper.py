from graphql_client import run_query


def get_competition_info(competition_id):
    query = """
    query GetCompetition($id: uuid!) {
      competitions_by_pk(id: $id) {
        id
        name
        city
        competitionDate: startDate
      }
    }
    """

    result = run_query(query, {"id": competition_id})

    return result["data"]["competitions_by_pk"]


def get_competition_results(competition_id):

    competition = get_competition_info(competition_id)

    events_query = """
    query GetEvents($competition_id: uuid!) {
      time_program_entry(
        where: {
          round: {
            event: {
              competition_id: {
                _eq: $competition_id
              }
            }
          }
        }
        order_by: { oid: asc }
      ) {
        round {
          event {
            number
            name
          }
          summary_types {
            id
            name
          }
        }
      }
    }
    """

    results_query = """
    query GetResults($id: Int!) {
      summary_type_by_pk(id: $id) {
        ranks {
          lane {
            result_text
            result_value
            dns
            dsq
            dnf
            competitor {
              id
              full_name
              club {
                id
                short_name
              }
            }
          }
        }
      }
    }
    """

    all_results = []

    events_result = run_query(
        events_query,
        {"competition_id": competition_id}
    )

    events = events_result["data"]["time_program_entry"]

    for event_entry in events:

        event = event_entry["round"]["event"]

        total_summary = next(
            (
                summary
                for summary in event_entry["round"]["summary_types"]
                if summary["name"] == "Total"
            ),
            None
        )

        if total_summary is None:
            continue

        result = run_query(
            results_query,
            {"id": total_summary["id"]}
        )

        ranks = result["data"]["summary_type_by_pk"]["ranks"]

        for rank in ranks:
            lane = rank["lane"]

            if (
                lane["dns"]
                or lane["dsq"]
                or lane["dnf"]
                or lane["result_value"] == 0
            ):
                continue

            competitor = lane["competitor"]

            all_results.append({
                "competition_id": competition["id"],
                "competition_name": competition["name"],
                "competition_city": competition["city"],
                "competition_date": competition["competitionDate"],

                "event_number": event["number"],
                "event_name": event["name"],

                "competitor_id": competitor["id"],
                "competitor_name": competitor["full_name"],

                "club_id": competitor["club"]["id"],
                "club_name": competitor["club"]["short_name"],

                "time": lane["result_text"],
                "time_value": lane["result_value"]
            })

    all_results.sort(
        key=lambda row: (
            row["event_number"],
            row["time_value"]
        )
    )

    return all_results