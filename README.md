# Data Engineer Certification - Practical Exam - Supplement Experiments
Datacamp Data Engineer Certification

## Task

1001-Experiments currently has the following four datasets with four months of data:

- `"user_health_data.csv"` which logs daily health metrics, habits and data from wearable devices,
- `"supplement_usage.csv"` which records details on supplement intake per user,
- `"experiments.csv"` which contains metadata on experiments, and
- `"user_profiles.csv"` which contains demographic and contact information of the users.

Each dataset contains unique identifiers for users and/or their supplement regimen.

The developers and data scientists currently manage code that cross-references all of these data sources separately, which is cumbersome and error-prone.

Your manager has asked you to write a Python function that cleans and merges these datasets into a single dataset.

The final dataset should provide a comprehensive view of each user's health metrics, supplement usage, and demographic information.

- To test your code, your manager will run only the code:  
  ```python
  merge_all_data('user_health_data.csv', 'supplement_usage.csv', 'experiments.csv', 'user_profiles.csv')

