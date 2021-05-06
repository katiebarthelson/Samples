# -*- coding: utf-8 -*-
# Homework 11 - ISYE 6501
# Part 1 ----------------------------------------------------------------------
# Formulate an optimization model (a linear program) to find the cheapest diet 
# that satisfies the maximum and minimum daily nutrition constraints, and solve
# it using PuLP. Turn in your code and the solution. (The optimal solution 
# should be a diet of air-popped popcorn, poached eggs, oranges, raw iceberg 
# lettuce, raw celery, and frozen broccoli. UGH!) 
import pulp
import pandas as pd
diet = pd.DataFrame.from_csv('diet.csv', index_col=['Foods'])
diet = diet[0:64]
# Convert currency values to a float
def convert_currency(val):
    new_val = val.replace(',','').replace('$', '')
    return float(new_val)
diet['Price/ Serving'] = diet['Price/ Serving'].apply(convert_currency)
dietcols = diet.columns.values.tolist()
# Identify Nutrients
nutrients = dietcols[2:12]
# Identify Foods
food = diet.index.values.tolist()
# Build dictionaries for all food to nutrient pairs
price = dict(zip(food,diet['Price/ Serving']))
calories = dict(zip(food,diet['Calories']))
cholesterol = dict(zip(food,diet['Cholesterol mg']))
fat = dict(zip(food,diet['Total_Fat g']))
sodium = dict(zip(food,diet['Sodium mg']))
carbs = dict(zip(food,diet['Carbohydrates g']))
fiber = dict(zip(food,diet['Dietary_Fiber g']))
protein = dict(zip(food,diet['Protein g']))
vitA = dict(zip(food,diet['Vit_A IU']))
vitC = dict(zip(food,diet['Vit_C IU']))
calcium = dict(zip(food,diet['Calcium mg']))
iron = dict(zip(food,diet['Iron mg']))
# instantiate problem class
lp_diet = pulp.LpProblem("Cheapest diet", pulp.LpMinimize)
# Define variables and non-negativity constraint
eat = pulp.LpVariable.dicts("Eat", food,lowBound=0, cat='Continuous')
# Define objective function
lp_diet += (pulp.lpSum([price[f] * eat[(f)] for f in food]))
# Define Constraints
# 'Calories' constraints
lp_diet += (pulp.lpSum([calories[f] * eat[(f)] for f in food])) >= 1500
lp_diet += (pulp.lpSum([calories[f] * eat[(f)] for f in food])) <= 2500
# 'Cholesterol mg' constraints
lp_diet += (pulp.lpSum([cholesterol[f] * eat[(f)] for f in food])) >=30
lp_diet += (pulp.lpSum([cholesterol[f] * eat[(f)] for f in food])) <= 240
# 'Total_Fat g' constraints
lp_diet += (pulp.lpSum([fat[f] * eat[(f)] for f in food])) >= 20
lp_diet += (pulp.lpSum([fat[f] * eat[(f)] for f in food])) <= 70
# 'Sodium mg' constraints
lp_diet += (pulp.lpSum([sodium[f] * eat[(f)] for f in food])) >= 800
lp_diet += (pulp.lpSum([sodium[f] * eat[(f)] for f in food])) <= 2000
# 'Carbohydrates g' constraints
lp_diet += (pulp.lpSum([carbs[f] * eat[(f)] for f in food])) >= 130
lp_diet += (pulp.lpSum([carbs[f] * eat[(f)] for f in food])) <= 450
# 'Dietary_Fiber g' constraints
lp_diet += (pulp.lpSum([fiber[f] * eat[(f)] for f in food])) >= 125
lp_diet += (pulp.lpSum([fiber[f] * eat[(f)] for f in food])) <= 250
# 'Protein g' constraints
lp_diet += (pulp.lpSum([protein[f] * eat[(f)] for f in food])) >= 60
lp_diet += (pulp.lpSum([protein[f] * eat[(f)] for f in food])) <= 100
# 'Vit_A IU' constraints
lp_diet += (pulp.lpSum([vitA[f] * eat[(f)] for f in food])) >= 1000
lp_diet += (pulp.lpSum([vitA[f] * eat[(f)] for f in food])) <= 10000
# 'Vit_C IU' constraints
lp_diet += (pulp.lpSum([vitC[f] * eat[(f)] for f in food])) >= 400
lp_diet += (pulp.lpSum([vitC[f] * eat[(f)] for f in food])) <= 5000
# 'Calcium mg' constraints
lp_diet += (pulp.lpSum([calcium[f] * eat[(f)] for f in food])) >= 700
lp_diet += (pulp.lpSum([calcium[f] * eat[(f)] for f in food])) <= 1500
# 'Iron mg' constraints
lp_diet += (pulp.lpSum([iron[f] * eat[(f)] for f in food])) >= 10
lp_diet += (pulp.lpSum([iron[f] * eat[(f)] for f in food])) <= 40
# Show the problem defined
#print lp_diet
# Solve the problem
lp_diet.solve()
print pulp.LpStatus[lp_diet.status]
# View the solution
print('Chosen Diet - showing selected food only')
for variable in lp_diet.variables():
    if variable.varValue != 0:
        print "{} = {}".format(variable.name, variable.varValue)
print('Total Cost')
print pulp.value(lp_diet.objective)

# Part 2 ----------------------------------------------------------------------
# Please add to your model the following constraints (which might require 
# adding more variables) and solve the new model:
# a. If a food is selected, then a minimum of 1/10 serving must be chosen. 
# (Hint: now you will need two variables for each food i: whether it is chosen,
# and how much is part of the diet. You’ll also need to write a constraint to 
# link them.) 
# b. Many people dislike celery and frozen broccoli. So at most one, 
# but not both, can be selected. 
# c. To get day-to-day variety in protein, at least 3 kinds of 
# meat/poultry/fish/eggs must be selected. [If something is ambiguous 
# (e.g., should bean-and-bacon soup be considered meat?), just call it whatever
# you think is appropriate – I want you to learn how to write this type of 
# constraint, but I don’t really care whether we agree on how to classify 
# foods!]
# instantiate problem class
lp_diet2 = pulp.LpProblem("Cheapest diet", pulp.LpMinimize)
# Define variables
eat2 = pulp.LpVariable.dicts("eat2", food,lowBound=0, cat='Continuous')
# add variable to choose foods conditionally
included = pulp.LpVariable.dicts("included",food,0,1,cat='Integer')
# Define objective function
lp_diet2 += (pulp.lpSum([price[f] * eat2[(f)] for f in food]))
# Define Constraints
# 'Calories' constraints
lp_diet2 += (pulp.lpSum([calories[f] * eat2[(f)] for f in food])) >= 1500
lp_diet2 += (pulp.lpSum([calories[f] * eat2[(f)] for f in food])) <= 2500
# 'Cholesterol mg' constraints
lp_diet2 += (pulp.lpSum([cholesterol[f] * eat2[(f)] for f in food])) >=30
lp_diet2 += (pulp.lpSum([cholesterol[f] * eat2[(f)] for f in food])) <= 240
# 'Total_Fat g' constraints
lp_diet2 += (pulp.lpSum([fat[f] * eat2[(f)] for f in food])) >= 20
lp_diet2 += (pulp.lpSum([fat[f] * eat2[(f)] for f in food])) <= 70
# 'Sodium mg' constraints
lp_diet2 += (pulp.lpSum([sodium[f] * eat2[(f)] for f in food])) >= 800
lp_diet2 += (pulp.lpSum([sodium[f] * eat2[(f)] for f in food])) <= 2000
# 'Carbohydrates g' constraints
lp_diet2 += (pulp.lpSum([carbs[f] * eat2[(f)] for f in food])) >= 130
lp_diet2 += (pulp.lpSum([carbs[f] * eat2[(f)] for f in food])) <= 450
# 'Dietary_Fiber g' constraints
lp_diet2 += (pulp.lpSum([fiber[f] * eat2[(f)] for f in food])) >= 125
lp_diet2 += (pulp.lpSum([fiber[f] * eat2[(f)] for f in food])) <= 250
# 'Protein g' constraints
lp_diet2 += (pulp.lpSum([protein[f] * eat2[(f)] for f in food])) >= 60
lp_diet2 += (pulp.lpSum([protein[f] * eat2[(f)] for f in food])) <= 100
# 'Vit_A IU' constraints
lp_diet2 += (pulp.lpSum([vitA[f] * eat2[(f)] for f in food])) >= 1000
lp_diet2 += (pulp.lpSum([vitA[f] * eat2[(f)] for f in food])) <= 10000
# 'Vit_C IU' constraints
lp_diet2 += (pulp.lpSum([vitC[f] * eat2[(f)] for f in food])) >= 400
lp_diet2 += (pulp.lpSum([vitC[f] * eat2[(f)] for f in food])) <= 5000
# 'Calcium mg' constraints
lp_diet2 += (pulp.lpSum([calcium[f] * eat2[(f)] for f in food])) >= 700
lp_diet2 += (pulp.lpSum([calcium[f] * eat2[(f)] for f in food])) <= 1500
# 'Iron mg' constraints
lp_diet2 += (pulp.lpSum([iron[f] * eat2[(f)] for f in food])) >= 10
lp_diet2 += (pulp.lpSum([iron[f] * eat2[(f)] for f in food])) <= 40
# Part a - minimum of 1/10 serving must be chosen
for f in food:
    eat2[f]>= included[f]*0.1
# Part b. only choose either broccoli or celery
lp_diet2 += included['Frozen Broccoli']+included['Celery, Raw']<=1
# Part c - require three types of protein
lp_diet2 += included['Tofu']+included['Roasted Chicken']
+included['Poached Eggs']+included['Scrambled Eggs']+included['Bologna,Turkey']
+included['Frankfurter, Beef']+included['Ham,Sliced,Extralean']
+included['Kielbasa,Prk']+included['Hamburger W/Toppings']
+included['Hotdog, Plain']+included['Peanut Butter']+included['Pork']
+included['Taco']+included['Sardines in Oil']+included['White Tuna in Water']
+included['Chicknoodl Soup']+included['Splt Pea&Hamsoup']
+included['Vegetbeef Soup']+included['Neweng Clamchwd']
+included['New E Clamchwd,W/Mlk']+included['Beanbacn Soup,W/Watr'] >=3
# Show the problem defined
# print lp_diet2
# Solve the problem
lp_diet2.solve()
print pulp.LpStatus[lp_diet2.status]
# View the solution
print('Chosen Diet additional constraints- showing selected food only')
for variable in lp_diet2.variables():
    if variable.varValue != 0:
        print "{} = {}".format(variable.name, variable.varValue)
print('Total Cost')
print pulp.value(lp_diet2.objective)
