import pandas as pd

file_path = '../Datasets/data1.csv'
dataset_1 = pd.read_csv(file_path, na_values=['N/A'])
# print(dataset_1.head())


# Exploring the data by assessing its shape
print(dataset_1.shape)

# changing the columns names
rename_column_names = {'1. What is your age?': 'Age', '2. Gender': 'Gender',
                       '3. Relationship Status': 'Relationship Status', '4. Occupation Status': 'Occupation Status',
                       '5. What type of organizations are you affiliated with?': 'Students',
                       '6. Do you use social media?': 'use_social_media',
                       '7. What social media platforms do you commonly use?': 'Social Media Platforms',
                       '8. What is the average time you spend on social media every day?': 'Time Spent',
                       '9. How often do you find yourself using Social media without a specific purpose?':
                           'Use Social Media without Purpose',
                       '10. How often do you get distracted by Social media when you are busy doing something?':
                           'Often you get distracted by social media',
                       '11. Do you feel restless if you havent used Social media in a while?':
                           'Restless level with no social media',
                       '12. On a scale of 1 to 5, how easily distracted are you?': 'Distraction level',
                       '13. On a scale of 1 to 5, how much are you bothered by worries?': 'Worries Level',
                       '14. Do you find it difficult to concentrate on things?': 'Concentration level',
                       '15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media?': 'Comparison Level',
                       '16. Following the previous question, how do you feel about these comparisons, generally '
                       'speaking?': 'Comparison Feeling',
                       '17. How often do you look to seek validation from features of social media?': 'Validation',
                       '18. How often do you feel depressed or down?': 'Depression level',
                       '19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate?':
                           'Fluctuation of Interest in daily activities',
                       '20. On a scale of 1 to 5, how often do you face issues regarding sleep?': 'Sleep Issues level'}

df = dataset_1.rename(columns=rename_column_names)

# Remove empty rows and time stamp
print((df == 'N/A').sum())
df = df.drop(columns=['Timestamp'])
# print(df.columns)
# Filter out users who answered 'No' to using social media
df = df[df['use_social_media'] != 'No']


# Remove salaried worker (approved), and retired (approved) (Included)
# change school student variable to University student
print(df['Occupation Status'])
print(df['Occupation Status'].value_counts())
print(df['Social Media Platforms'].unique)
print(df['Gender'].unique)

# for df['Occupation Status'] in df:
#  if df['Occupation Status'] == '':

# Remove the gap (nan, N/A), remove Company, Government , (approved)
# Change private, school to University (approved)
column = df['Students']
print(column.unique())
print(column.value_counts())
print(df.columns)
# df = df[~df['Students'].isin(['University, N/A', 'School, N/A'])]
# print(df.shape)

print(df.dtypes)


def checking_rows(df, column1, column2, choice1, choice2):
    for index, row in df.iterrows():
        if row[column1] == choice1 and row[column2] == choice2:
            print(True)
        else:
            print(False)


# checking_rows(df, 'Occupation Status', 'Students', 'Salaried', 'School')
# checking_rows(df, 'Occupation Status', 'Students', 'retired', 'School')

# Splitting the social media platforms used
df['Social Media Platforms'] = df['Social Media Platforms'].str.split(',')
social_media_dummies = df['Social Media Platforms'].explode().str.strip().str.lower().str.capitalize()
social_media_dummies = pd.get_dummies(social_media_dummies)
df = df.drop(columns=['Social Media Platforms']).join(social_media_dummies.groupby(level=0).sum())
print(df.columns)

file_path1 = '../Datasets/mediarates.xlsx'
df1 = pd.read_excel(file_path1)
# print(len(df1))
df1 = df1.dropna()
print(len(df1))

platform_cols = ['Discord', 'Facebook', 'Instagram', 'Pinterest',
                 'Reddit', 'Snapchat', 'Tiktok', 'Twitter', 'Youtube']
# Check for rows where all platform columns are 0
# Filter users who don't use any social media
no_social_users = df[df['use_social_media'] == 'No']
print(df['Use Social Media without Purpose'].dtype)

# Display the count
print(f"Number of users who don't use any social media: {len(no_social_users)}")
#
# dataset2_table = dash_table.DataTable(
#     id="dataset2-table",
#     columns=[
#         {"id": "user_id", "name": "user_id", "type": "numeric"},
#         {"id": "post_type", "name": "post_type", "type": "text"},
#         {"id": "post_length", "name": "post_length", "type": "numeric"},
#         {"id": "likes", "name": "likes", "type": "numeric"},
#         {"id": "comments", "name": "comments", "type": "numeric"},
#         {"id": "shares", "name": "shares", "type": "numeric"},
#         {"id": "engagement_rate", "name": "engagement_rate", "type": "numeric"},
#         {"id": "user_followers", "name": "user_followers", "type": "numeric"},
#         {"id": "post_category", "name": "post_category", "type": "text"},
#         {"id": "post_hour", "name": "post_hour", "type": "numeric"},
#         {"id": "is_weekend", "name": "is_weekend", "type": "numeric"},
#         {"id": "user_verified", "name": "user_verified", "type": "numeric"},
#         {"id": "spam_flag", "name": "spam_flag", "type": "numeric"},
#     ],
#     data=df1.to_dict('records'),
#     page_size=10,
#     style_table={"overflowX": "auto"},
#     style_cell={"textAlign": "left", "padding": "6px"},
# )
