"""Contains the NHL Stats API Client class"""
from typing import Dict, List
import requests

class Client:
  """Manages connections and requests to the NHL stats API.

  Example usage:
    from nhlpy.stats.client import Client
    stats_client = Client()
    res = client.get_conferences()
  """
  def __init__(self):
    self.base_url = 'https://statsapi.web.nhl.com/api/v1/'

  def get_conferences(self, conference_id: str = None) -> dict:
    """Gets conferences in the NHL.

    Args:
      conference_id: The ID of the conference to retrieve. If not specified,
        retrieves information for all conferences.

    Returns:
      A dictionary containing the JSON response from the API request.
    """
    url = self.base_url + 'conferences'
    if conference_id:
      url = url + f'/{conference_id}'

    return self._get_response_json(url)

  def get_divisions(self, division_id: str = None) -> dict:
    """Gets divisions in the NHL.

    Args:
      division_id: The ID of the division to retrieve. If not specified,
        retrieves information for all divisions.

    Returns:
      A dictionary containing the JSON response from the API request.
    """
    url = self.base_url + 'divisions'
    if division_id:
      url = url + f'/{division_id}'

    return self._get_response_json(url)

  def get_draft(self, year: str = None) -> dict:
    """Gets NHL draft information.

    Args:
      year: """
    raise NotImplementedError

  def get_franchises(self, franchise_id: str = None) -> dict:
    """Gets franchises in the NHL.

    Args:
      franchise_id: Specifies the franchise to return. If not specified,
        retrieves information for all franchises.

    Returns:
      A dictionary containing the JSON response from the API request.
    """
    url = self.base_url + 'franchises'
    if franchise_id:
      url = url + f'/{franchise_id}'

    return self._get_response_json(url)

  def get_player(self, player_id: str) -> dict:
    """Gets player information.

    You can retrieve the player ID by calling get_team_roster()

    Args:
      player_id: The ID of the player to query.
      include_stats: Includes the player's stats.

    Returns:
      A dict containing general player information.
    """
    url = self.base_url + f'people/{player_id}'
    return self._get_response_json(url)

  def get_player_stats(self, player_id: str) -> dict:
    """Gets basic aggregated player stats for the specified player.

    Args:
      player_id: The ID of the player to query.

    Returns:
      A dict containing the aggregated player stats for the specified player.
    """
    url = self.base_url + f'people/{player_id}/stats'
    return self._get_response_json(url)

  def get_player_stats_for_season(self, player_id: str, season: str) -> dict:
    """Gets player stats for a single season.

    Args:
      player_id: The ID of the player to query.
      season: The ID of the NHL season. For the 2021-2022 season, this would be
        20212022.

    Returns:
      A dict containing single season stats for the specified player.
    """
    url = self.base_url + f'people/{player_id}/stats'
    params = {
      'stats': 'statsSingleSeason',
      'season': season
    }
    self._get_response_json(url, params=params)

  def get_player_stats_year_by_year(self, player_id: str) -> dict:
    """Gets a player's stats for each year of their career.

    Args:
      player_id: The ID of the player to query.

    Returns:
      A dict containing year-by-year stats for a player's career.
    """
    url = self.base_url + f'people/{player_id}/stats'
    params = {'stats': 'yearByYear'}
    return self._get_response_json(url, params=params)

  def get_teams(
    self, team_ids: List[str] = None, show_roster: bool = False,
    show_expanded_roster: bool = False, show_upcoming_game: bool = False,
    show_previous_game: bool = False, show_stats: bool = False,
    season: str = None, specific_stats: List[str] = None
  ) -> dict:
    """Gets NHL team information.

    Args:
      team_ids:
      show_roster:
      show_expanded_roster:
      show_upcoming_game:
      show_previous_game:
      show_stats:
      season:
      specific_stats:

    Returns:
      A dictionary containing the JSON response from the request.
    """
    url = self.base_url + 'teams'

    expand_opts = [show_roster, show_expanded_roster, show_upcoming_game,
                   show_previous_game, show_stats]

    expand_param = ','.join(filter(None, expand_opts))
    stats_param = ','.join(filter(None, specific_stats))

    params = {}
    if expand_param:
      params['expand'] = expand_param
    if stats_param:
      params['stats'] = stats_param
    if season:
      params['season'] = season

    if team_ids:
      if len(team_ids) > 1:
        params['teamId'] = team_ids
      else:
        url = url + f'/{team_ids[0]}'

    return self._get_response_json(url, params)

  def get_team_roster(self, team_id: str) -> dict:
    """Gets the roster for a team.

    Args:
      team_id: The ID of the team to query.

    Returns:
      A dictionary with a list of players on the team.
    """
    url = self.base_url + f'teams/{team_id}/roster'
    return self._get_response_json(url)

  def _get_response_json(self, url: str, params: Dict[str, str] = None) -> dict:
    """Makes a get request to the specified URL and returns the JSON response

    Args:
      url: The endpoint to make a request to.
      params: Optional request parameters

    Returns:
      A dict containing the JSON response.
    """
    return requests.get(url, params=params).json()
