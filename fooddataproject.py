#imports
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fdplists import micros,dvs,animalfoods,plantfoods,exceptionkws

foods = pd.read_csv("food.csv") #foodid-food
foods = foods.drop(columns=["data_type","publication_date","food_category_id"]) #sorts data set (same for 3 below)
fnuts = pd.read_csv("food_nutrient.csv", low_memory=False) #foodid-specific nutrientid
fnuts = fnuts.drop(columns=["id","data_points","derivation_id","min","max","median","footnote","min_year_acquired"])
nutrients = pd.read_csv("nutrient.csv") #nutrientid-nutrient
nutrients = nutrients.drop(columns=["nutrient_nbr","rank"])

tempdata = fnuts.merge(foods[["fdc_id","description"]],left_on="fdc_id",right_on="fdc_id") #merge food names + nutrient id
rawdata = tempdata.merge(nutrients[["id","name","unit_name"]],left_on="nutrient_id",right_on="id") #merge nutrient ids + nutrients
data = rawdata[["description","name","amount","unit_name"]].set_index(["description","name"]).sort_index() #finalizes index

def dvfunc(food,calories=False): #creates list for food's dvs, calories standardizes to 100cal
    fooddv = {} #storage
    energy = data.loc[(food, "Energy")] #all rows with food + its energy
    fooddv["Calories"] = energy.loc[energy["unit_name"] == "KCAL", "amount"].iloc[0] #standardizes to kcal, place into dict
    for i in range(22):
        try:
            row = data.loc[(food, micros[i]),"amount"] #find the row with food and its micro
        except (KeyError, IndexError):
            print(f"{food} doesn't have {micros[i]}") #exception printed if micro not found
            continue
        
        if calories == False: #going by 100g
            fooddv[micros[i]] = round(float(row.iloc[0])/dvs[i]*100,2) #turn amount into dv, insert in dict
        else: #going by 100cal
            ratio = 100/fooddv["Calories"] #conversion ratio for cal
            fooddv[micros[i]] = round(float(row.iloc[0])/dvs[i]*100*ratio,2) #same thing but use raito
    if calories == True:
        fooddv["Calories"] = 100 #set calories for 100cal
        
    totaldv = 0 #total dv completed of food
    for micro in fooddv: #add up every micro
        if micro != "Calories": #exclude calories
            if fooddv[micro]>100: #set cap for totaldv for 100
                fooddv[micro]=100.0
            totaldv += fooddv[micro]
    totaldv = round(totaldv/22,2) #find final score
    fooddv["Total"] = totaldv #add in dict
    
    foodaslist = [x.strip() for x in re.split(r"[,()]",food)] #split usda wording into list
    foodaslist = [word for word in foodaslist if word not in exceptionkws] #remove exception keywords
    fooddv["Name"] = " ".join(foodaslist[:2]) #select first 2 and remove commas
    return fooddv

def organize(flist,calories=False): #organizing table function based on food list
    lset = [] #set to store individual dvs
    for food in flist:
        lset.append(dvfunc(food,calories)) #store dvs of all foods
    dtable = pd.DataFrame(lset).set_index("Name") #make data set
    dtable = dtable.rename(columns={"Vitamin A, RAE":"Vitamin A","Vitamin C, total ascorbic acid":"Vitamin C",
                                    "Vitamin D (D2 + D3)":"Vitamin D","Vitamin E (alpha-tocopherol)":"Vitamin E",
                                    "Vitamin K (phylloquinone)":"Vitamin K","Folate, total":"Folate"}) #rename some micros
    return dtable

def compare(food1,df1,food2,df2): #compares two foods with plot
    df = pd.concat([df1.loc[food1],df2.loc[food2]], axis=1, ignore_index=False) #combine two rows
    df = df.drop("Calories") #drop calories
    print(df)
    
    ax = df.plot.barh(figsize=(8,5)) #create plot
    ax.set_xlabel("DV")
    ax.set_ylabel("Micronutrient")
    ax.invert_yaxis() #make micros in right order
    plt.show()
    
def makeset(cals):
    animal = organize(animalfoods,calories=cals).sort_values(by="Name")
    animal.loc["Median"] = round(animal.median(),2)
    plant = organize(plantfoods,calories=cals).sort_values(by="Name")
    plant.loc["Median"] = round(plant.median(),2)
    return animal,plant

def boxplot(micro,data1,data2,name):
    d1data = list(data1[micro].drop("Median"))
    d2data = list(data2[micro].drop("Median"))
    plt.boxplot([d1data,d2data],tick_labels=["Animal","Plant"])
    plt.title(name)
    print(f"Animal 5N Sum = {np.percentile(d1data,[0,25,50,75,100])}")
    print(f"Plant 5N Sum = {np.percentile(d2data,[0,25,50,75,100])}")
    plt.show()

animal,plant = makeset(False)
canimal,cplant = makeset(True)
plant.to_csv("gplant.csv", index=True)
animal.to_csv("ganimal.csv", index=True)
cplant.to_csv("calplant.csv", index=True)
canimal.to_csv("calanimal.csv", index=True)