# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy import Request, FormRequest
from scrapy.http import TextResponse
from datetime import date
import json
import re
from collections import OrderedDict

class alkomprar_comSpider(scrapy.Spider):

    name = "alkomprar_com_spider"

###########################################################
    models = []
    title = 'Flyers'
    count = 0
    def __init__(self, brand=None, url=None, *args, **kwargs):
        super(alkomprar_comSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://print24.com/fr/']
        if brand:
            self.title = brand.replace('_', ' ')
            self.start_urls = ['https://print24.com' + url]

            print (url)

###########################################################

    # def parse(self, response):
    #     urls = response.xpath('//div[@id="productmenu"]//li[@item_group]/a')
    #     for url in urls:
    #         item_url = url.xpath('./@href').extract_first()
    #         title = url.xpath('./div/text()').extract_first()
    #         # yield Request(response.urljoin(item_url), callback=self.parse1, meta={'title':title, 'page':1})
    #         yield Request('https://print24.com/fr/product/accroche-portes/', callback=self.parse1, meta={'title':title, 'page':1})
    #         break

###########################################################

    def parse(self, response):
        item = OrderedDict()
        item['title'] = self.title
        formdata = OrderedDict()
        formdata_header = {}
        param_tags = response.xpath('//form[@name="calcform"]/input')
        for param in param_tags:
            value = param.xpath('./@value').extract_first()
            if value:
                key = param.xpath('./@name').extract_first()
                formdata[key] = value
                formdata_header[key] = value

        param_tags = response.xpath('//form[@name="calcform"]/div[@id="calcContent"]/input')
        for param in param_tags:
            value = param.xpath('./@value').extract_first()
            if value:
                key = param.xpath('./@id').extract_first()
                if "prev_item_group" in key:
                    formdata['prev_item_group'] = value
                    formdata_header['prev_item_group'] = value
                elif "prev_view_group" in key:
                    formdata['prev_view_group'] = value
                    formdata_header['prev_view_group'] = value
        total_options = OrderedDict()
        one_option = {}
        formdata.pop('availability_value', None)
        formdata.pop('pg', None)
        formdata_header.pop('availability_value', None)
        formdata_header.pop('pg', None)

        left_options = response.xpath('//section[contains(@class,"leftColumn")]//div[@box_name]')
        for options in left_options:
            # tow_divs = options_div.xpath('./div[@class="width49pr"]')
            # divs = []
            # if tow_divs:
            #     for div in tow_divs:
            #         divs.append(div)
            # else:
            #     divs.append(options_div)
                key = options.xpath('./@box_name').extract_first()
                if key == "shipping_country" : continue
                value = options.xpath('.//div[@class="column rc_0"]/div/@property').extract_first()
                if value:
                    formdata[key] = value
                if key != "item_group" and key != "availability":
                    attrs = {}
                    label = options.xpath('./parent::div/label/text()').extract_first()
                    if label:
                        attrs['option_name'] = label
                        value_tags = options.xpath('.//div[@class="column rc_0"]/div[not(@class="header")]')
                        value_tags2 = options.xpath('.//div[@class="column rc_1"]/div[not(@class="header")]')
                        values = OrderedDict()
                        for i, value_tag in enumerate(value_tags):
                            val_key = ''.join(value_tag.xpath('./text()').extract())
                            if len(value_tags2) > i :
                                val_key1 = ''.join(value_tags2[i].xpath('./text()').extract())
                                val_key = (val_key+' ' + val_key1).strip()
                            val_value = value_tag.xpath('./@property').extract_first()
                            if val_key != '':
                                values[val_key] = val_value
                        attrs['values'] = values
                        if len(values.keys()) > 1:
                            total_options[key] = attrs
                            formdata[key] = values[list(values.keys())[0]]
                        elif len(values.keys()) == 1:
                            one_option[key] = attrs

        right_options = response.xpath('//section[contains(@class,"rightColumn")]//div[@box_name]')
        for options in right_options:
            # tow_divs = options_div.xpath('./div[@class="width49pr"]')
            # divs = []
            # if tow_divs:
            #     for div in tow_divs:
            #         divs.append(div)
            # else:
            #     divs.append(options_div)
            # for options in divs:
                key = options.xpath('./@box_name').extract_first()
                if key == "shipping_country" : continue
                value = options.xpath('.//div[@class="column rc_0"]/div/@property').extract_first()
                if value:
                    formdata[key] = value
                if key != "item_group" and key != "availability":
                    attrs = {}
                    label = options.xpath('./parent::div/label/text()').extract_first()
                    if label:
                        attrs['option_name'] = label
                        value_tags = options.xpath('.//div[@class="column rc_0"]/div[not(@class="header")]')
                        value_tags2 = options.xpath('.//div[@class="column rc_1"]/div[not(@class="header")]')
                        values = OrderedDict()
                        for i, value_tag in enumerate(value_tags):
                            val_key = ''.join(value_tag.xpath('./text()').extract())
                            if len(value_tags2) > i :
                                val_key1 = ''.join(value_tags2[i].xpath('./text()').extract())
                                val_key = (val_key+' ' + val_key1).strip()
                            val_value = value_tag.xpath('./@property').extract_first()
                            if val_key != '':
                                values[val_key] = val_value
                        attrs['values'] = values
                        if len(values.keys()) > 1:
                            total_options[key] = attrs
                            formdata[key] = values[list(values.keys())[0]]
                        elif len(values.keys()) == 1:
                            one_option[key] = attrs


        formdata['shipping_country'] = 'FR'
        formdata['cmd'] = 'send_properties'
        formdata['view_group'] = '0'
        # formdata['changed_box'] = 'quantity'
        formdata['finishing_size'] = '4016'
        url = 'https://print24.com/fr/cgi-bin/ajax.cgi'
        index_option = 0
        for one in one_option.keys():
            index_option +=1
            item['Option{} Name'.format(index_option)] = one_option[one]['option_name']
            val1 = list(one_option[one]['values'].keys())[0]
            item['Option{} Value'.format(index_option)] = val1
            formdata[one] = one_option[one]['values'][val1]

        # index_option += 1
    #     yield FormRequest(url, callback=self.parse_options, formdata=formdata, meta={'formdata_header':formdata_header}, dont_filter=True)
    #
    # def parse_options(self, response):
    #     formdata_header = response.meta['formdata_header']
    #     formdata = {}
    #     for key in formdata_header.keys():
    #         formdata[key] = formdata_header[key]
    #
    #     item = OrderedDict()
    #     item['title'] = self.title
    #     html = json.loads(response.body)['boxes']
    #     resp = TextResponse(url=response.url, body=html, encoding='utf-8')
    #
    #
    #     total_options = OrderedDict()
    #     one_option = {}
    #     # formdata.pop('availability_value', None)
    #     # formdata.pop('pg', None)
    #     index_option = 1
    #     left_options = resp.xpath('//section[contains(@class,"leftColumn")]//div[@box_name]')
    #     for options in left_options:
    #         # tow_divs = options_div.xpath('./div[@class="width49pr"]')
    #         # divs = []
    #         # if tow_divs:
    #         #     for div in tow_divs:
    #         #         divs.append(div)
    #         # else:
    #         #     divs.append(options_div)
    #         key = options.xpath('./@box_name').extract_first()
    #         if key == "shipping_country" : continue
    #         value = options.xpath('.//div[@class="column rc_0"]/div/@property').extract_first()
    #         if value:
    #             formdata[key] = value
    #             label = options.xpath('./parent::div/label/text()').extract_first()
    #             if label:
    #                 value_tags = options.xpath('.//div[@class="column rc_0"]/div[@class="header"]/text()').extract_first()
    #                 value_tags2 = ''.join(options.xpath('.//div[@class="column rc_1"]/div[@class="header"]/text()').extract())
    #                 if value_tags:
    #                     item['Option{} Name'.format(index_option)] = label
    #                     item['Option{} Value'.format(index_option)] = value_tags + value_tags2
    #                     index_option += 1
    #         if key != "item_group" and key != "availability":
    #             attrs = {}
    #             label = options.xpath('./parent::div/label/text()').extract_first()
    #             if label:
    #                 attrs['option_name'] = label
    #                 value_tags = options.xpath('.//div[@class="column rc_0"]/div[not(@class="header")]')
    #                 value_tags2 = options.xpath('.//div[@class="column rc_1"]/div[not(@class="header")]')
    #                 values = OrderedDict()
    #                 for i, value_tag in enumerate(value_tags):
    #                     val_key = ''.join(value_tag.xpath('./text()').extract())
    #                     if len(value_tags2) > i :
    #                         val_key1 = ''.join(value_tags2[i].xpath('./text()').extract())
    #                         val_key = (val_key+' ' + val_key1).strip()
    #                     val_value = value_tag.xpath('./@property').extract_first()
    #                     if val_key != '':
    #                         values[val_key] = val_value
    #                 attrs['values'] = values
    #                 if len(values.keys()) > 1:
    #                     total_options[key] = attrs
    #                     # formdata[key] = values[list(values.keys())[0]]
    #                 elif len(values.keys()) == 1:
    #                     one_option[key] = attrs
    #
    #     right_options = resp.xpath('//section[contains(@class,"rightColumn")]//div[@box_name]')
    #     for options in right_options:
    #         # tow_divs = options_div.xpath('./div[@class="width49pr"]')
    #         # divs = []
    #         # if tow_divs:
    #         #     for div in tow_divs:
    #         #         divs.append(div)
    #         # else:
    #         #     divs.append(options_div)
    #         # for options in divs:
    #         key = options.xpath('./@box_name').extract_first()
    #         if key == "shipping_country" : continue
    #         value = options.xpath('.//div[@class="column rc_0"]/div/@property').extract_first()
    #         if value:
    #             formdata[key] = value
    #             label = options.xpath('./parent::div/label/text()').extract_first()
    #             if label:
    #                 value_tags = options.xpath('.//div[@class="column rc_0"]/div[@class="header"]/text()').extract_first()
    #                 value_tags2 = ''.join(options.xpath('.//div[@class="column rc_1"]/div[@class="header"]/text()').extract())
    #                 if value_tags:
    #                     item['Option{} Name'.format(index_option)] = label
    #                     item['Option{} Value'.format(index_option)] = value_tags + value_tags2
    #                     index_option += 1
    #         if key != "item_group" and key != "availability":
    #             attrs = {}
    #             label = options.xpath('./parent::div/label/text()').extract_first()
    #             if label:
    #                 attrs['option_name'] = label
    #                 value_tags = options.xpath('.//div[@class="column rc_0"]/div[not(@class="header")]')
    #                 value_tags2 = options.xpath('.//div[@class="column rc_1"]/div[not(@class="header")]')
    #                 values = OrderedDict()
    #                 for i, value_tag in enumerate(value_tags):
    #                     val_key = ''.join(value_tag.xpath('./text()').extract())
    #                     if len(value_tags2) > i :
    #                         val_key1 = ''.join(value_tags2[i].xpath('./text()').extract())
    #                         val_key = (val_key+' ' + val_key1).strip()
    #                     val_value = value_tag.xpath('./@property').extract_first()
    #                     if val_key != '':
    #                         values[val_key] = val_value
    #                 attrs['values'] = values
    #                 if len(values.keys()) > 1:
    #                     total_options[key] = attrs
    #                     # formdata[key] = values[list(values.keys())[0]]
    #                 elif len(values.keys()) == 1:
    #                     one_option[key] = attrs
    #
    #     price_text = response.body.split('priceDisplay')[-1].split('</div>')[0]
    #     prices = re.findall(r'[\d,.]+', price_text)
    #     if prices:
    #         item['Variant Price_No_Vat'] = prices[-2].replace(',','.')
    #         if item['Variant Price_No_Vat'].count('.') > 1:
    #             item['Variant Price_No_Vat'] = item['Variant Price_No_Vat'].replace('.', '', 1)
    #         item['Variant Price_Vat'] = prices[-1].replace(',','.')
    #         if item['Variant Price_Vat'].count('.') > 1:
    #             item['Variant Price_Vat'] = item['Variant Price_Vat'].replace('.', '', 1)
    #     price_delivery_text = response.body.split('TTC plus')[-1].split('de livraison')[0]
    #     if price_delivery_text:
    #         item['Fee'] = re.findall(r'[\d,.]+', price_delivery_text)[0]
    #     # self.models.append(item)
    #     self.count += 1
    #     print(self.count)
    #     yield item
    #
    #     formdata['shipping_country'] = 'FR'
    #     formdata['cmd'] = 'send_properties'
    #     formdata['view_group'] = '0'
    #     # formdata['changed_box'] = 'quantity'
    #     formdata['finishing_size'] = '4016'
    #     url = 'https://print24.com/fr/cgi-bin/ajax.cgi'
    #     index_option = 0
    #     # for one in one_option.keys():
    #     #     index_option +=1
    #     #     item['Option{} Name'.format(index_option)] = one_option[one]['option_name']
    #     #     val1 = list(one_option[one]['values'].keys())[0]
    #     #     item['Option{} Value'.format(index_option)] = val1
    #     #     formdata[one] = one_option[one]['values'][val1]
    #
    #     # index_option += 1
    #     condition_item = None
    #     final_item = None
    #     for i, key in enumerate(total_options.keys()):
    #         val = formdata[key]
    #         if i+1 < len(total_options.keys()):
    #             for j, key1 in enumerate(total_options[key]['values'].keys()):
    #                 if val == total_options[key]['values'][key1] and len(total_options[key]['values'].keys()) > j+1:
    #                     condition_item = {key: total_options[key]['values'][list(total_options[key]['values'].keys())[j+1]]}
    #                     break
    #         else:
    #             for j, key1 in enumerate(total_options[key]['values'].keys()):
    #                 if val == total_options[key]['values'][key1] and len(total_options[key]['values'].keys()) > j+1:
    #                     condition_item = {key: total_options[key]['values'][list(total_options[key]['values'].keys())[j+1]]}
    #                     break
    #                 elif j+1 == len(total_options[key]['values'].keys()):
    #                     final_item = {key: total_options[key]['values'][list(total_options[key]['values'].keys())[0]]}
    #
    #     if condition_item:
    #         formdata[condition_item.keys()[0]] = condition_item.values()[0]
    #     if final_item:
    #         formdata[final_item.keys()[0]] = final_item.values()[0]
    #
    #
    #     yield FormRequest(url, callback=self.parse_options, formdata=formdata, meta={'formdata_header':formdata_header}, dont_filter=True)


    # def temp(self, response):
    #
        key1 = list(total_options.keys())[0]
        item['Option{} Name'.format(index_option+1)] = total_options[key1]['option_name']
        for i, val1 in enumerate(total_options[key1]['values'].keys()):
            if i > 0:break
            item['Option{} Value'.format(index_option+1)] = val1
            formdata[key1] = total_options[key1]['values'][val1]
            if len(total_options.keys()) < 2:
                yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
            else:
                key2 = list(total_options.keys())[1]
                item['Option{} Name'.format(index_option+2)] = total_options[key2]['option_name']
                for val2 in total_options[key2]['values'].keys():
                    item['Option{} Value'.format(index_option+2)] = val2
                    formdata[key2] = total_options[key2]['values'][val2]

                    if len(total_options.keys()) < 3:
                        yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                    else:
                        key3 = list(total_options.keys())[2]
                        item['Option{} Name'.format(index_option+3)] = total_options[key3]['option_name']
                        for val3 in total_options[key3]['values'].keys():
                            item['Option{} Value'.format(index_option+3)] = val3
                            formdata[key3] = total_options[key3]['values'][val3]

                            if len(total_options.keys()) < 4:
                                yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                            else:
                                key4 = list(total_options.keys())[3]
                                item['Option{} Name'.format(index_option+4)] = total_options[key4]['option_name']
                                for val4 in total_options[key4]['values'].keys():
                                    item['Option{} Value'.format(index_option+4)] = val4
                                    formdata[key4] = total_options[key4]['values'][val4]

                                    if len(total_options.keys()) < 5:
                                        yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                    else:
                                        key5 = list(total_options.keys())[4]
                                        item['Option{} Name'.format(index_option+5)] = total_options[key5]['option_name']
                                        for val5 in total_options[key5]['values'].keys():
                                            item['Option{} Value'.format(index_option+5)] = val5
                                            formdata[key5] = total_options[key5]['values'][val5]

                                            if len(total_options.keys()) < 6:
                                                yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                            else:
                                                key6 = list(total_options.keys())[5]
                                                item['Option{} Name'.format(index_option+6)] = total_options[key6]['option_name']
                                                for val6 in total_options[key6]['values'].keys():
                                                    item['Option{} Value'.format(index_option+6)] = val6
                                                    formdata[key6] = total_options[key6]['values'][val6]

                                                    if len(total_options.keys()) < 7:
                                                        yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                    else:
                                                        key7 = list(total_options.keys())[6]
                                                        item['Option{} Name'.format(index_option+7)] = total_options[key7]['option_name']
                                                        for val7 in total_options[key7]['values'].keys():
                                                            item['Option{} Value'.format(index_option+7)] = val7
                                                            formdata[key7] = total_options[key7]['values'][val7]

                                                            if len(total_options.keys()) < 8:
                                                                yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                            else:
                                                                key8 = list(total_options.keys())[7]
                                                                item['Option{} Name'.format(index_option+8)] = total_options[key8]['option_name']
                                                                for val8 in total_options[key8]['values'].keys():
                                                                    item['Option{} Value'.format(index_option+8)] = val8
                                                                    formdata[key8] = total_options[key8]['values'][val8]

                                                                    if len(total_options.keys()) < 9:
                                                                        yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                    else:
                                                                        key9 = list(total_options.keys())[8]
                                                                        item['Option{} Name'.format(index_option+9)] = total_options[key9]['option_name']
                                                                        for val9 in total_options[key9]['values'].keys():
                                                                            item['Option{} Value'.format(index_option+9)] = val9
                                                                            formdata[key9] = total_options[key9]['values'][val9]

                                                                            if len(total_options.keys()) < 10:
                                                                                yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                            else:
                                                                                key10 = list(total_options.keys())[9]
                                                                                item['Option{} Name'.format(index_option+10)] = total_options[key10]['option_name']
                                                                                for val10 in total_options[key10]['values'].keys():
                                                                                    item['Option{} Value'.format(index_option+10)] = val10
                                                                                    formdata[key10] = total_options[key10]['values'][val10]

                                                                                    if len(total_options.keys()) < 11:
                                                                                        yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                                    else:
                                                                                        key11 = list(total_options.keys())[10]
                                                                                        item['Option{} Name'.format(index_option+11)] = total_options[key11]['option_name']
                                                                                        for val11 in total_options[key11]['values'].keys():
                                                                                            item['Option{} Value'.format(index_option+11)] = val11
                                                                                            formdata[key11] = total_options[key11]['values'][val11]

                                                                                            if len(total_options.keys()) < 12:
                                                                                                yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                                            else:
                                                                                                key12 = list(total_options.keys())[11]
                                                                                                item['Option{} Name'.format(index_option+12)] = total_options[key12]['option_name']
                                                                                                for val12 in total_options[key12]['values'].keys():
                                                                                                    item['Option{} Value'.format(index_option+12)] = val12
                                                                                                    formdata[key12] = total_options[key12]['values'][val12]

                                                                                                    if len(total_options.keys()) < 13:
                                                                                                        yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                                                    else:
                                                                                                        key13 = list(total_options.keys())[12]
                                                                                                        item['Option{} Name'.format(index_option+13)] = total_options[key13]['option_name']
                                                                                                        for val13 in total_options[key13]['values'].keys():
                                                                                                            item['Option{} Value'.format(index_option+13)] = val13
                                                                                                            formdata[key13] = total_options[key13]['values'][val13]

                                                                                                            if len(total_options.keys()) < 14:
                                                                                                                yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                                                            else:
                                                                                                                key14 = list(total_options.keys())[13]
                                                                                                                item['Option{} Name'.format(index_option+14)] = total_options[key14]['option_name']
                                                                                                                for val14 in total_options[key14]['values'].keys():
                                                                                                                    item['Option{} Value'.format(index_option+14)] = val14
                                                                                                                    formdata[key14] = total_options[key14]['values'][val14]

                                                                                                                    if len(total_options.keys()) < 15:
                                                                                                                        yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                                                                    else:
                                                                                                                        key15 = list(total_options.keys())[14]
                                                                                                                        item['Option{} Name'.format(index_option+15)] = total_options[key15]['option_name']
                                                                                                                        for val15 in total_options[key15]['values'].keys():
                                                                                                                            item['Option{} Value'.format(index_option+15)] = val15
                                                                                                                            formdata[key15] = total_options[key15]['values'][val15]

                                                                                                                            if len(total_options.keys()) < 16:
                                                                                                                                yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                                                                            else:
                                                                                                                                key16 = list(total_options.keys())[15]
                                                                                                                                item['Option{} Name'.format(index_option+16)] = total_options[key16]['option_name']
                                                                                                                                for val16 in total_options[key16]['values'].keys():
                                                                                                                                    item['Option{} Value'.format(index_option+16)] = val16
                                                                                                                                    formdata[key16] = total_options[key16]['values'][val16]

                                                                                                                                    if len(total_options.keys()) < 17:
                                                                                                                                        yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                                                                                    else:
                                                                                                                                        key17 = list(total_options.keys())[16]
                                                                                                                                        item['Option{} Name'.format(index_option+17)] = total_options[key17]['option_name']
                                                                                                                                        for val17 in total_options[key17]['values'].keys():
                                                                                                                                            item['Option{} Value'.format(index_option+17)] = val17
                                                                                                                                            formdata[key17] = total_options[key17]['values'][val17]

                                                                                                                                            if len(total_options.keys()) < 18:
                                                                                                                                                yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                                                                                            else:

                                                                                                                                                key18 = list(total_options.keys())[17]
                                                                                                                                                item['Option{} Name'.format(index_option+18)] = total_options[key18]['option_name']
                                                                                                                                                for val18 in total_options[key18]['values'].keys():
                                                                                                                                                    item['Option{} Value'.format(index_option+18)] = val18
                                                                                                                                                    formdata[key18] = total_options[key18]['values'][val18]

                                                                                                                                                    if len(total_options.keys()) < 19:
                                                                                                                                                        yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                                                                                                    else:

                                                                                                                                                        key19 = list(total_options.keys())[18]
                                                                                                                                                        item['Option{} Name'.format(index_option+19)] = total_options[key19]['option_name']
                                                                                                                                                        for val19 in total_options[key19]['values'].keys():
                                                                                                                                                            item['Option{} Value'.format(index_option+19)] = val19
                                                                                                                                                            formdata[key19] = total_options[key19]['values'][val19]

                                                                                                                                                            if len(total_options.keys()) < 20:
                                                                                                                                                                yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})
                                                                                                                                                            else:

                                                                                                                                                                key20 = list(total_options.keys())[19]
                                                                                                                                                                item['Option{} Name'.format(index_option+20)] = total_options[key20]['option_name']
                                                                                                                                                                for val20 in total_options[key20]['values'].keys():
                                                                                                                                                                    item['Option{} Value'.format(index_option+20)] = val20
                                                                                                                                                                    formdata[key20] = total_options[key20]['values'][val20]

                                                                                                                                                                    yield FormRequest(url, callback=self.parsePrice, formdata=formdata, meta={'item':item})






    def parsePrice(self, response):

        item = response.meta['item']
        price_text = response.body.split('priceDisplay')[-1].split('</div>')[0]
        prices = re.findall(r'[\d,.]+', price_text)
        if prices:
            item['Variant Price_No_Vat'] = prices[-2].replace(',','.')
            if item['Variant Price_No_Vat'].count('.') > 1:
                item['Variant Price_No_Vat'] = item['Variant Price_No_Vat'].replace('.', '', 1)
            item['Variant Price_Vat'] = prices[-1].replace(',','.')
            if item['Variant Price_Vat'].count('.') > 1:
                item['Variant Price_Vat'] = item['Variant Price_Vat'].replace('.', '', 1)
        price_delivery_text = response.body.split('TTC plus')[-1].split('de livraison')[0]
        if price_delivery_text:
            item['Fee'] = re.findall(r'[\d,.]+', price_delivery_text)[0]
        # self.models.append(item)
        self.count += 1
        print(self.count)
        yield item

