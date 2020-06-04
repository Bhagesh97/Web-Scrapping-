import sys
import requests
import csv

def read_skus():
    skus = open("skus.txt","r")

    skus_list = []

    for sku in skus.readlines():
        sku = sku.replace("\n","")
        skus_list.append(sku)
    
    skus.close()

    return skus_list


if __name__ == "__main__":
    skus = read_skus()

    with open(f'{str(sys.argv[1])}.csv', mode='w') as csv_file:

        images_link = ["image1","image2","image3","image4","image5","image6","image7","image8","image9","image10",
                        "image11","image12","image13","image14","image15","image16","image17","image18","image19","image20"]

        fields = ["price","sku","name","longDescription","modelNumber","shippingWeight","image1","image2","image3","image4","image5","image6","image7","image8","image9","image10",
                        "image11","image12","image13","image14","image15","image16","image17","image18","image19","image20","Store1","Store2","Store3","Store4"
                ,"Store5","Store6","Store7","Store8","Store9","Store10","Store11","Store12","Store13","Store14","Store15","Store16","Store17"
                ,"Store18","Store19","Store20","Store21","Store22","Store23","Store24","Store25"]
        writer = csv.DictWriter(csv_file ,fieldnames = fields)
        writer.writeheader()

        for sku in skus:

            data = requests.get(f"https://api.bestbuy.com/v1/products/{sku}.json?show=salePrice,sku,name,salePrice,longDescription,modelNumber,shippingWeight,images&apiKey=pYZhC6m0Q7F98K7G5zvMHQAi")
            data = data.json()

            stores = requests.get(f"https://api.bestbuy.com/v1/products/{sku}/stores.json?postalCode=33172&apiKey=pYZhC6m0Q7F98K7G5zvMHQAi")
            stores = stores.json()

            main = {"price":data["salePrice"],"sku": data["sku"],"name": data["name"],
                    "longDescription": data["longDescription"],"modelNumber": data["modelNumber"],
                    "shippingWeight": data["shippingWeight"]}

            temp_imgs = {}
            count = 1
            for img in data["images"]:
                if "Standard" in img["rel"]:
                    temp_imgs[f"image{count}"] = img["href"]
                    count += 1 
            

            store_data = {}
            count = 1
            for index,store in enumerate(stores["stores"]):
                
                if store["lowStock"]:
                    temp_string = f'{store["name"]}={store["lowStock"]}'
                    store_data[f"Store{count}"] = temp_string
                    count +=1 
                if index == len(stores["stores"]):
                    for count in range(count,26):
                        store_data[f"Store{count}"] = "None"


            main.update(temp_imgs)
            main.update(store_data)      

            writer.writerow( main )
                
