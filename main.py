# -*- coding: utf-8 -*-
"""
Created on Tue 22 August 2023

@author: Xuefei Han
"""
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    index_df = pd.read_csv("D:/PycharmProjects/written_test/data/index_df.csv")
    index_df = index_df.rename(columns={'Unnamed: 0': "Date", 'index': "idx_price"})

    # final result dataframe yearly
    annual_stats = pd.DataFrame(
        columns=['Year', 'Annual_Return', 'Annual_Volatility', 'Sharpe_Ratio', 'Max_Drawdown', 'Max_Drawdown_Start', 'Max_Drawdown_End'])

    # convet the str date to datetime for yearly stat
    index_df['Date'] = pd.to_datetime(index_df['Date'], format='%Y%m%d')
    index_df['Year'] = index_df['Date'].dt.year

    # calculate stat for each year
    for year in index_df['Year'].unique():

        sub_df = index_df[index_df['Year'] == year]

        sub_df.loc[:, 'Daily_Return'] = sub_df['idx_price'].pct_change().fillna(0)
        if len(sub_df) < 200:
            annual_return = np.prod(1 + sub_df['Daily_Return']) - 1
        else:
            annual_return = np.prod(1 + sub_df['Daily_Return']) ** (252 / len(sub_df)) - 1
        annual_volatility = np.std(sub_df['Daily_Return']) * np.sqrt(252)
        sharpe_ratio = annual_return / annual_volatility

        # max drawdown
        sub_df.loc[:, 'Cumulative_Return'] = (1 + sub_df['Daily_Return']).cumprod()
        cumulative_max = np.maximum.accumulate(sub_df['Cumulative_Return'])
        drawdown = (cumulative_max - sub_df['Cumulative_Return']) / cumulative_max
        max_drawdown = drawdown.max()
        end_date_index = drawdown.idxmax()
        end_date = sub_df.loc[end_date_index, 'Date']
        start_date_index = sub_df.loc[:end_date_index, 'Cumulative_Return'].idxmax()
        start_date = sub_df.loc[start_date_index, 'Date']

        annual_stats.loc[len(annual_stats)] = [year, annual_return, annual_volatility, sharpe_ratio, max_drawdown, start_date, end_date]
    annual_stats.columns = ['年份', '年化收益率(%)', '年化波动率(%)', '夏普比率', '最大回撤(%)', '最大回撤开始日期', '最大回撤结束日期']
    annual_stats['最大回撤开始日期'] = annual_stats['最大回撤开始日期'].dt.strftime('%Y%m%d')
    annual_stats['最大回撤结束日期'] = annual_stats['最大回撤结束日期'].dt.strftime('%Y%m%d')
    avg=annual_stats.mean(axis=0,numeric_only=True)
    avg['年份']='all'
    annual_stats=annual_stats.append(avg,ignore_index=True)


    # print(annual_stats)
