import requests
import lxml.html

# set url for scraping
url = 'https://www.nsetropicals.com/product-category/restocks/'

# set header for web scrape
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# request the web page
html = requests.get(url, headers=header)
    
# create HtmlElement object
doc = lxml.html.fromstring(html.text)

# create list to store plant data
data = []
    
def get_plant_list(doc):
    
    # Parse page for ul of plants
    plant_parent_list = doc.xpath('//*[@id="shop"]/div/ul')[0]

    # Parse ul for li(s) of the plants
    plant_list = plant_parent_list.xpath('//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')
    
    # iterate through plantsList to grab data for individual plants
    for plant in plant_list:
        try:
            plants = {}
            title = plant.xpath('.//h2[@class="woocommerce-loop-product__title"]/text()')[0]
            if plant.xpath('.//span[@class="onsale"]'):
                price = plant.xpath('.//span[@class="price"]/del/span/bdi/text()')[0]
                salesPrice = plant.xpath('.//span[@class="price"]/ins/span/bdi/text()')[0]
            else:
                price = plant.xpath('.//span[@class="price"]/span/bdi/text()')[0]
                salesPrice = 'none'
            if plant.xpath('.//p[@class="out-of-stock"]'):
                stock = 'Out of Stock'
            else:
                stock = "In Stock"
            # Add plants to dict and store in list
            plants["Title"] = title
            plants["Price"] = price
            plants["Sales Price"] = salesPrice
            plants["Stock"] = stock
            data.append(plants)
        except:
            print('Unable to parse list, please check xpath values and try again.')
            
    return data
            
def print_plant_list(list):
    # create method to print plant list 
    for info in data:
        try:
            print(info, end='\n\n')
        except:
            print('Plant list is empty, please check stock')
            
def restocked(data, doc):
    
    # Get updated plant list
    plant_list = get_plant_list(doc)
    
    # Create list to hold out of stock items for comparison
    out_of_stock = []
    restocked = []
    
    # Grab out of stock plants
    for info in data:
        if info['Stock'] == 'Out of Stock':
            out_of_stock.append(info)
    
    # Check stock see if plant stock has been updated
    for restock in out_of_stock:
        for plant in plant_list:
            if restock['Title'] == plant['Title']:
                if restock['Stock'] != plant['Stock']:
                    restocked.append(restock)

    # clear outOfStock list for list comphrehension 
    out_of_stock.clear()
    [out_of_stock.append(x) for x in restocked if x not in out_of_stock]
    
    
    # Print out items if are now in stock
    for i in out_of_stock:
        print(f"{i['Title']} is back in stock!")
    
        
def new_plant_stock(data, doc):
    
    # Get updated plant list
    plant_list = get_plant_list(doc)
    
    # Create list to store the new plant products
    new_plants = []
    
    # Compare data and plantList if Plant from Plantlist is not in data add to newPlants
    [new_plants.append(x) for x in data if x not in plant_list]
    
    # Iterate through new plants and update user
    for plant in new_plants:
        if new_plants:
            print(f"{plant['Title']} is a new product")
        else:
            continue
    
    
# scheduling same code to run multiple
# times after every 1 minute
def job():
    print("Tracking Products....")
    print_plant_list(get_plant_list(doc))
    # Simulate item being added back in stock
    # for info in data:
    #     if info['Stock'] == 'Out of Stock':
    #         info['Stock'] = 'In Stock'
    #     else:
    #         continue
    restocked(data, doc)
    new_plant_stock(data, doc)
    
if __name__ == "__main__":
    job()