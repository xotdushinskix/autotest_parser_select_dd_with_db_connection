import json
from elasticsearch import Elasticsearch
from selenium import webdriver
import time
import unittest
from selenium.webdriver.support.wait import WebDriverWait
import data

es = Elasticsearch(hosts = 'qwerty.bintime.com:1234')

class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://qaz:wsxg@gepard.bintime.com/')

    def testLogin(self):
        driver = self.driver
        driver.maximize_window()

        helpXPath = data.categoriesXPath

        x = 1
        while x < 1906:
            x += 1
            y = x
            y = str(y)

            a = (helpXPath + y + ']')

            #click on Category Manufacturer
            driver.find_element_by_xpath(data.categorySelect).click()

            #click on categories
            driver.find_element_by_xpath(a).click()

            #click on search button
            WebDriverWait(driver, 50).until(lambda driver : driver.find_element_by_xpath(data.searchButton)).click()
            time.sleep(3)

            resultCategorie = WebDriverWait(driver, 50).until(lambda driver : driver.find_element_by_xpath(data.resultForCategorie))
            result = resultCategorie.text
            quantity = result.split(" ")[0]
            quantity = int(quantity)
            categName = result[:]

            categName = str(categName)
            a = categName
            b = (' '.join(a.split()[3:]))
            categoryNameLowerCase = (b.lower())
            print(categoryNameLowerCase)
            categoryNameWithoutQuotes = categoryNameLowerCase[1:-1]

            toData = es.count(index = "gepard_product", doc_type = "product", body = {
              "query": {
                "filtered": {
                  "filter": {
                    "bool": {
                      "must": [
                        {"term": {
                          "multilingual.1.category_name.exact": categoryNameWithoutQuotes
                        }},
                        {
                          "term": {
                            "visibility": "1"
                          }
                        }
                      ]
                    }
                  }
                }
              }
            }
            )

            dbProduct = json.dumps(toData["count"]).strip("")
            dbProduct = int(dbProduct)
            print(dbProduct)

            if quantity == dbProduct:
                print('good')
            else:
                print('bad')
                driver.save_screenshot('/home/nikita/SeleniumGepard/DataAndCategoryQuantity/invalidData.png')
            print('           ')

if __name__ == '__main__':
    unittest.main()


