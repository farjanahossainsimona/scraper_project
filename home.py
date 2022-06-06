import requests
from bs4 import BeautifulSoup
import xlwt
from xlwt import Workbook

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from scraper_project.auth import login_required
from scraper_project.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    if request.method == 'POST':
        url = request.form['url']
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        #results = results.prettify()
        results = soup.find(id="front-list-recentlySoldProducts")
        book_titles = []
        job_elements = results.find_all("div", class_="book-list-wrapper")
        
        i = 1
                
        # Workbook is created
        wb = Workbook()
          
        # add_sheet is used to create sheet.
        sheet1 = wb.add_sheet('Recently Sold Products')
          
        sheet1.write(0, 0, 'Book Title')
        sheet1.write(0, 1, 'Author Name')
        sheet1.write(0, 2, 'Book Status')
        sheet1.write(0, 3, 'Price')
        sheet1.write(0, 4, 'Img url')
        sheet1.write(0, 5, 'Book url')  
        
        for job_element in job_elements:
            title = job_element.find("p", class_="book-title")
            book_titles.append(title.text.strip())
            sheet1.write(i, 0, title.text.strip())
       
            author = job_element.find("p", class_="book-author")
            sheet1.write(i, 1, author.text.strip())
            
            status = job_element.find("p", class_="book-status")
            sheet1.write(i, 2, status.text.strip())
            
            price = job_element.find("span")
            sheet1.write(i, 3, price.text.strip())
            
            imgdiv = job_element.find("div", class_="book-img")
            imgurl = imgdiv.find("img")
            imgsrc = imgurl['data-src']
            print(imgsrc)
            sheet1.write(i, 4, imgsrc)
            
            bookurl = job_element.find("a")
            booksrc = bookurl['href']
            sheet1.write(i, 5, booksrc)
            
            i= i+1
           
        wb.save('RokomariFeaturedBooks.xlsx')
        
        return render_template('home/index.html', results=book_titles, url=url)
    
    else:
        return render_template('home/index.html')
    
@bp.route('/profile')
def profile():
    
    return render_template('home/profile.html')