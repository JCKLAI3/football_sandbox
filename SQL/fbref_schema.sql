-- Drop Tables --------------------------------------------

DROP TABLE IF EXISTS fbref.fixtures;
DROP TABLE IF EXISTS fbref.competition_seasons;
DROP TABLE IF EXISTS fbref.competitions;
DROP TABLE IF EXISTS fbref.teams;
DROP TABLE IF EXISTS fbref.country;
DROP TABLE IF EXISTS fbref.seasons;


-- Create Tables --------------------------------------------

-- Seasons table
CREATE TABLE IF NOT EXISTS fbref.seasons (
    season_id SMALLINT NOT NULL,
    season_name VARCHAR(9),
    PRIMARY KEY(season_id)
);

CREATE INDEX idx_seasons_season_id ON fbref.seasons(season_id);

CREATE INDEX idx_seasons_season_name ON fbref.seasons(season_name);


-- Country table
CREATE TABLE IF NOT EXISTS fbref.country (
    country_id SERIAL NOT NULL,
    country_code VARCHAR(3),
    PRIMARY KEY(country_id)
);

CREATE INDEX idx_country_country_id ON fbref.country(country_id);
CREATE INDEX idx_country_country_code ON fbref.country(country_code);

-- Teams table
CREATE TABLE IF NOT EXISTS fbref.teams (
    team_id SMALLINT NOT NULL,
    gender VARCHAR(1),
    team_name VARCHAR(70),
    team_fb_ref_id VARCHAR(10) UNIQUE NOT NULL,
    PRIMARY KEY(team_id)
    
);

CREATE INDEX idx_teams_team_id ON fbref.teams(team_id);
CREATE INDEX idx_team_fb_ref_id ON fbref.teams(team_fb_ref_id);
CREATE INDEX idx_team_team_name ON fbref.teams(team_name);

-- Competitions table
CREATE TABLE IF NOT EXISTS fbref.competitions (
    competition_id SMALLINT NOT NULL,
    country_id SMALLINT,
    gender VARCHAR(1),
    competition_name VARCHAR(70),
    competition_link VARCHAR(100),
    competition_fb_ref_id VARCHAR(5) UNIQUE NOT NULL, 
    PRIMARY KEY(competition_id),
    CONSTRAINT fk_competitions_country_id_country
        FOREIGN KEY(country_id) 
            REFERENCES fbref.country(country_id)
);

CREATE INDEX idx_competitions_competition_id ON fbref.competitions(competition_id);
CREATE INDEX idx_competitions_country_id ON fbref.competitions(country_id);
CREATE INDEX idx_competitions_competition_name ON fbref.competitions(competition_name);
CREATE INDEX idx_competitions_competition_fb_ref_id ON fbref.competitions(competition_fb_ref_id);

-- Competition seasons table
CREATE TABLE IF NOT EXISTS fbref.competition_seasons (
    competition_seasons_id INT NOT NULL,
    season_id SMALLINT,
    competition_id SMALLINT,
    PRIMARY KEY(competition_seasons_id),
    CONSTRAINT fk_competition_seasons_season_id_competitions 
        FOREIGN KEY(season_id) 
            REFERENCES fbref.seasons(season_id),
    CONSTRAINT fk_competition_seasons_competition_id_competitions 
        FOREIGN KEY(competition_id) 
            REFERENCES fbref.competitions(competition_id)

);

CREATE INDEX idx_competition_seasons_competition_seasons_id ON fbref.competition_seasons(competition_seasons_id);
CREATE INDEX idx_competition_seasons_season_id ON fbref.competition_seasons(season_id);
CREATE INDEX idx_competition_seasons_competition_id ON fbref.competition_seasons(competition_id);

-- Fixtures table
CREATE TABLE IF NOT EXISTS fbref.fixtures (
    fixture_id SERIAL NOT NULL,
    competition_seasons_id INT, 
    kickoff TIMESTAMP,
    home_team_id SMALLINT,
    home_score SMALLINT,
    away_score SMALLINT,
    away_team_id SMALLINT, 
    fixture_link VARCHAR(150),
    fixture_fb_ref_id VARCHAR(8) NOT NULL, 
    PRIMARY KEY(fixture_id),
    CONSTRAINT fk_fixtures_competition_seaons_id_competitions_seaons
        FOREIGN KEY(competition_seasons_id) 
            REFERENCES fbref.competition_seasons(competition_seasons_id),
    CONSTRAINT fk_fixtures_home_team_id_teams
        FOREIGN KEY(home_team_id) 
            REFERENCES fbref.teams(team_id),
    CONSTRAINT fk_fixtures_away_team_id_teams
        FOREIGN KEY(away_team_id) 
            REFERENCES fbref.teams(team_id)
);

CREATE INDEX idx_fixtures_fixture_id  ON fbref.fixtures(fixture_id);
CREATE INDEX idx_fixtures_competition_seasons_id  ON fbref.fixtures(competition_seasons_id);
CREATE INDEX idx_fixtures_competition_home_team_id  ON fbref.fixtures(home_team_id);
CREATE INDEX idx_fixtures_competition_away_team_id ON fbref.fixtures(away_team_id);
CREATE INDEX idx_fixtures_competition_fixture_fb_ref_id ON fbref.fixtures(fixture_fb_ref_id);



-- convention = {
--   "ix": "ix_%(column_0_label)s",
--   "uq": "uq_%(table_name)s_%(column_0_name)s",
--   "ck": "ck_%(table_name)s_%(constraint_name)s",
--   "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
--   "pk": "pk_%(table_name)s"
-- }