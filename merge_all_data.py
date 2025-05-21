# import libraries
import pandas as pd

# function
def merge_all_data(user_health_file, supplement_usage_file, experiments_file, user_profiles_file):
    # Step 1: Read the datasets
    user_health_data = pd.read_csv(user_health_file)
    supplement_usage = pd.read_csv(supplement_usage_file)
    experiments = pd.read_csv(experiments_file)
    user_profiles = pd.read_csv(user_profiles_file)

    #Step 2a: data cleaning - drop na data if any
    user_profiles = user_profiles.dropna(subset=['user_id', 'email'])
    user_health_data = user_health_data.dropna(subset=['user_id', 'date'])
    supplement_usage = supplement_usage.dropna(subset=['user_id', 'date'])

    #Step 2b: data cleaning - convert 'date' to datetime format
    user_health_data['date'] = pd.to_datetime(user_health_data['date'])
    supplement_usage['date'] = pd.to_datetime(supplement_usage['date'])
    user_health_data['date'] = user_health_data['date'].dt.strftime('%Y-%m-%d')
    supplement_usage['date'] = supplement_usage['date'].dt.strftime('%Y-%m-%d')

    #Step 2c: data cleaning - data type cleaning
    # user_health_data['sleep_hours']
    user_health_data['sleep_hours'] = user_health_data['sleep_hours'].str.replace('h', '', case=False)
    user_health_data['sleep_hours'] = pd.to_numeric(user_health_data['sleep_hours'], errors='coerce').where(pd.notnull(user_health_data['sleep_hours']), None)

    #Step 2d: data cleaning - unit conversion - dosage
    supplement_usage['dosage_grams'] = supplement_usage.loc[supplement_usage['dosage_unit'] == 'mg', 'dosage'] / 1000


    #Step 2d: data cleaning - add age groups
    def age_group(age):
        if pd.isna(age):
            return 'Unknown'
        elif age < 18:
            return 'Under 18'
        elif 18 <= age <= 25:
            return '18-25'
        elif 26 <= age <= 35:
            return '26-35'
        elif 36 <= age <= 45:
            return '36-45'
        elif 46 <= age <= 55:
            return '46-55'
        elif 56 <= age <= 65:
            return '56-65'
        else:
            return 'Over 65'
    user_profiles['user_age_group'] = user_profiles['age'].apply(age_group)

    #Step 3: join tables
    merged_df = user_profiles.merge(user_health_data, left_on='user_id', right_on='user_id', how='left', suffixes=('_user_profiles', '_user_health'))
    merged_df = merged_df.merge(supplement_usage, on=['user_id', 'date'], how='left', suffixes=('', '_supplement_usage'))
    merged_df = merged_df.merge(experiments, left_on='experiment_id', right_on='experiment_id', how='left', suffixes=('', '_experiments'))

    #Step 4 fill NAs after join
    merged_df['supplement_name'] = merged_df['supplement_name'].fillna('No intake')

    #Step 5: final output - columns selction and rename
    final_df = merged_df[['user_id', 'date', 'email', 'user_age_group', 'name', 'supplement_name', 'dosage_grams', 'is_placebo', 'average_heart_rate', 'average_glucose', 'sleep_hours', 'activity_level']]
    final_df = final_df.rename(columns={'name': 'experiment_name'})

    return final_df
