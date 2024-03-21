
import numpy as np

#Global constants
#---here we set all fixed values according to the discussion in chapter 5---
fractionLoadingSpace = 22.71 / 176.68 #fraction of loading space in m³
riskFreeRate = 0.0053 #rate as decimal number
marketRiskPremium = 0.048 #rate as decimal number
initialInvestmentTotal = 80000 #Euro
initialInvestmentSavingsBank = 41129.58 #Euro
buildingSize = 1674.24 * fractionLoadingSpace #m²
salaries = 28050 * fractionLoadingSpace #Euro
fuelCost = (240 * 50)/100 * 11.9 * 1.1 #Euro 240 tours, 50kM, 11.9L/100km, fuel price net 1.1 Euro/L
maintenanceCost = (50000/1.19) * fractionLoadingSpace #Euro
insuranceCost = (50000/1.19) * fractionLoadingSpace #Euro
electricityCost = 38177.57 * fractionLoadingSpace #Euro
mealsKantinePerYear = 82695 #number of meals
mealsToGoPerYear = 75536 #number of meals
mealsKindertafelPerYear = 3270 #number of meals
mealsPerYear = (mealsKantinePerYear + mealsToGoPerYear + mealsKindertafelPerYear) * fractionLoadingSpace #number of meals
wasteSaved = 1560 * fractionLoadingSpace # metric tons
waisteSavedEuro = 190.4 * wasteSaved #Euro
numberOfGuests = 84638 # visits per year (not unique visitors, but visits per year))
numberOfFoodPackages = 0.7 * numberOfGuests * fractionLoadingSpace #number of food packages in 
averageVisitsPerYear = 1096  #Average visits per year per guest
proportionOfMaleGuests = (numberOfGuests / averageVisitsPerYear) * 0.49 * fractionLoadingSpace   #persons / unique vistors
proportionOfFemaleGuests = (numberOfGuests / averageVisitsPerYear) * 0.51 * fractionLoadingSpace #persons / unique vistors
lifeExpectancyMale = 78.2 #years
ageAverageMale = 43.4 #years
expectedRemainingLifetimeMale = lifeExpectancyMale - ageAverageMale #years
lifeExpectancyFemale = 82.9 #years
ageAverageFemale = 46.0 #years
expectedRemainingLifetimeFemale =  lifeExpectancyFemale - ageAverageFemale #years
numberOfGuestsKindertafel = 30 #persons
ageAverageChildren = 11 #years
proportionOfMaleGuestsKinderTafel = numberOfGuestsKindertafel  * 0.49 * fractionLoadingSpace #persons
proportionOfFemaleGuestsKinderTafel = numberOfGuestsKindertafel * 0.51 * fractionLoadingSpace #persons
expectedRemainingLifetimeFemaleChildren = lifeExpectancyFemale - ageAverageChildren #year
expectedRemainingLifetimeMaleChildren = lifeExpectancyMale - ageAverageChildren #years

#Global variables & lists
discountRates = []
rentBuilding = []
valueMeals = []
valueFoodPackages = []
healthCosts = []
cashFlowCosts = []
cashFlowBenefits = []
cashFlowNetBenefits = []
cashFlowHealthCostsSaved=[]
cashFlowsMealsAlternative=[]
PVHealthCostsSaved = []
PvCosts = []
PvBenefits = []
PvNetBenefits = []
PvMealsAlternative =[]

# This main function is the entry point
def main():
    print('----Social Impact Measurement----')
    print('---Feasible Values/Assumptions---')
    print(f'The expected remaining life time for male children is {expectedRemainingLifetimeMaleChildren:.2f} years')
    print(f'The expected remaining life time for female children is {expectedRemainingLifetimeFemaleChildren:.2f} years')
    print(f'The expected remaining life time for male adults is {expectedRemainingLifetimeMale:.2f} years')
    print(f'The expected remaining life time for female adults is {expectedRemainingLifetimeFemale:.2f} years')
    setPossibleValues()
    print('---------------------------------')
    calculateCashFlows()
    calculatePVs()
    print('---------------------------------')
    calculateSROIs()
    print('---------------------------------')
    calculateRobinHoodBenefitCostRatio()
    print('---------------------------------')
    calculateBacoRatios()
    print('---------------------------------')

#Here we set the permissible values for all variables that cannot be determined exactly and should instead be considered in ranges.
def setPossibleValues():         
    for beta in np.arange(0.4,1.7,0.1):
        discountRates.append(capm(riskFreeRate, beta, marketRiskPremium))
    for discountRate in discountRates:
        print(f'The discount rate is: {discountRate*100:.2f}%')
        
 
    for rentPerSquareMeter in range(15,31,1):
        rentBuilding.append(rentPerSquareMeter*buildingSize)
    for rent in rentBuilding:
        print(f'The rent for the building is: {rent:.2f} Euro')
        
    
    for valueMeal in np.arange(2.0,3.1,1):
        valueMeals.append(valueMeal*mealsPerYear)
    for value in valueMeals:
        print(f'The value of the meals is: {value:.2f} Euro')
        
    for valueFoodpackage in np.arange(9.0,20.0,1):
        valueFoodPackages.append(valueFoodpackage*numberOfFoodPackages)
    for value in valueFoodPackages:
        print(f'The value of the food packages is: {value:.2f} Euro')
    
    print(f'The fuel costs are: {fuelCost:.2f} Euro')
    print(f'The maintenance costs are: {maintenanceCost:.2f} Euro')
    print(f'The insurance costs are: {insuranceCost:.2f} Euro')
    print(f'The electricity costs are: {electricityCost:.2f} Euro')
    print(f'The waste costs saved are: {wasteSaved:.2f} Euro')

    for costs in range(16,33,1):
        healthCosts.append(costs); 
        print(f'The saved health costs are: {costs:.2f} Euro')
       
#Here we calculate the surplus of all costs and monetized impacts          
def calculateCashFlows():
    for rent in rentBuilding:
        for meals in valueMeals:
            for foodPackages in valueFoodPackages:
                for costs in healthCosts:
                    cashFlowHealthCostsSaved.append(costs)
                    cashFlowCosts.append(rent + salaries  + fuelCost +maintenanceCost + insuranceCost + electricityCost)
                    cashFlowBenefits.append(meals + foodPackages + waisteSavedEuro)
                    cashFlowNetBenefits.append(meals + foodPackages + waisteSavedEuro - (rent + salaries  + fuelCost +maintenanceCost + insuranceCost + electricityCost))    
                    cashFlowsMealsAlternative.append(meals/fractionLoadingSpace)
                
#Here we calcualte present values
def calculatePVs():   
    for discountRate in discountRates:   
        print(f'Calculate all possible cashflows with a discount rate of {discountRate*100:.2f}%')    
        idx = -1
        for cashFlow in cashFlowHealthCostsSaved:
            idx += 1 
            #female children
            timeSeriesFemaleChildren = []
            for i in np.arange(1,expectedRemainingLifetimeFemaleChildren,1):
                timeSeriesFemaleChildren.append(cashFlow * proportionOfFemaleGuestsKinderTafel)
            
            #male children
            timeSeriesMaleChildren = []
            for i in np.arange(1,expectedRemainingLifetimeMaleChildren,1):
                timeSeriesMaleChildren.append(cashFlow * proportionOfMaleGuestsKinderTafel)
            
            #female adults  
            timeSeriesFemale = []
            for i in np.arange(1,expectedRemainingLifetimeFemale,1):
                timeSeriesFemale.append(cashFlow * proportionOfFemaleGuests)
            
            #male adults
            timeSeriesMale = []
            for i in np.arange(1,expectedRemainingLifetimeMale,1):
                timeSeriesMale.append(cashFlow * proportionOfMaleGuests)
                             
            PVHealthCostsSaved.append(npv(timeSeriesFemaleChildren, discountRate)
                                 +npv(timeSeriesMaleChildren, discountRate)
                                 +npv(timeSeriesFemale,discountRate)
                                 +npv(timeSeriesMale,discountRate))
        
            timeSeriesCosts = []            
            for i in range(1,6,1):
                timeSeriesCosts.append(cashFlowCosts[idx])
            PvCosts.append(npv(timeSeriesCosts,discountRate))

            timeSeriesBenefits = [] 
            for i in range(1,6,1):               
                timeSeriesBenefits.append(cashFlowBenefits[idx])
            PvBenefits.append(npv(timeSeriesBenefits, discountRate) + PVHealthCostsSaved[-1])
            
            timeSeriesNetBenefits = []
           
            for i in range(1,6,1):               
                timeSeriesNetBenefits.append(cashFlowNetBenefits[idx])
            PvNetBenefits.append(npv(timeSeriesNetBenefits, discountRate) + PVHealthCostsSaved[-1])
            
            PvMealsAlternative.append(cashFlowsMealsAlternative[idx])  
                 
def calculateSROIs():   
    srois = []
    print(np.min(cashFlowNetBenefits))
    print(np.max(cashFlowNetBenefits))
    print(len(cashFlowNetBenefits))
    print(np.min(PvNetBenefits))
    print(np.max(PvNetBenefits))
    print(len(PvNetBenefits))
    for pv in PvNetBenefits:
        srois.append(sroi(pv, initialInvestmentTotal))        
    print("SROI Combinations:", len(srois))
    print("SROI MIN:", np.min(srois))
    print("SROI MAX:", np.max(srois))
    print("SROI AVG:", np.average(srois))
    print("SROI Median:", np.median(srois))
    print("SROI Std Dev:", np.std(srois))
    
def calculateRobinHoodBenefitCostRatio():
   robinHoodBenefitCostRatios = []
   for pv in PvBenefits:
       robinHoodBenefitCostRatios.append(benefitCostRatio(pv,initialInvestmentTotal,initialInvestmentSavingsBank))
   print("Robin Hood BCR Combinations:", len(robinHoodBenefitCostRatios))
   print("Robin Hood BCR MIN:", np.min(robinHoodBenefitCostRatios))
   print("Robin Hood BCR MAX:", np.max(robinHoodBenefitCostRatios))
   print("Robin Hood BCR AVG:", np.average(robinHoodBenefitCostRatios))
   print("Robin Hood BCR Median:", np.median(robinHoodBenefitCostRatios))
   print("Robin Hood BCR Std Dev:", np.std(robinHoodBenefitCostRatios))
   
def calculateBacoRatios():
   BacoRatios = []
   idx = -1
   for pv in PvBenefits:
       idx += 1
       BacoRatios.append(baco(pv,initialInvestmentTotal, PvMealsAlternative[idx]))
   print("Baco Combinations:", len(BacoRatios))
   print("Baco MIN:", np.min(BacoRatios))
   print("Baco MAX:", np.max(BacoRatios))
   print("Baco AVG:", np.average(BacoRatios))
   print("Baco Median:", np.median(BacoRatios))
   print("Baco Std Dev:", np.std(BacoRatios))       
            
def npv(cashFlows, discountRate):
    #Loop through the cash flows and discount them  
    npv = 0
    for i in range(len(cashFlows)):
        npv += cashFlows[i] / (1 + discountRate) ** (i+1)    #i+1 because i starts at zero but first payment is in t=1
    return npv

def capm(riskFreeRate, beta, marketRiskPremium):
    #Calculate the expected return using the Capital Asset Pricing Model
    return riskFreeRate + beta * marketRiskPremium

def sroi(impacts, costs):
    #Calculate the Social Return on Investment
    return impacts / costs
            
def benefitCostRatio(impacts, initialInvestmentTotal, initialInvestmentSelf ):
    #Calculate the Benefit-Cost Ratio
    benefitCostRatio = impacts / initialInvestmentSelf
    robinHoodBcRatio = (initialInvestmentSelf / initialInvestmentTotal)
    robinHoodBenefits = robinHoodBcRatio * benefitCostRatio
    return robinHoodBenefits

def baco(impacts, initialInvestmentTotal, mealsAlternative):
     #Calculate the Best Available Charitable Option
    socialImpactProject = impacts
    socialImpactComparison = (initialInvestmentTotal / 300000) * mealsAlternative
    baco = (initialInvestmentTotal / socialImpactComparison) / (initialInvestmentTotal / socialImpactProject)
    return baco   
      
# Check if this file is run as the main program
if __name__ == "__main__":
# Call the main function
    main()
