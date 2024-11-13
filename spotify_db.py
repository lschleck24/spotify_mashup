from base_db import _BaseDB
import os
import sqlite3
import pandas as pd
from datetime import datetime as dt
from glob import glob
import numpy as np
from traceback import print_exc as pe
from tqdm import tqdm

class SpotifyDB(_BaseDB):
    FOLDER = ''
    DB_NAME = 'spotify_db.sqlite'

    DATA = 'data/playlist_songs4.csv'

    PATH = FOLDER + DATA

    def __init__(self, 
                 create: bool = False):
        super().__init__(self.PATH, create)

        if create == True:
            pass

        return
    
    def _drop_tables(self) -> None:
        sql = """
            DROP TABLE IF EXISTS tSong
            ;"""
        self.run_action(sql,keep_open=True)

        sql = """
            DROP TABLE IF EXISTS tArtist
            ;"""
        self.run_action(sql,keep_open=True)
        
        sql = """
            DROP TABLE IF EXISTS tGenre
            ;"""
        self.run_action(sql,keep_open=True)

        sql = """
            DROP TABLE IF EXISTS tPlaylist
            ;"""
        self.run_action(sql,keep_open=True)

        sql = """
            DROP TABLE IF EXISTS tSongByArtist
            ;"""
        self.run_action(sql,keep_open=True)

        sql = """
            DROP TABLE IF EXISTS tSongByGenre
            ;"""
        self.run_action(sql,keep_open=True)

        sql = """
            DROP TABLE IF EXISTS tSongByPlaylist
            ;"""
        self.run_action(sql,keep_open=True)

        self._conn.commit()
        self._close()
        return
    
    def _create_tables(self) -> None:
        sql = """
            CREATE TABLE tSong (
                song_id INTEGER PRIMARY KEY,
                song_name TEXT NOT NULL,
                duration INTEGER NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL
            );"""
        self.run_action(sql,keep_open=True)

        sql = """
            CREATE TABLE tArtist (
                artist_id INTEGER PRIMARY KEY,
                artist_name TEXT NOT NULL
            );"""
        self.run_action(sql,keep_open=True)

        sql = """
            CREATE TABLE tGenre (
                genre_id INTEGER PRIMARY KEY,
                genre_name TEXT NOT NULL
            );"""
        self.run_action(sql,keep_open=True)

        sql = """
            CREATE TABLE tPlaylist (
                playlist_id INTEGER PRIMARY KEY,
                playlist_name TEXT NOT NULL
            );"""
        self.run_action(sql,keep_open=True)


def _get_song_id(self,song_name,duration,year,month):
    pass




'''
LIST OF NECESSARY COLUMNS
song_name, duration (seconds), year, month
list of artist names
list of genres
list of playlist names

LIST OF OPTIONAL COLUMNS
day, album name

'''