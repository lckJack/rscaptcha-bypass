#!/usr/bin/env python
# -*- coding: utf-8 -*


import bs4 as BeautifulSoup
import requests
import json
import time
import os
import sys
from PIL import Image
import cv2
import pytesseract
from colored import fg, bg, attr

def do_request():

    #custom request to bypass the captcha
    return True

def check_folder():
    if not os.path.isdir('./imgs'):
        os.mkdir('./imgs')
        print("%s [Creating: dir]%s " % (fg(11), attr(0)) + "./imgs")

    else:
        print("%s [Exists: dir]%s " % (fg(11), attr(0)) + "./imgs")

if __name__ == "__main__":
    print('Lets try breaking that annoying captcha :)')
    check_folder()
    url = 'http://localhost/'
    headers = {
        #Headers u need:
        # 'key': 'value',
    }
    nrequest = 20 # number of requests, if you want unlimited request change 'for' bucle to 'while'
    time_between_request = 1 # lets give a break to the server

    for number in range(nrequest):      
        r = requests.post(url+'/wp-admin/admin-ajax.php', data={'action': 'new_captcha'}, headers=headers)
        r.enconding = 'utf-8'
        rbeauty = json.loads(r.text)

        print("%s [Saving]%s " % (fg(11), attr(0)) + (str(rbeauty['prefix'])+".png"))

        imgfile = requests.get(rbeauty['img'], headers=headers)

        f = open(('imgs/'+str(rbeauty['prefix'])+".png"), "wb")
        f.write(imgfile.content)
        f.close()

        im_gray = cv2.imread('imgs/'+str(rbeauty['prefix'])+".png", cv2.IMREAD_GRAYSCALE)        
        (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

        cv2.imwrite('imgs/'+str(rbeauty['prefix'])+".png", im_bw)

        imgtext = pytesseract.image_to_string(Image.open('imgs/'+str(rbeauty['prefix'])+".png"))

        if len(imgtext) == 4:
            print("%s [Maybe Recognized]%s " % (fg(40), attr(0)) + (imgtext.strip()).replace('\n', ''))

            #do_request() < Now there is captcha make a custom request to the page and its done :)

        else:
            print("%s [Not Recognized]%s " % (fg(9), attr(0)) + (imgtext.strip()).replace('\n', ''))
        
        

        time.sleep( time_between_request )
    
