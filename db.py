# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import requests


class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['douban.com']

    #start_urls = ['http://douban.com/']
    def start_requests(self):
        url = 'https://accounts.douban.com/login'
        return [Request(url,callback=self.parse,meta={"cookiejar":1})]

    def parse(self, response):
        captcha_url=response.xpath('//img[@id="captcha_image"]/@src').extract()[0]
        if captcha_url =="":
            print("此时无验证码")
            data={
                "source": "index_nav",
                "redir": "https: // www.douban.com /",
                "form_email":str(13673090326),
                "form_password":"czj123123",
                "login": "登录"
            }
            print("登录中*******")
            return [FormRequest.from_response(response,callback=self.parse_login,formdata=data,meta={"cookiejar":response.meta["cookiejar"]})]

        else:
            captcha_id = response.xpath('//div[@class="captcha_block"]/input[@type="hidden"]/@value').extract()[0]
            print(captcha_id)
            print("此时有验证码")
            captresponse=requests.get(captcha_url)
            with open('D:\CAPTCHA\captcha.png','wb') as f:
                f.write(captresponse.content)
            print("请输入验证码*******")
            captcha=input()
            data2={
                "source":"index_nav",
                "redir":"https: // www.douban.com /",
                "form_email":str(13673090326),
                "form_password":"czj123123",
                "captcha-solution": captcha,
                "captcha-id": captcha_id,  # 需要修改
                "login": "登录",

            }
            return [FormRequest.from_response(response,callback=self.parse_login,formdata=data2,meta={"cookiejar":response.meta["cookiejar"]})]

    def parse_login(self,response):
        print(response.text)
        name=response.xpath('//div[@class="top-nav-info"]//span/text()').extract()
        if len(name)>0:
            print("登录成功")
        else:
            print("登录失败")

