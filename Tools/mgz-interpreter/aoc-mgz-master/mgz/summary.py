"""MGZ Summary."""

import hashlib
import logging
import os
import struct

import construct
import mgz
import mgz.body


LOGGER = logging.getLogger(__name__)
SEARCH_MAX_BYTES = 3000
POSTGAME_LENGTH = 2096
LOOKAHEAD = 9
CHECKSUMS = 4


def find_postgame(data, size):
    """Find postgame struct.

    We can find postgame location by scanning the last few
    thousand bytes of the rec and looking for a pattern as
    follows:

    [action op]    [action length]    [action type]
    01 00 00 00    30 08 00 00        ff

    The last occurance of this pattern signals the start of
    the postgame structure. Note that the postgame action length
    is always constant, unlike other actions.
    """
    pos = None
    for i in range(size - SEARCH_MAX_BYTES, size - LOOKAHEAD):
        op_type, length, action_type = struct.unpack('<IIB', data[i:i + LOOKAHEAD])
        if op_type == 0x01 and length == POSTGAME_LENGTH and action_type == 0xFF:
            LOGGER.debug("found postgame candidate @ %d with length %d", i + LOOKAHEAD, length)
            return i + LOOKAHEAD, length


def parse_postgame(handle, size):
    """Parse postgame structure."""
    data = handle.read()
    postgame = find_postgame(data, size)
    if postgame:
        pos, length = postgame
        try:
            return mgz.body.actions.postgame.parse(data[pos:pos + length])
        except construct.core.ConstructError:
            raise IOError("failed to parse postgame")
    raise IOError("could not find postgame")


class Summary:
    """MGZ summary.

    Access metadata that in most cases can be found quickly.
    """

    def __init__(self, handle, size):
        """Initialize."""
        self._handle = handle
        try:
            self._header = mgz.header.parse_stream(handle)
        except (construct.core.ConstructError, ValueError):
            raise RuntimeError("invalid mgz file")
        self.body_position = self._handle.tell()
        self.size = size
        self.postgame = None
        self._teams = None
        self._resigned = set()

    def get_postgame(self):
        """Get postgame structure."""
        if self.postgame is not None:
            return self.postgame
        self._handle.seek(0)
        try:
            self.postgame = parse_postgame(self._handle, self.size)
            return self.postgame
        except IOError:
            self.postgame = False
            return None
        finally:
            self._handle.seek(self.body_position)

    def get_duration(self):
        """Get game duration."""
        postgame = self.get_postgame()
        if postgame:
            return postgame.duration_int * 1000
        duration = self._header.initial.restore_time
        while self._handle.tell() < self.size:
            operation = mgz.body.operation.parse_stream(self._handle)
            if operation.type == 'sync':
                duration += operation.time_increment
            elif operation.type == 'action':
                if operation.action.type == 'resign':
                    self._resigned.add(operation.action.player_id)
        self._handle.seek(self.body_position)
        return duration

    def get_restored(self):
        """Check for restored game."""
        return self._header.initial.restore_time > 0, self._header.initial.restore_time

    def get_version(self):
        """Get game version."""
        return mgz.const.VERSIONS[self._header.version], str(self._header.sub_version)[:5]

    def get_dataset(self):
        """Get dataset."""
        sample = self._header.initial.players[0].attributes.player_stats
        if 'mod' in sample and sample.mod['id'] > 0:
            return sample.mod
        elif 'trickle_food' in sample and sample.trickle_food:
            return {
                'id': 1,
                'name': mgz.const.MODS.get(1),
                'version': '<5.7.2'
            }
        return {
            'id': 0,
            'name': 'Age of Kings: The Conquerors',
            'version': '1.0c'
        }

    def get_owner(self):
        """Get rec owner (POV)."""
        return self._header.replay.rec_player

    def get_teams(self):
        """Get teams."""
        if self._teams:
            return self._teams
        teams = []
        for j, player in enumerate(self._header.initial.players):
            added = False
            for i in range(0, len(self._header.initial.players)):
                if player.attributes.my_diplomacy[i] == 'ally':
                    inner_team = False
                    outer_team = False
                    new_team = True
                    for t, tl in enumerate(teams):
                        if j in tl or i in tl:
                            new_team = False
                        if j in tl and i not in tl:
                            inner_team = t
                            break
                        if j not in tl and i in tl:
                            outer_team = t
                            break
                    if new_team:
                        teams.append([i, j])
                    if inner_team is not False:
                        teams[inner_team].append(i)
                    if outer_team is not False:
                        teams[outer_team].append(j)
                    added = True
            if not added and j != 0:
                teams.append([j])
        self._teams = teams
        return teams

    def get_diplomacy(self):
        """Compute diplomacy."""
        if not self._teams:
            self.get_teams()

        player_num = 0
        computer_num = 0
        for player in self._header.scenario.game_settings.player_info:
            if player.type == 'human':
                player_num += 1
            elif player.type == 'computer':
                computer_num += 1
        total_num = player_num + computer_num

        diplomacy = {
            'FFA': (len(self._teams) == total_num) and total_num > 2,
            'TG':  len(self._teams) == 2 and total_num > 2,
            '1v1': total_num == 2,
        }

        diplomacy['type'] = 'unknown'
        if diplomacy['FFA']:
            diplomacy['type'] = 'FFA'
        if diplomacy['TG']:
            diplomacy['type'] = 'TG'
            size = len(self._teams[0])
            diplomacy['team_size'] = '{}v{}'.format(size, size)
        if diplomacy['1v1']:
            diplomacy['type'] = '1v1'
            diplomacy['team_size'] = '1v1'
        return diplomacy

    def get_achievements(self, name):
        """Get achievements for a player.

        Must match on name, not index, since order is not always the same.
        """
        postgame = self.get_postgame()
        if not postgame:
            return None
        for achievements in postgame.achievements:
            if name == achievements.player_name:
                return achievements
        return None

    def get_players(self):
        """Get basic player info."""
        for i, player in enumerate(self._header.initial.players[1:]):
            achievements = self.get_achievements(player.attributes.player_name)
            if achievements:
                winner = achievements.victory
            else:
                winner = self.guess_winner(i + 1)
            yield {
                'name': player.attributes.player_name,
                'civilization': player.attributes.civilization,
                'human': self._header.scenario.game_settings.player_info[i + 1].type == 'human',
                'number': i + 1,
                'color_id': player.attributes.player_color,
                'winner': winner,
                'mvp': achievements.mvp if achievements else None,
                'score': achievements.total_score if achievements else None,
                'position': (player.attributes.camera_x, player.attributes.camera_y)
            }

    def get_ladder(self):
        """Get Voobly ladder.

        This is expensive if the rec is not from Voobly,
        since it will search the whole file. Returns tuple,
        (from_voobly, ladder_name).
        """
        ladder = None
        voobly = False
        ratings = set()
        while self._handle.tell() < self.size:
            try:
                op = mgz.body.operation.parse_stream(self._handle)
                if op.type == 'message' and op.subtype == 'chat':
                    if op.data.text.find('Voobly: Ratings provided') > 0:
                        start = op.data.text.find("'") + 1
                        end = op.data.text.find("'", start)
                        ladder = op.data.text[start:end]
                        voobly = True
                    elif op.data.text.find('<Rating>') > 0:
                        line = op.data.text
                        player_start = line.find('>') + 2
                        player_end = line.find(':', player_start)
                        ratings.add(int(line[player_end + 2:len(line)]))
                    elif op.data.text.find('No ratings are available') > 0:
                        voobly = True
                        break
                    elif op.data.text.find('This match was played at Voobly.com') > 0:
                        voobly = True
                        break
            except (construct.core.ConstructError, ValueError):
                break
        self._handle.seek(self.body_position)
        return voobly, ladder, len(ratings) > 0 and ratings != {1600}

    def get_settings(self):
        """Get settings."""
        return {
            'type': self._header.lobby.game_type,
            'difficulty': self._header.scenario.game_settings.difficulty,
            'population_limit': self._header.lobby.population_limit * 25,
            'reveal_map': self._header.lobby.reveal_map,
            'speed': mgz.const.SPEEDS.get(self._header.replay.game_speed),
            'cheats': self._header.replay.cheats_enabled,
            'lock_teams': self._header.lobby.lock_teams
        }

    def get_hash(self):
        """Compute match hash.

        Use the first three synchronization checksums
        as a unique identifier for the match.
        """
        self._handle.seek(self.body_position)
        checksums = []
        while self._handle.tell() < self.size and len(checksums) < CHECKSUMS:
            op = mgz.body.operation.parse_stream(self._handle)
            if op.type == 'sync' and op.checksum is not None:
                checksums.append(op.checksum.sync.to_bytes(8, 'big', signed=True))
        return hashlib.sha1(b''.join(checksums))

    def get_map(self):
        """Get the map name.

        TODO: Search all language strings.
        """
        map_id = self._header.scenario.game_settings.map_id
        instructions = self._header.scenario.messages.instructions
        size = mgz.const.MAP_SIZES[self._header.map_info.size_x]
        if map_id in mgz.const.MAP_NAMES:
            return mgz.const.MAP_NAMES[map_id], size
        else:
            name = 'Unknown'
            line = instructions.split('\n')[2]
            if line.find(':') > 0:
                name = line.split(":")[1].strip()
            elif line.find('\xa1\x47') > 0:
                name = line.split('\xa1\x47')[1].strip()
            elif line.find("\xa3\xba") > 0:
                name = line.split('\xa3\xba')[1].strip()
            name = name.strip()
            # Special case for maps (prefixed with language-specific name,
            # real map name in parentheses.
            if name.find(' (') > 0:
                name = name.split(' (')[1][:-1]
            return name, size

    def get_completed(self):
        """Determine if the game was completed.

        If there's a postgame, it will indicate completion.
        If there is no postgame, guess based on resignation.
        """
        postgame = self.get_postgame()
        if postgame:
            return postgame.complete
        else:
            return True if self._resigned else False

    def get_mirror(self):
        """Determine mirror match."""
        mirror = False
        if self.get_diplomacy()['1v1']:
            civs = set()
            for data in self.get_players():
                civs.add(data['civilization'])
            mirror = (len(civs) == 1)
        return mirror

    def guess_winner(self, i):
        """Guess if a player won.

        Find what team the player was on. If anyone
        on their team resigned, assume the player lost.
        """
        for team in self.get_teams():
            if i not in team:
                continue
            for p in team:
                if p in self._resigned:
                    return False
        return True
