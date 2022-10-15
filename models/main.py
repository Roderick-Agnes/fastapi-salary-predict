import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# loading dataset
def load_dataset():
    return pd.read_csv("dataset/salary_dataset - Sheet1.csv")

# cleaning dataset
def clean_dataset():
    dataset = load_dataset()
    # Clean null or NaN values from data frame using dropna().
    # change type of salary column to float
    
    index = 0
    dataset['salary'].dropna()
    for element in dataset['salary']:
        number = element
        if "." in number:
            # print(number.split(',')[0])
            number = number.split(',')[0]
            part = (number.replace('.', ''))
            dataset['salary'][index] = part
            index += 1

    # change type of salary column to float
    idx = 0
    for element in dataset['year_experience']:
        if "," in str(element):
            parts = element.replace(',', '.')
            dataset['year_experience'][idx] = parts
        idx += 1

    dataset['year_experience'] = pd.to_numeric(dataset['year_experience'], errors='coerce')
    dataset['year_experience'].dropna()

    dataset = dataset.dropna()
    return dataset

# Building Model
async def build_and_predict(data, type: str = 'formdata'):
    dataset = clean_dataset()
    
    x = dataset.drop('salary', axis=1)
    y = dataset['salary']

    # x.head()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    linear = LinearRegression()
    linear.fit(x_train, y_train)

    # Predict test data x_test with call function predict() and store to variable y_pred. 
    # The result is prediction salary with test data using LinearRegression.

    y_pred = linear.predict(x_test)

    print("y_pred: ", y_pred)

    # Accuracy
    accuracy = linear.score(x_test, y_test)

    if type == 'formdata':

        # Prediction salary with input data from Web Client using LinearRegression
        input_data = pd.DataFrame([data])
        print('formdata: ', input_data)
        predicted_salary = linear.predict(input_data)[0]
        # Convert decimal to integer
        if int(predicted_salary) < 0: predicted_salary = 0-int(predicted_salary)
        predicted_salary = int(predicted_salary)
        print("{:,.2f}".format(predicted_salary))

        return {
            "prediction_salary_with_test_data": y_pred.tolist(),
            "accuracy_test_prediction_salary": accuracy,
            "predicted_salary": "{:,.2f}".format(predicted_salary)
        }
    
    if type == 'singlefile':
        try:
            print('path: ')
            dataset = pd.read_csv(data)
            print("olddata: \n", dataset)
            
            # remove all column with values not is numbers
            dataset_filter = dataset.apply(pd.to_numeric, errors='coerce')
            dataset_filter = dataset_filter.dropna(axis=1)

            input_single = pd.DataFrame(dataset_filter)
            singlefile_result = linear.predict(input_single)
            # print("newdata: \n", dataset)
            dataset['salary'] = singlefile_result
            # formatted salary column
            dataset['salary'] = dataset['salary'].map('{:,.2f}'.format)

            print("newdata: \n", dataset)

            return {"data": dataset.to_dict('records')}
        except Exception:
            return {'message': "Error to handle single file"}

    else:
        return {'multi files'}

