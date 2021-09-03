import requests
import time


def auction(item,bin):
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



  #print(auction_data['auctions'][0])
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
        #print("Player "+str(loop2)+"complete")
      except:
        break
 
  return(list_1)


def bazaar_buy(item):
  bazaar_data = requests.get(
        url = "https://api.hypixel.net/skyblock/bazaar",
    ).json()

  return(int((bazaar_data['products'][item]['buy_summary'][0]['pricePerUnit'])))



def bazaar_sell(item):
  bazaar_data = requests.get(
        url = "https://api.hypixel.net/skyblock/bazaar",
    ).json()

  return(int((bazaar_data['products'][item]['sell_summary'][0]['pricePerUnit'])))

while True:
  do = input("What would you like to do?\nType 'help' for list of commands.\n")
  if do == "help":
    print("bz - allows you to view bazzar\nah - allows you to view auction house\nahuuid - allows you to view auctions using their UUID\nflip - allows you to flip items\n")
  else:
    break

if do == "f" or do == "F" or do == "Flip" or do == "flip":

  do = input("What would you like to flip? ")

  if do == "super compactor":
    
    compactor_price=bazaar_buy("ENCHANTED_COBBLESTONE")*448+bazaar_buy("ENCHANTED_REDSTONE_BLOCK")

    print("Price: "+ str(compactor_price))

    compactor_sell = bazaar_sell("SUPER_COMPACTOR_3000")
    
    print("Sell Price: " + str(compactor_sell))

    profit = compactor_sell - compactor_price

    print("Profit: "+str(profit))

  elif do == "candle":
    enchnated_acacia_price = bazaar_buy("ENCHANTED_ACACIA_LOG")
    enchanted_coal_price = bazaar_buy("ENCHANTED_COAL")

    candle_price = enchnated_acacia_price*6 + enchanted_coal_price
    print("Candle Price: "+str(candle_price))

    price = int(auction("Repelling Candle",True))
    
    print("Sell Price: "+str(price))

    print("Profit: "+str(price - candle_price))



  elif do == "golem":
    #golem_bin =  auction("Golem Armor Helmet", True)
    #print(golem_bin)
    golem_not_bin = auction("Golem Armor Helmet", False)
    print(golem_not_bin)
    
    



elif do == "Bazaar" or do == "bazaar" or do == "bz":
  thing = input("What item would you like to search? (Spelling matters! ")
  thing = thing.upper()
  thing = thing.replace(' ','_')

  try:
    print("Buy Price: "+str(bazaar_buy(thing)))
    print("Sell Price: "+str(bazaar_sell(thing)))
  except:
    print("Error")


elif do == "Auction" or do == "ah":
  do = input("Would you like BIN, auction or both? ") 

  thing = input("What item would you like to search? (Spelling and capitilization matters!!) ")

  sort = input("How would you like your item sorted? (Type a number)\n1: Lowest Price\n2: Highest Price\n3: Ending Soon\n4: Ending Last\n")

  auct_number = input("How many auctions do you want displayed? ")

  if do == "BIN" or do == "bin":
    data=auction(thing, 1)

  elif do == "auction": 
    data=auction(thing, 0)

  elif do == "both":
    data = auction(thing, 2)


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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

elif do == "ahuuid":
  loop = 0
  loop1 = 0


  uuid = input("UUID:")
  data = requests.get("https://api.hypixel.net/skyblock/auctions").json()

  for x in range (0, loop1+1):
    
    url = "https://api.hypixel.net/skyblock/auctions?page="+str(x)
    #print(url)
    auction_data = requests.get(url).json()
    loop2 = 0
    while True:
      try:
        if auction_data['auctions'][loop2]['uuid'] == uuid:
          print (auction_data['auctions'][loop2])
                        

        loop2 +=1
        #print("Player "+str(loop2)+"complete")
      except:
        break
