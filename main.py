import requests

import time


def auction(item,bin):
  #auction function; any and all auction functios go through this
  
  data = requests.get("https://api.hypixel.net/skyblock/auctions").json()

  list_1 = []

  def Auction(name, priceer,timer,binner):
    return({
  "Name": name,
  "Price": priceer,
  "Minutes Left": timer,
  "Bin":binner
  }
  )

  print("Retrieving auction price for "+ item +". This usually takes about 15 seconds.")
  loop1 = data['totalPages']
  loop2 = 0
  for x in range (0, loop1+1):
    
    url = "https://api.hypixel.net/skyblock/auctions?page="+str(x)
    #print(url)
    auction_data = requests.get(url).json()
    loop2 = 0
    while True:
      try:
        if item in auction_data['auctions'][loop2]['item_name']:
          is_bin = False
          if 'bin' in auction_data['auctions'][loop2]:
            is_bin = True
          else:
            is_bin = False


          if is_bin==True and not bin == 0:

            timing = int((int(auction_data['auctions'][loop2]['end'])/1000 - time.time())/60)

            list_1.append(Auction(
              auction_data['auctions'][loop2]['item_name'],
            auction_data['auctions'][loop2]['starting_bid'],timing,True
            ))
          if is_bin == False and not bin == 1:

            timing = int((int(auction_data['auctions'][loop2]['end'])/1000 - time.time())/60)
            list_1.append(Auction(
              auction_data['auctions'][loop2]['item_name'],
            auction_data['auctions'][loop2]['highest_bid_amount'],timing,False
            ))
        loop2 +=1
      except:
        break
 
  return(list_1)


def bazaar_buy(item):
  #bazaar buy price function

  bazaar_data = requests.get(
        url = "https://api.hypixel.net/skyblock/bazaar",
    ).json()

  return(float(str(bazaar_data['products'][item]['buy_summary'][0]['pricePerUnit'])))



def bazaar_sell(item):
  #bazaar sell price function

  bazaar_data = requests.get(
        url = "https://api.hypixel.net/skyblock/bazaar",
    ).json()
  
  return(float(str(bazaar_data['products'][item]['sell_summary'][0]['pricePerUnit'])))

while True:
  do = input("What would you like to do?\nType 'help' for list of commands.\n")
  if do == "help":
    print("bz - allows you to view bazzar\nah - allows you to view auction house\nahuuid - allows you to view auctions using their UUID\nflip - allows you to flip items\n")
  else:
    break

if do == "f" or do == "F" or do == "Flip" or do == "flip":

  do = input("Would you like to: (Type a number)\n1: Bazaar Flip\n")

  if do == "1":
    #bazaar flip

    do = input("Would you like to...  (Type a number)\n1: Flip by item\n2: Find an item to flip\n")

    if do == "1":
      do = input("What item would you like to flip? (Spelling matters!) ")
      do = do.upper()
      do = do.replace(' ','_')

      print("\nAll prices have 0.1 added/subtracted so your order can beat compitition.\n")

      buy_price = bazaar_buy(do)
      buy_price -= 0.1
      print("Buy Price: "+ str(round(buy_price,1)))

      sell_price = bazaar_sell(do)

      sell_price += 0.1
      print("Sell Price: "+ str(round(sell_price,1)))

      print("Profit: "+ str(round(buy_price - sell_price,1)))


    elif do == "2":
      do = input("How would you like your items sorted?  (Type a number)\n1: Alphabetically\n2: Profit per item\n3: Profit per Coin\n4: Initial investment\n5: Sales Backlog\n")
      bz_nbr = input("How many items would you like to be displayed? (Type number or 'a' for all) ")
      print("\nCollecting Bazaar Flipping Data.  This usually takes about one minute.\n")
      data=[]

      bazaar_data = requests.get(
        url = "https://api.hypixel.net/skyblock/bazaar",
      ).json()

      def Bazaar_item(number,offical_name, name ,buy_pricer,sell_pricer,sales_backlog):
        return({
      "#": number,
      "Offical Name": offical_name,
      "Name": name,
      "Sell offer Price": float(buy_pricer),
      "Buy order Price": float(sell_pricer),
      "Profit per item": round(float(buy_pricer) - float(sell_pricer),2),
      "Profit per coin": round((float(buy_pricer) - float(sell_pricer)) / float(sell_pricer),2),
      "Sales Backlog": sales_backlog
      })
      
      import items

      keys = list(items.thing)
      #print(keys[0])
      #print(items.thing[keys[0]])


      
      loop3 = 0
      bazaar_items = []
      percent = -1
      while True:

        try:
          buy_price = bazaar_buy(keys[loop3])
          buy_price -= 0.1
          buy_price = str(round(buy_price,1))

          sell_price = bazaar_sell(keys[loop3])
          sell_price += 0.1
          sell_price = str(round(sell_price,1))

          sales_backlog = round(float(bazaar_data['products'][keys[loop3]]['quick_status']['sellVolume'])/(float(bazaar_data['products'][keys[loop3]]['quick_status']['sellMovingWeek'])/7),2)

          if sales_backlog < 7 and (float(buy_price) - float(sell_price)) > 0:
            bazaar_items.append(Bazaar_item(loop3, keys[loop3], items.thing[keys[loop3]],buy_price, sell_price, sales_backlog))
          
          percent_done = int((loop3/len(keys))*100)
          if percent_done%10 == 0 and not percent == percent_done:
            print(str(percent_done) + "% Complete")
            percent = percent_done

          loop3 += 1
        except:
          break

      #sorting

      if do == "1":
        def myFunc(e):
          return e['Name']

        bazaar_items.sort(key=myFunc)

      elif do == "2":
        def myFunc(e):
          return e['Profit per item']

        bazaar_items.sort(reverse = True,key=myFunc)

      elif do == "3":
        def myFunc(e):
          return e['Profit per coin']

        bazaar_items.sort(reverse = True, key=myFunc)

      elif do == "4":
        def myFunc(e):
          return e['Buy order Price']

        bazaar_items.sort(key=myFunc)

      elif do == "5":
        def myFunc(e):
          return e['Sales Backlog']

        bazaar_items.sort(key=myFunc)


      if bz_nbr == "a":
        bz_nbr = len(bazaar_items)

      bz_nbr = int(bz_nbr)
      if bz_nbr > len(bazaar_items):
        bz_nbr = len(bazaar_items)
      

      for x in range(0,bz_nbr):
        print("Item: " + str(bazaar_items[x]['Name']) + 
        "  Buy Order Price: " + str(bazaar_items[x]['Buy order Price']) + 
        "  Sell Offer Price: " + str(bazaar_items[x]['Sell offer Price']) + 
        "  Profit Per Item: " + str(bazaar_items[x]['Profit per item']) + 
        '  Profit Per Coin ' + str(bazaar_items[x]['Profit per coin']) + 
        "  Sales Backlog: " + str(bazaar_items[x]['Sales Backlog']))




elif do == "Bazaar" or do == "bazaar" or do == "bz":
  #manual search of bazaar

  thing = input("What item would you like to search? (Spelling matters!) ")
  thing = thing.upper()
  thing = thing.replace(' ','_')

  try:
    print("Buy Price: "+str(bazaar_buy(thing)))
    print("Sell Price: "+str(bazaar_sell(thing)))
  except:
    print("Error")


elif do == "Auction" or do == "ah":
  #manual search of the auction house

  do = input("Would you like BIN, auction or both? ") 

  thing = input("What item would you like to search? (Spelling and capitilization matters!!) ")

  sort = input("How would you like your item sorted? (Type a number)\n1: Lowest Price\n2: Highest Price\n3: Ending Soon\n4: Ending Last\n")

  auct_number = input("How many auctions do you want to be displayed? (Type number of 'a' for all ")

  if do == "BIN" or do == "bin":
    data=auction(thing, 1)

  elif do == "auction": 
    data=auction(thing, 0)

  elif do == "both":
    data = auction(thing, 2)

  #sorting

  if sort == "1":
    def myFunc(e):
      return e['Price']

    data.sort(key=myFunc)

  elif sort == "2":
    def myFunc(e):
      return e['Price']

    data.sort(reverse = True, key=myFunc)

  elif sort == "3":
    def myFunc(e):
      return e['Minutes Left']

    data.sort(key=myFunc)

  elif sort == "4":
    def myFunc(e):
      return e['Minutes Left']

    data.sort(reverse = True, key=myFunc)


  if auct_number == "a":
    auct_number = len(data)

  auct_number = int(auct_number)
  if auct_number > len(data):
    auct_number = len(data)
  
  for x in range(0,auct_number):
    print(data[x])



elif do == "ahuuid":
  #auction found by auction UUID; prints raw data
  loop = 0
  loop1 = 0


  uuid = input("UUID:")
  data = requests.get("https://api.hypixel.net/skyblock/auctions").json()

  for x in range (0, loop1+1):
    
    url = "https://api.hypixel.net/skyblock/auctions?page="+str(x)

    auction_data = requests.get(url).json()
    loop2 = 0
    while True:
      try:
        if auction_data['auctions'][loop2]['uuid'] == uuid:
          print (auction_data['auctions'][loop2])
                        

        loop2 +=1
      except:
        break