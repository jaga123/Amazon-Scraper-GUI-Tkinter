from tkinter import *
from PIL import ImageTk
from Functions import *
import pandas as pd
import time

Category = [
    "All Departments",
    "Audible Audiobooks",
    "Alexa Skills",
    "Amazon Devices",
    "Amazon Warehouse Deals",
    "Apps & Games",
    "Automotive",
    "Beauty",
    "Books",
    "Music",
    "Baby",
    "Clothing & Accessories",
    "Electronics",
    "Gift Cards",
    "Grocery",
    "Handmade",
    "Health & Personal Care",
    "Home & Kitchen",
    "Industrial & Scientific",
    "Jewelery",
    "Kindle Store",
    "Luggage & Bags",
    "Luxury Beauty",
    "Movies & TV",
    "Musical Instruments, Stage & Audio",
    "Office Products",
    "Patio, Lawn & Garden",
    "Pet Supplies",
    "Prime Video",
    "Shoes & Handbags",
    "Smart Home",
    "Software",
    "Sports & Outdoors",
    "Tools & Home Improvement",
    "Toys & Games",
    "Video Games",
    "Watches"
]

Pages = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "All"
]

data_list = []

HEIGHT = 500
WIDTH = 900
root = Tk()
root.title("Amazon Scraper")
canvas = Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# Adding background image
background_image = ImageTk.PhotoImage(file="C:/Users/Jagannath Wijekoon/PycharmProjects/AmazonGUI/Amazon-1.jpg")
background_label = Label(root, image=background_image).place(relwidth=1, relheight=1)


def callback_category(event):
    category_selected = str(category_dropdown.get())
    return category_selected


def callback_pages(event):
    pages_selected = str(pages_dropdown.get())
    return pages_selected


def run_scraper(search_term, category, no_pages):
    print("Search Term: ", search_term)
    print("Category: ", category)
    print("Number of Pages: ", no_pages)
    label['text'] = "Scraping Pages..."
    x = 1
    if category == Category[0]:
        url = f'https://www.amazon.ca/s?k={search_term}&ref=nb_sb_noss'
    else:
        url = f'https://www.amazon.ca/s?k={search_term}&i={category}'

    while True:
        soup = geturl(url)
        getdata(soup, data_list)
        url = amazonpagination(soup)
        x = x + 1
        print(x)
        if no_pages == 'All':
            if not url:
                print(url)
                break
            else:
                print(url)
                print(len(data_list))
            time.sleep(1)
        else:
            if not url or x > int(no_pages):
                print(url)
                break
            else:
                print(url)
                print(len(data_list))
            time.sleep(1)
    df = pd.DataFrame(data_list)
    # Finishing Message
    if url == "No Results Found! Check the Search Term or Product Category":
        label['text'] = url
    else:
        label['text'] = "Scraping Finished"
        df.to_csv(search_term + category + '.csv', encoding='utf-8')


frame = Frame(root, bg='#424651', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.1, anchor='n')

entry = Entry(frame, font=('Helvetica',12))
entry.place(relwidth=0.25, relheight=1)

button = Button(frame, text="Scrape", font=('Helvetica', 12),
                command=lambda: run_scraper(entry.get(), category_dropdown.get(), pages_dropdown.get()))
button.place(relx=0.26, relwidth=0.1, relheight=1)

category_dropdown = StringVar(frame)
category_dropdown.set(Category[0])

cat_drop = OptionMenu(frame, category_dropdown, *Category)
cat_drop.config(width=30, font=('Helvetica', 12))
cat_drop.place(relx=0.37, relheight=1)

pages_dropdown = StringVar(frame)
pages_dropdown.set(Pages[0])

p_drop = OptionMenu(frame, pages_dropdown, *Pages)
p_drop.config(width=5, font=('Helvetica', 12))
p_drop.place(relx=0.82, relwidth=0.18, relheight=1)

lower_frame = Frame(root, bg='#424651', bd=5)
lower_frame.place(relx=0.5, rely=0.225, relwidth=0.8, relheight=0.1, anchor='n')

label = Label(lower_frame)
label.place(relwidth=1, relheight=1)

root.mainloop()
