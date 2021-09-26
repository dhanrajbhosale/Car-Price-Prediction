from flask import Flask, render_template, request
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
    
        Owner_Type=request.form['Owner_Type']
        Fuel_Type=request.form['Fuel_Type']
        Seller_Type=request.form['Seller_Type']

        if(Owner_Type=='Second'):
                owner_Second=1
                owner_Third=0
                owner_Fourth_Plus=0
                owner_Test_Drive=0
        elif(Owner_Type=='Third'):
                owner_Second=0
                owner_Third=1
                owner_Fourth_Plus=0
                owner_Test_Drive=0
        elif(Owner_Type=='Fourth_Plus'):
                owner_Second=0
                owner_Third=0
                owner_Fourth_Plus=1
                owner_Test_Drive=0
        elif(Owner_Type=='Test_Drive'):
                owner_Second=0
                owner_Third=0
                owner_Fourth_Plus=0
                owner_Test_Drive=1
        else:
                owner_Second=0
                owner_Third=0
                owner_Fourth_Plus=0
                owner_Test_Drive=0

        if(Fuel_Type=='Petrol'):
                fuel_Petrol=1
                fuel_Diesel=0
                fuel_LPG=0
                fuel_Electric=0
        elif(Fuel_Type=='Diesel'):
                fuel_Petrol=0
                fuel_Diesel=1
                fuel_LPG=0
                fuel_Electric=0
        elif(Fuel_Type=='LPG'):
                fuel_Petrol=0
                fuel_Diesel=0
                fuel_LPG=1
                fuel_Electric=0
        elif(Fuel_Type=='Electric'):
                fuel_Petrol=0
                fuel_Diesel=0
                fuel_LPG=0
                fuel_Electric=1
        else:
                fuel_Petrol=0
                fuel_Diesel=0
                fuel_LPG=0
                fuel_Electric=0

        Year=2020-Year

        if(Seller_Type=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Trustmark_Dealer=0
        elif(Seller_Type=='tDealer'):
            Seller_Type_Individual=0
            Seller_Type_Trustmark_Dealer=1
        else:
            Seller_Type_Individual=0
            Seller_Type_Trustmark_Dealer=0	
        Transmission=request.form['Transmission']
        if(Transmission=='Mannual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0

        prediction=model.predict([[Kms_Driven2,Year,fuel_Diesel,fuel_Electric,fuel_LPG,fuel_Petrol,Seller_Type_Individual,Seller_Type_Trustmark_Dealer,Transmission_Manual,owner_Fourth_Plus,owner_Second,owner_Test_Drive,owner_Third]])
        output=round(prediction[0],2)
        
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

