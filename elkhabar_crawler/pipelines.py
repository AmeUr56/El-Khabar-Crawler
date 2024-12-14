# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

months = {"يناير": 1, "فبراير": 2, "مارس": 3, "أبريل": 4, "مايو": 5, "يونيو": 6, "يوليو": 7, "أغسطس": 8, "سبتمبر": 9, "أكتوبر": 10, "نوفمبر": 11, "ديسمبر": 12}

class ProcessingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter.get('title'):
            adapter['title'] = adapter['title'].strip()
        
        if adapter.get('author'):
            author = adapter['author']
            adapter['author'] = author.split(":")[-1].strip()
        
        if adapter.get('number_readers'):
            adapter['number_readers'] = int(adapter['number_readers'])
        
        if adapter.get('content'):
            adapter['content'] = "\n".join(adapter['content']).strip()
            
        if adapter.get('publish_date'):
            date = adapter['publish_date'].strip()
            date = date.replace("\n","").replace("\t","").replace("(","").split(" ")
            day = date[0]
            month = date[1]
            year = date[2]
        
            adapter['publish_date'] = f"{year}-{months[month]}-{day}"
        
        return item

class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect('elkhabar_articles.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS article (
                title TEXT,
                author TEXT,
                publish_date DATE,
                number_readers INT,
                content TEXT
            )
        ''')

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        self.cursor.execute('''
            INSERT INTO article (title, author, publish_date,number_readers,content) VALUES (?,?,?,?,?)
        ''', (
            adapter.get('title'),
            adapter.get('author'),
            adapter.get("publish_date"),
            adapter.get("number_readers"),
            adapter.get("content")
            )
        )

        return item
    