# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import sqlite3

class MongoDbPipeline:
    collection_name = "best_movies"

    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://Elveera:test123@cluster0.mxs3z.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item) #name of collection to store all ids
        return item

class SQLlitePipeline(object):

    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))

    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE best_movies(
                    title TEXT,
                    year TEXT,
                    genre TEXT,
                    duration TEXT,
                    rating TEXT,
                    movie_url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
       self.connection.close()


    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO best_movies (title, year, genre, duration, rating, movie_url) VALUES(?,?,?,?,?,?)

        ''', (
            item.get('title'),
            item.get('year'),
            item.get('genre'),
            item.get('duration'),
            item.get('rating'),
            item.get('movie_url')
        ))
        self.connection.commit()
        return item
