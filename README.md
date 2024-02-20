# Flexible-Slotting-of-Customer-Time-Windows
All python files contained in this repository have been implemented in the Python 3.11 version. As DIE PyCharm was used. 

## 1. Running the Application
In order to execute the application and run main.py, some files have to be moved in different folders:
- dataset: The customer data set which should be used must be imported into the folder "import" (.../datasets/dataSets_CSV/import) --> *Note: For variant 3, the datasets from the folder .../datasets/dataSets_CSV/No CPTS must be used*
- variant: The variant which should be executed must the moved into the main folder and the respective name (v2 for variant 2 etc.) must be entered in line 8 in the main.py:
  > versionen = ['v2']

Once those files are moved and the variant name is entered, there can be a dataSetName (*excelOutput/excelOutput_'+version+'_'+datasetName+'.csv*) chosen for the output. The output which will be stored in the folder "excelOutput". 

- With the function "excelAllVersions" the customers are slotted
  
- With the function "orToolAllVersions" the vehicle routing with time windows is executed and the exact route is defined, the total distance of the route and the total time are calculated.
*Note: In the file "orToolsVRPTW.py" the number of delivery vehicles can be adjusted in line 34*
    > data['num_vehicles'] = 1

- The function "orToolAllVersionsdirect" is used for the Benchmark approach and the vehicle routing with time windows is directly executed without the execution of the different variantsnd the exact route is defined, the total distance of the route and the total time are calculated.

## 2. Creating (new) Data Sets
To create the customer data set, the file "createRandomDatset.py" from the folder "dataset" must be used.
To change the number of customers (currently it is 70 customers minutes), the number of customers must be adjusted in line 3
  > numberOfCustomers = 70

In the file "randomSetGenerator.py" the customer types and delivery time range for each customer type are defined, the x- and y-coordinates, the delivery time, the willingness to wait and price sensitivy for each customer are defined 

The file "csvBuilder.py" then creates a csv-file with the mentioned charactics 
> header = ["id", "xCoord", "yCoord", "custType", "delDate", "delTime", "willingToWait", "deliveryWindows", "priceSens"]

and stores the file in the folder "dataset".

## 3. Use of Python packages:
I used the following Python packages:
- matplotlib (version: 3.7.1)
- ortools (version: 9.5.2237)
