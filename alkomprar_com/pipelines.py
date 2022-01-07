# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import xlsxwriter
import os, csv
from collections import OrderedDict

class AlkomprarComPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline


    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        # if spider.name == 'task6_scraper' or spider.name == 'task6_scraper_no':
        #     try:
            f1 = open('{}1.csv'.format(spider.title),"w", newline='')
            writer = csv.writer(f1, delimiter=';',quoting=csv.QUOTE_ALL)
            writer.writerow(spider.headers)
            flag1 = True
            for data in spider.models:
                if flag1:
                    writer.writerow(data.keys())
                    flag1 =False
                else:
                    writer.writerow(data.values())

            f1.close()
        #     except:
        #         pass
        #
        # # pass
        #     filepath = 'carreau-de-ciment-mural.xlsx'
        #     if os.path.isfile(filepath):
        #         os.remove(filepath)
        #     workbook = xlsxwriter.Workbook(filepath)
        #     sheet = workbook.add_worksheet('eclairage-exterieur')
        #     data = spider.result_data_list
        #     headers = spider.headers
        #     flag =True
        #     # headers = []
        #     print('---------------Writing in file----------------------')
        #     print('total row: ' + str(len(data)))
        #
        #     for index, value in enumerate(data.keys()):
        #         if flag:
        #             for col, val in enumerate(headers):
        #                 # headers.append(val)
        #                 sheet.write(index, col, val)
        #             flag = False
        #         for col, key in enumerate(headers):
        #             if key in data[value].keys():
        #                 sheet.write(index+1, col, data[value][key])
        #             else:
        #                 sheet.write(index+1, col, '')
        #         print('row :' + str(index))
        #
        #     workbook.close()
        #
        # elif spider.name == 'ouyao_cn' or spider.name == "qq":

            filepath = '{}.xlsx'.format(spider.title)
            if os.path.isfile(filepath):
                os.remove(filepath)
            workbook = xlsxwriter.Workbook(filepath)
            sheet = workbook.add_worksheet('eclairage-exterieur')
            data = spider.models
            # headers = spider.headers
            flag =True
            # headers = []
            print('---------------Writing in file----------------------')
            print('total row: ' + str(len(data)))

            for index, value in enumerate(data):
                if flag:
                    for col, val in enumerate(value.keys()):
                        # headers.append(val)
                        sheet.write(index, col, val)
                    flag = False
                for col, key in enumerate(value.keys()):
                    sheet.write(index+1, col, value[key])

                print('row :' + str(index))

            workbook.close()



    def process_item(self, item, spider):

        return item
