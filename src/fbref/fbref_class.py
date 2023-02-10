"""FBref class used to fetch data from https://fbref.com/en/"""

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.fbref.etl.clean import (
    clean_defense_table,
    clean_fixtures_df,
    clean_home_away_league_table,
    clean_league_table_df,
    clean_player_stat_table,
    clean_possession_table,
)

competition_dict = {
    "9": "Premier-League",
    "12": "La-Liga",
    "11": "Serie-A",
    "13": "Ligue-1",
    "20": "Bundesliga",
}


class FBref:
    def instantiate_beautiful_soup_object(self, input_url):
        """Function used to create BeautifulSoup object to be used to extract information from URL"""
        html_request = requests.get(input_url)
        beautifulsoup_object = BeautifulSoup(html_request.content, "html.parser")
        return beautifulsoup_object

    def get_html_table_ids(self, input_url):
        """Function used to give a dictionary that contains the names of each table for a given URL"""
        # instantiate beautiful soup
        beautifulsoup_object = self.instantiate_beautiful_soup_object(input_url)
        # get table list
        html_table_list = beautifulsoup_object.find_all("table")
        # get table id list
        table_id_list = []

        for table in html_table_list:
            try:
                table_id_list.append(table["id"])
            except KeyError:
                pass

        return table_id_list

    def get_column_names(self, html_table):
        """Function used to get column names for tables scraped online"""
        headers = html_table.find("thead")

        over_headers = headers.find("tr", class_="over_header")

        if over_headers is None:
            no_over_headers = 0
        else:
            over_headers = over_headers.find_all("th")
            no_over_headers = len(over_headers)

        table_headers = headers.find_all("th", scope="col")
        table_headers_text = [header.text for header in table_headers]
        no_table_headers = len(table_headers_text)

        if no_over_headers > 0:
            over_headers_text = []
            for header in over_headers:
                if "colspan" in header.attrs.keys():  # if statement for cases I ran into
                    for times in range(int(header["colspan"])):
                        over_headers_text.append(header.text)
                else:
                    over_headers_text.append(header.text)

            full_header_names = [over_headers_text[i] + " " + table_headers_text[i] for i in range(no_table_headers)]
            full_header_names = [header.strip() for header in full_header_names]
        else:
            full_header_names = table_headers_text
        return full_header_names

    def get_html_table(self, table_id, input_url):
        """Function used to grab html code for specified table"""
        # grab html of data
        beautifulsoup_object = self.instantiate_beautiful_soup_object(input_url)
        html_table = beautifulsoup_object.find(id=table_id)
        return html_table

    def get_fbref_df(self, fbref_html_table, expected_attribute_no=None):
        """Function used to grab df for given table from FBref"""
        fb_table_headers = self.get_column_names(fbref_html_table)
        fb_table_body = fbref_html_table.find("tbody")

        fb_table_rows = fb_table_body.find_all("tr")

        if expected_attribute_no is not None:
            fb_table_rows = self.get_rid_of_dividers(fb_table_rows, expected_attribute_no)

        fb_table_rows_list = []

        for fb_table_row in fb_table_rows:

            # main data
            row_data = [data_cell.text for data_cell in fb_table_row]

            fb_table_rows_list.append(row_data)

        fb_table_df = pd.DataFrame(data=fb_table_rows_list, columns=fb_table_headers)
        return fb_table_df

    def get_rid_of_dividers(self, data_rows_list, expected_attribute_no):
        """Function used to get rid of html divider rows"""
        # to get rid of divider rows
        data_rows = [row for row in data_rows_list if len(row.attrs) == expected_attribute_no]
        return data_rows

    def get_big_5_leagues(self):
        """Function used to grab data about Europe's top 5 leagues"""
        big5_table_html = self.get_html_table("comps_club", "https://fbref.com/en/comps/")
        big5_headers = self.get_column_names(big5_table_html)
        big5_headers = big5_headers + ["competition_link", "competition_id"]

        big5_table_body = big5_table_html.find("tbody")

        big5_rows = big5_table_body.find_all("tr")

        big5_rows_list = []
        for big5_row in big5_rows:
            # main data
            row_data = [data_cell.text for data_cell in big5_row]
            # additional columns of interest
            competition_link = "https://fbref.com" + big5_row.find(attrs={"data-stat": "league_name"}).a["href"]
            competition_id = competition_link.split("/")[5]

            row_data += [competition_link]
            row_data += [competition_id]
            big5_rows_list.append(row_data)

        big5_table_df = pd.DataFrame(data=big5_rows_list, columns=big5_headers)
        return big5_table_df

    def get_competition_dict(self):
        """Function used to return a dictionary for competition id to competition name"""
        return competition_dict

    def get_teams_per_country(self, country):
        """Function used to output football clubs per country"""
        team_country_dict = {
            "England": "https://fbref.com/en/country/clubs/ENG/England-Football-teams",
            "France": "https://fbref.com/en/country/clubs/FRA/France-Football-teams",
            "Germany": "https://fbref.com/en/country/clubs/GER/Germany-Football-teams",
            "Italy": "https://fbref.com/en/country/clubs/ITA/Italy-Football-teams",
            "Spain": "https://fbref.com/en/country/clubs/ESP/Spain-Football-teams",
        }

        team_country_link = team_country_dict[country]

        team_html_table = self.get_html_table("clubs", team_country_link)
        team_headers = self.get_column_names(team_html_table)
        team_headers += ["team_link", "team_id"]

        team_body = team_html_table.find("tbody")
        team_rows = team_body.find_all("tr")

        team_rows = self.get_rid_of_dividers(data_rows_list=team_rows, expected_attribute_no=0)

        team_rows_list = []

        for team_row in team_rows:

            # main data
            row_data = [data_cell.text for data_cell in team_row]

            # additional columns of interest
            try:
                team_link = team_row.find("a")["href"]  # note here team link doesn't have specific tag to search
                if "squads" in team_link:
                    full_team_link = "https://fbref.com" + team_link
                    team_id = full_team_link.split("/")[5]
                else:
                    team_link = np.nan
                    team_id = np.nan
            except TypeError:
                team_link = np.nan
                team_id = np.nan

            row_data += [full_team_link]
            row_data += [team_id]
            team_rows_list.append(row_data)

        team_df = pd.DataFrame(data=team_rows_list, columns=team_headers)

        return team_df

    def get_competition_seasons(self, competition_link):
        """"""
        competition_seasons_html = self.get_html_table("seasons", competition_link)
        competition_seasons_headers = self.get_column_names(competition_seasons_html)

        competition_seasons_body = competition_seasons_html.find("tbody")
        competition_seasons_rows = competition_seasons_body.find_all("tr")

        competition_seasons_rows_list = []
        for competition_seasons_row in competition_seasons_rows:
            row_data = [data_cell.text for data_cell in competition_seasons_row]
            competition_seasons_rows_list.append(row_data)
        competition_seasons_df = pd.DataFrame(data=competition_seasons_rows_list, columns=competition_seasons_headers)
        return competition_seasons_df

    def get_fixtures_and_results(self, competition_id, season_name):
        """Function used to grab fixtures and results for a given competition and season"""
        competition_name = competition_dict[str(competition_id)]

        fixtures_html = self.instantiate_beautiful_soup_object(
            f"https://fbref.com/en/comps/{competition_id}/{season_name}/schedule/"
            + f"{season_name}-{competition_name}-Scores-and-Fixtures"
        )

        fixtures_html_table = fixtures_html.find(id=f"sched_{season_name}_{competition_id}_1")
        fixtures_headers = self.get_column_names(fixtures_html_table)
        fixtures_headers += ["home_team_id", "away_team_id", "fixture_link"]

        fixtures_body = fixtures_html_table.find("tbody")

        fixtures_rows = fixtures_body.find_all("tr")

        fixtures_rows = self.get_rid_of_dividers(data_rows_list=fixtures_rows, expected_attribute_no=0)

        fixtures_rows_list = []

        for fixtures_row in fixtures_rows:

            # main data
            row_data = [data_cell.text for data_cell in fixtures_row]

            # additional columns of interest
            # fixture link
            try:
                fixture_link = "https://fbref.com" + fixtures_row.find(attrs={"data-stat": "match_report"}).a["href"]
            except TypeError:
                fixture_link = np.nan
            # home id
            home_id = fixtures_row.find(attrs={"data-stat": "home_team"}).a["href"].split("/")[3]
            # away id
            away_id = fixtures_row.find(attrs={"data-stat": "away_team"}).a["href"].split("/")[3]

            row_data += [home_id]
            row_data += [away_id]
            row_data += [fixture_link]

            fixtures_rows_list.append(row_data)

        fixtures_df = pd.DataFrame(data=fixtures_rows_list, columns=fixtures_headers)
        cleaned_fixtures_df = clean_fixtures_df(fixtures_df)
        cleaned_fixtures_df["season_name"] = season_name.replace("-", "_")
        cleaned_fixtures_df["competition_id"] = competition_id
        return cleaned_fixtures_df

    def get_fixture_stats(self, fixture_url, team_id, stat_type):
        """Function used to grab stats for a specified team. ie"""

        if stat_type == "summary":
            table_id = f"stats_{team_id}_summary"
            fixture_stat_df = self.get_fixture_stat_df(table_id, fixture_url)
        elif stat_type == "passing":
            table_id = f"stats_{team_id}_passing"
            fixture_stat_df = self.get_fixture_stat_df(table_id, fixture_url)
        elif stat_type == "passing_types":
            table_id = f"stats_{team_id}_passing_types"
            fixture_stat_df = self.get_fixture_stat_df(table_id, fixture_url)
        elif stat_type == "defense":
            table_id = f"stats_{team_id}_defense"
            fixture_stat_df = self.get_fixture_stat_df(table_id, fixture_url)
        elif stat_type == "possession":
            table_id = f"stats_{team_id}_possession"
            fixture_stat_df = self.get_fixture_stat_df(table_id, fixture_url)
        elif stat_type == "misc":
            table_id = f"stats_{team_id}_misc"
            fixture_stat_df = self.get_fixture_stat_df(table_id, fixture_url)
        elif stat_type == "keeper":
            table_id = f"keeper_stats_{team_id}"
            fixture_stat_df = self.get_fixture_stat_df(table_id, fixture_url)
        elif stat_type == "shots":
            table_id = f"shots_{team_id}"
            fixture_stat_df = self.get_fixture_shots_df(table_id, fixture_url)
        else:
            raise Exception("stat_type input invalid.")

        return fixture_stat_df

    def get_fixture_stat_df(self, table_id, fixture_url):
        """Function used to grab dataframe for stats from a given fixture url"""
        fixture_stat_html = self.get_html_table(table_id, fixture_url)
        fixture_stat_headers = self.get_column_names(fixture_stat_html)

        fixture_stat_body = fixture_stat_html.find("tbody")

        fixture_stat_rows = fixture_stat_body.find_all("tr")

        fixture_stat_rows_list = []
        for fixture_stat_row in fixture_stat_rows:
            # main data
            row_data = [data_cell.text for data_cell in fixture_stat_row]
            fixture_stat_rows_list.append(row_data)

        fixture_stat_df = pd.DataFrame(data=fixture_stat_rows_list, columns=fixture_stat_headers)
        return fixture_stat_df

    def get_fixture_shots_df(self, table_id, fixture_url):
        """Function used to grab dataframe for shots from a given fixture url"""
        fixture_shots_html = self.get_html_table(table_id, fixture_url)
        fixture_shots_headers = self.get_column_names(fixture_shots_html)

        fixture_shots_body = fixture_shots_html.find("tbody")

        fixture_shots_rows = fixture_shots_body.find_all("tr")

        fixture_shots_rows = self.get_rid_of_dividers(data_rows_list=fixture_shots_rows, expected_attribute_no=1)

        fixture_shots_rows_list = []
        for fixture_shots_row in fixture_shots_rows:
            # main data
            row_data = [data_cell.text for data_cell in fixture_shots_row]
            fixture_shots_rows_list.append(row_data)

        fixture_shots_df = pd.DataFrame(data=fixture_shots_rows_list, columns=fixture_shots_headers)
        return fixture_shots_df

    def get_season_stats_table(self, table_type, competition_id, season_name):
        """Function used to grab league table for given competition and season"""
        competition_name = competition_dict[str(competition_id)]

        season_stats_html = self.instantiate_beautiful_soup_object(
            f"https://fbref.com/en/comps/{competition_id}/{season_name}/{season_name}-{competition_name}-Stats"
        )
        if table_type == "league_table":
            season_table = season_stats_html.find(id=f"results{season_name}{competition_id}1_overall")
            season_df = self.get_fbref_df(season_table)
            cleaned_season_df = clean_league_table_df(season_df)
        elif table_type == "home_away_league_table":
            season_table = season_stats_html.find(id=f"results{season_name}{competition_id}1_home_away")
            season_df = self.get_fbref_df(season_table)
            cleaned_season_df = clean_home_away_league_table(season_df)
        elif table_type == "defense_table":
            season_table = season_stats_html.find(id="stats_squads_defense_for")
            season_df = self.get_fbref_df(season_table)
            cleaned_season_df = clean_defense_table(season_df)
        elif table_type == "possession_table":
            season_table = season_stats_html.find(id="stats_squads_possession_for")
            season_df = self.get_fbref_df(season_table)
            cleaned_season_df = season_df
            cleaned_season_df = clean_possession_table(season_df)

        else:
            raise Exception("Input table_type invalid.")

        cleaned_season_df["competition_id"] = competition_id
        cleaned_season_df["season_name"] = season_name.replace("-", "_")

        return cleaned_season_df

    def get_big5_player_stats(self, table_type, season_name):
        """Function used to grab player data from the big 5 leagues"""

        if table_type == "standard":
            big5_url = (
                f"https://fbref.com/en/comps/Big5/{season_name}/stats/players/"
                + f"{season_name}-Big-5-European-Leagues-Stats"
            )
            big5_table_html = self.get_html_table("stats_standard", big5_url)
            big5_df = self.get_fbref_df(big5_table_html, expected_attribute_no=0)
            big5_df = clean_player_stat_table(big5_df, table_type)
        elif table_type == "passing":
            big5_url = (
                f"https://fbref.com/en/comps/Big5/{season_name}/{table_type}/players/"
                + f"{season_name}-Big-5-European-Leagues-Stats"
            )
            big5_table_html = self.get_html_table("stats_passing", big5_url)
            big5_df = self.get_fbref_df(big5_table_html, expected_attribute_no=0)
            big5_df = clean_player_stat_table(big5_df, table_type)
        elif table_type == "defense":
            big5_url = (
                f"https://fbref.com/en/comps/Big5/{season_name}/{table_type}/players/"
                + f"{season_name}-Big-5-European-Leagues-Stats"
            )
            big5_table_html = self.get_html_table("stats_defense", big5_url)
            big5_df = self.get_fbref_df(big5_table_html, expected_attribute_no=0)
            big5_df = clean_player_stat_table(big5_df, table_type)
        elif table_type == "possession":
            big5_url = (
                f"https://fbref.com/en/comps/Big5/{season_name}/{table_type}/players/"
                + f"{season_name}-Big-5-European-Leagues-Stats"
            )
            big5_table_html = self.get_html_table("stats_possession", big5_url)
            big5_df = self.get_fbref_df(big5_table_html, expected_attribute_no=0)
            big5_df = clean_player_stat_table(big5_df, table_type)
        elif table_type == "shooting":
            big5_url = (
                f"https://fbref.com/en/comps/Big5/{season_name}/{table_type}/players/"
                + f"{season_name}-Big-5-European-Leagues-Stats"
            )
            big5_table_html = self.get_html_table("stats_shooting", big5_url)
            big5_df = self.get_fbref_df(big5_table_html, expected_attribute_no=0)
            big5_df = clean_player_stat_table(big5_df, table_type)
        elif table_type == "miscellaneous":
            big5_url = (
                f"https://fbref.com/en/comps/Big5/{season_name}/misc/players/"
                + f"{season_name}-Big-5-European-Leagues-Stats"
            )
            big5_table_html = self.get_html_table("stats_misc", big5_url)
            big5_df = self.get_fbref_df(big5_table_html, expected_attribute_no=0)
            big5_df = clean_player_stat_table(big5_df, table_type)
        else:
            raise Exception("Input table_type invalid.")
        big5_df["season_name"] = season_name
        return big5_df
