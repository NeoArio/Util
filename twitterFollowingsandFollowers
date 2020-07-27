from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


class twitterFollowingsandFollowers:
    def __init__(self, path):
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.base_url = "https://twitter.com/"
        self.css_class = "a[class='r-hkyrab r-1loqt21 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0 css-4rbku5 css-18t94o4 css-901oao']"
        self.path = path
        self.id = id

    def extract(self, id):
        url = self.base_url + id
        self.driver.get(url)
        time.sleep(10)
        elements = self.driver.find_elements_by_css_selector(self.css_class)
        count = 0
        while not elements:
            count += 1
            time.sleep(5)
            elements = self.driver.find_elements_by_css_selector(self.css_class)
            if count > 5:
                return "not_found", "not_found"
        followings = elements[0].get_attribute("title")
        followers = elements[1].get_attribute("title")
        return followings, followers

    def read_csv(self):
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file)
            list_of_publishers = []
            for row in csv_reader:
                if row:
                    list_of_publishers.append(row[0].split('//')[1])
        return list_of_publishers


if __name__ == '__main__':
    tw = twitterFollowingsandFollowers("/home/yusif/Desktop/publishers.csv")
    tw2 = twitterFollowingsandFollowers("/home/yusif/Desktop/publishers2.csv")
    list_of_publishers = tw.read_csv()
    list_of_publishers2 = tw2.read_csv()
    final_list = [item for item in list_of_publishers2 if item not in list_of_publishers]
    with open('publishers_file2.csv', mode='w') as publishers_file:
        publishers_writer = csv.writer(publishers_file)
        for index, publisher in enumerate(final_list):
            followings, followers = tw.extract(publisher)
            print("ID: {},  followings: {}, followers: {}".format(publisher, followings, followers))

            if index == 0:
                publishers_writer.writerow(["Publisher", "Followings", "Followers"])
            publishers_writer.writerow([publisher, followings, followers])

