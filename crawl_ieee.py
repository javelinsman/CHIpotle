import requests
from selenium import webdriver 
import bibtexparser
import re
import pathlib
import time
import random
import json

WEBDRIVER_PATH = './chromedriver.exe'

'''
@ARTICLE{7274774,
author={E. {Foxlin} and T. {Calloway} and H. {Zhang}},
journal={IEEE Transactions on Visualization and Computer Graphics}, title={Design and Error Analysis of a Vehicular AR System with Auto-Harmonization},
year={2015},
volume={21},
number={12},
pages={1323-1335},
abstract={This paper describes the design, development and testing of an AR system that was developed for aerospace and ground vehicles to meet stringent accuracy and robustness requirements. The system uses an optical see-through HMD, and thus requires extremely low latency, high tracking accuracy and precision alignment and calibration of all subsystems in order to avoid mis-registration and “swim”. The paper focuses on the optical/inertial hybrid tracking system and describes novel solutions to the challenges with the optics, algorithms, synchronization, and alignment with the vehicle and HMD systems. Tracker accuracy is presented with simulation results to predict the registration accuracy. A car test is used to create a through-the-eyepiece video demonstrating well-registered augmentations of the road and nearby structures while driving. Finally, a detailed covariance analysis of AR registration error is derived.},
keywords={aircraft;augmented reality;automobiles;covariance analysis;error analysis;helmet mounted displays;image registration;optical tracking;traffic engineering computing;error analysis;vehicular AR system;auto-harmonization;aerospace vehicles;ground vehicles;optical see-through HMD;optical-inertial hybrid tracking system;through-the-eyepiece video;covariance analysis;AR registration error;augmented reality;car;aircraft;Aerospace electronics;Optical sensors;Augmented reality;Virtual reality;Calibration;Adaptive optics;Cameras;Augmented reality;registration;calibration;hybrid tracking;inertial;see-through HMD;Inertial, augmented reality, calibration, registration, hybrid tracking, see through HMD, image processing, sensor fusion},
doi={10.1109/TVCG.2015.2481385},
ISSN={1941-0506},
month={Dec},}
'''
def crawl(bibpath):
    
    # Open selenium webdriver
    options = webdriver.ChromeOptions()
    # specify headless mode
    options.add_argument('headless')
    # add disable gpu option
    options.add_argument("disable-gpu")
    browser = webdriver.Chrome(WEBDRIVER_PATH, options=options)

    # TODO: save data in data
    data = {}
    # open bib file
    with open(bibpath, 'r', encoding='utf8') as bibfile :

        # with bibtexparser, parse bib file
        bibs = bibtexparser.load(bibfile)

        fail_count = 0
        for bib in bibs.entries :
            doi = bib['doi']    # get doi which is used as primary key
            ikey = bib['ID']    # get ID to find url

            # TODO: authors
            # TODO: abstract
            # TODO: year
            # TODO: journal ( conference )
            # TODO: volume 
            # TODO: authors
            # 그냥 bib에 존재하는 데이터 다 data로 때려 박을까?

            # TODO: to distinguish from chi data, please change location
            filepath = f"crawled/{doi}.txt"
            if pathlib.Path(filepath).exists():
                print(f'[PASS] {doi}')
                continue

            # Get reference data
            ref_url = f'https://ieeexplore.ieee.org/document/{ikey}/references#references'
            #print(ref_url)
            response = requests.get(ref_url)
            if response.ok:
                browser.implicitly_wait(3)
                browser.get(ref_url)

                refs_ieee = [elem.get_attribute('href') for elem in browser.find_elements_by_class_name('stats-reference-link-viewArticle')]
                refs_cross = [elem.get_attribute('href').split('doi.org/')[1] for elem in browser.find_elements_by_class_name('stats-reference-link-crossRef')]
                refs_acm = [elem.get_attribute('href').split('doi.org/')[1] for elem in browser.find_elements_by_class_name('stats-reference-link-accessAcm')]
                with open('log.txt', 'a') as f:
                    f.write(f'[SUCCESS] {doi} ref\n')
            else:
                with open('log.txt', 'a') as f:
                    f.write(f'[FAIL] {doi} ref\n')
                fail_count += 1

            # get citation data
            cite_url = f'https://ieeexplore.ieee.org/document/{ikey}/citations#citations'
            # print(cite_url)
            response = requests.get(cite_url)
            if response.ok:
                browser.implicitly_wait(3)
                browser.get(cite_url)

                cites_ieee = [elem.get_attribute('href') for elem in browser.find_elements_by_class_name('stats-citations-link-viewArticle')]
                cites_cross = [elem.get_attribute('href').split('doi.org/')[1] for elem in browser.find_elements_by_class_name('stats-citations-link-crossRef')]
                cites_acm = [elem.get_attribute('href').split('doi.org/')[1] for elem in browser.find_elements_by_class_name('stats-citations-link-accessAcm')]
                    

                #print(cites_ieee)
                #print(cites_cross)
                #print(cites_acm)
                with open('log.txt', 'a') as f:
                    f.write(f'[SUCCESS] {doi} cite\n')
            else:
                with open('log.txt', 'a') as f:
                    f.write(f'[FAIL] {doi} cite\n')
                fail_count += 1
            if fail_count >= 3:
                break
            time.sleep(random.randint(5, 10))
    
    browser.quit()


if __name__ == "__main__":
    crawl('./tvcg/tvcg-11-01.bib')