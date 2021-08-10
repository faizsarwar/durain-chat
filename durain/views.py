from sqlite3.dbapi2 import Cursor
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import sys
from . import db



def index(request):
	# return render(request, 'arithmetic/home.html')
    return HttpResponse("hello from chatapp durains")


@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)
    # get query from json
    queryresult=req.get('queryResult')
    # get action from json
    action = queryresult.get('action')


    def get_info(action):  # yes intents keliye  #connect db
        address=queryresult.get('parameters').get('address')
        phone=queryresult.get('parameters').get('phone-number')
        name=queryresult.get('parameters').get('person').get('name')
        quantity=queryresult.get('parameters').get('unit-weight').get('amount')
        quantity_unit=queryresult.get('parameters').get('unit-weight').get('unit')
        durain=''.join(action).split(".")[0]                    #fetching durain name from action 
        delivery_time=datetime.datetime.now() + datetime.timedelta(days=1)
        db.insert_order(name,phone,address,quantity,quantity_unit,durain,delivery_time)
        fulfillmentText={'fulfillmentText': "thanks. your order will arrive at {}  approx ".format(delivery_time)}
        return fulfillmentText


    def get_feedback(): #connect db
        phone=queryresult.get('parameters').get('phone-number')
        name=queryresult.get('parameters').get('person').get('name')
        feedback=queryresult.get('parameters').get('any')
        db.insert_feedback(name,phone,feedback)
        fulfillmentText={'fulfillmentText': "Your feedback is very valuable for us thanks !!"}
        #store feedback in db
        return fulfillmentText


    def give_response(item:str): #connect db 
      item=db.get_duarin_details_and_image_uri(item)

      #fetch details from db
      db_details=[item[0]]
      # fetch image uri from db
      db_image_url=item[1]
      fulfillmentText = {
        "fulfillmentMessages":[
        {
        "text": {
          "text": db_details
        }
        },
        { 
        "image": {
          "imageUri":db_image_url
                }
        },
       {
        "quickReplies": {
          "quickReplies": [
          "Yes",
          "No"
                        ]
                      }
        }      
      ]
      }
      return fulfillmentText


    def get_promotions(): #connect db
        #fetch prormo from db
        promotions=db.get_promotions()
        text="promotion offer is : {} , vailidity is  {} ".format(promotions[0],promotions[1])
        fulfillmentText={'fulfillmentText': text}
        return fulfillmentText




    if action=="welcome" : #image + suggestionchip show hungi
        fulfillmentText = {
        "fulfillmentMessages":[                  
        {
        "text": {
          "text": [
            "Hello from Quin Durain shop we provide high quality Fresh Durains directly imported from farms we have all types of Durains with cash on delivery options available \n      \n        Black Gold , Black Pearl or Tai Yuan , Lipan , Golden Phoenix , Capri , Red Prawn or Ang Hae , Green Bamboo or Tekka , D24 or Sultan , Mao Shan Wang , King of Kings , TSW , Tawa , Kunpo , Black Thorn , D13 , Tupai King , XO (Johor)."
          ]
        }
        },

        { 
        "image": {
          "imageUri": "https://cdn-a.william-reed.com/var/wrbm_gb_food_pharma/storage/images/publications/food-beverage-nutrition/foodnavigator-asia.com/headlines/processing-packaging/durians-take-on-technology-as-singapore-start-up-turns-king-of-fruits-into-traceable-digital-assets/9950065-1-eng-GB/Durians-take-on-technology-as-Singapore-start-up-turns-King-of-Fruits-into-traceable-digital-assets_wrbm_large.jpg"
                }
        },      
       {
        "quickReplies": {
          "quickReplies": [
            "Black Gold",
            "Black Pearl or Tai Yuan",
            "Lipan",
            "Golden Phoenix",
            "Capri",
            "Red Prawn or Ang Hae",
            "Green Bamboo or Tekka",
            "D24 or Sultan",
            "Mao Shan Wang",
            "King of Kings",
            "TSW",
            "Tawa",
            "Kunpo",
            "Black Thorn",
            "D13",
            "Tupai King",
            "XO (Johor)"
                        ]
                      }
        }
      ]
    }

    elif action=="feedback":
        fulfillmentText=get_feedback()

    elif action=="promotions":
        fulfillmentText=get_promotions()

    #saray yes walay yhn catch krwaonga fulfillment text bhi is fn mai hi return krwado 
    elif action=="BlackGold.BlackGold-yes" or action=="BlackPearlorTaiYuan.BlackPearlorTaiYuan-yes" or action=="BlackThorn.BlackThorn-yes" or action=="Capri.Capri-yes" or action=="D13.D13-yes" or action=="D24orSultan.D24orSultan-yes" or action=="GoldenPhoenix.GoldenPhoenix-yes" or action=="GreenBambooorTekka.GreenBambooorTekka-yes" or action=="KingofKings.KingofKings-yes" or action=="Kunpo.Kunpo-yes" or action=="Lipan.Lipan-yes" or action=="MaoShanWang.MaoShanWang-yes" or action=="RedPrawnorAngHae.RedPrawnorAngHae-yes" or action=="Tawa.Tawa-yes" or action=="TSW.TSW-yes" or action=="TupaiKing.TupaiKing-yes" or action=="XOJohor.XOJohor-yes":  
        fulfillmentText=get_info(action)

    #baghair yes walay direct function mai bhej k details show db sya show and image show url from db
    else:                               
    	fulfillmentText = give_response(action)


    # return response
    return JsonResponse(fulfillmentText, safe=False)