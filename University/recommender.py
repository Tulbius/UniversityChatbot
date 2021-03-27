import pandas as pd
import numpy as np
import sklearn.metrics.pairwise as pw
import gspread

from oauth2client.service_account import ServiceAccountCredentials

def initialization():
    university = pd.read_csv('Word_University_Rank_2020.csv', encoding="UTF-8")
    df = pd.DataFrame(university)
    df['Number_students'] = df['Number_students'].apply(lambda x: x.replace(',','.'))
    df['Number_students'] = df['Number_students'].astype(float, errors = 'raise')
    df = normalization(df)
    df = df.drop('Rank_Char', axis=1)
    df = df.drop('Overall_Ranking', axis=1)
    df['Number_students'] = round(df['Number_students'], 5)
    df['Numb_students_per_Staff'] = round(df['Numb_students_per_Staff'], 5)
    df['Teaching'] = round(df['Teaching'], 5)
    df['Research'] = round(df['Research'], 5)
    df['Citations'] = round(df['Citations'], 5)
    df['Industry_Income'] = round(df['Industry_Income'], 5)
    df['International_Outlook'] = round(df['International_Outlook'], 5)
    return df

def pred(df):
    df_pred = df.copy()
    df_pred = df_pred.drop(df.iloc[:, 0:3], axis=1)
    df_pred = df_pred.drop(df.iloc[:, 4:8], axis=1)
    df_pred = df_pred.drop(df.iloc[:, 13:], axis=1)
    return df_pred

def normalization(df):
    df['Number_students'] = df['Number_students']/np.sqrt(df['Number_students'])
    df['Numb_students_per_Staff'] = df['Numb_students_per_Staff']/np.sqrt(df['Numb_students_per_Staff'])
    df.iloc[:,9:15] = df.iloc[:,9:15]/np.sqrt(df.iloc[:,9:15])
    return df

def prediction(nb,t,r,c,i,o, df_pred):
    u = df_pred[df_pred['Number_students'] == nb]
    score = [0,0,0]
    univ_rank = [0,0,0]
    for univ in df_pred['Number_students'] :
        if univ !=nb:
            U = df_pred[df_pred['Number_students'] == univ]
            if (pw.cosine_similarity(u,U)[0][0] > score[0]):
                score[2] = score[1]
                univ_rank[2] = univ_rank[1]
                score[1] = score[0]
                univ_rank[1] = univ_rank[0]
                score[0] = float(pw.cosine_similarity(u,U)[0][0])
                univ_rank[0] = univ
            elif (pw.cosine_similarity(u,U)[0][0] > score[1])  :
                score[2] = score[1]
                univ_rank[2] = univ_rank[1]
                score[1] = float(pw.cosine_similarity(u,U)[0][0])
                univ_rank[1] = univ
            elif (pw.cosine_similarity(u,U)[0][0] > score[2]):
                score[2] = float(pw.cosine_similarity(u,U)[0][0])
                univ_rank[2] = univ
    return univ_rank

def univ_names(result,df):
    L = []
    for i in result:
        L.append(df[df['Number_students'] == i].iloc[0,1])
    return L

def authentication():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("universe").sheet1  # Open the spreadhseet
    data = sheet.get_all_records()  # Get a list of all records
    df_result = pd.DataFrame(data)
    return df_result

def recommendation(df_result,df_pred,df):
  #normalization
  nb = int(df_result.iloc[0,1]) / np.sqrt(int(df_result.iloc[0,1]))
  t = int(df_result.iloc[0,2]) / np.sqrt(int(df_result.iloc[0,2]))
  r = int(df_result.iloc[0,3]) / np.sqrt(int(df_result.iloc[0,3]))
  c = int(df_result.iloc[0,4]) / np.sqrt(int(df_result.iloc[0,4]))
  i = int(df_result.iloc[0,5]) / np.sqrt(int(df_result.iloc[0,5]))
  o = int(df_result.iloc[0,6]) / np.sqrt(int(df_result.iloc[0,6]))
  df_res = df_pred.append({'Number_students': nb, 'Teaching': t, 'Research': r, 'Citations': c, 'Industry_Income': i, 'International_Outlook': o}, ignore_index=True)
  #prediction
  result = prediction(nb,t,r,c,i,o, df_res)
  recommendations = univ_names(result,df)
  return recommendations

def delete(df_result):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("universe").sheet1  # Open the spreadhseet
    sheet.delete_rows(2)

def result():
    df = initialization()
    df_pred = pred(df)
    df_result = authentication()
    return recommendation(df_result, df_pred, df)