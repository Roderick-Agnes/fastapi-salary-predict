from utils.libs import *

# loading dataset
def load_dataset():
    dataset = pd.read_csv("dataset/salary_dataset - Sheet1.csv")
    return dataset

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

    # dataset['knowledge'].dropna()
    # dataset['technical'].dropna()
    # dataset['logical'].dropna()
    # dataset['year_experience'].dropna()

    dataset = dataset.dropna()
    return dataset

# Building Model
def build_and_predict(data):
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

    print(x_test)

    # Accuracy
    accuracy = linear.score(x_test, y_test)

    # Prediction salary with input data from Web Client using LinearRegression
    input_data = pd.DataFrame([data])
    predicted_salary = linear.predict(input_data)[0]
    # Convert decimal to integer
    if int(predicted_salary) < 0: predicted_salary = 0-int(predicted_salary)
    predicted_salary = int(predicted_salary)
    print("{:,.2f}".format(predicted_salary))

    return {
        "prediction_salary_with_test_data": y_pred.tolist(),
        "accuracy_test_prediction_salary": accuracy,
        "predicted_salary": predicted_salary
    }

