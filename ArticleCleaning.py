# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 21:02:49 2023

@author: Daniel
"""

import pandas as pd

df = pd.read_csv(r'C:\Users\User\PycharmProjects\Thinkingpinoy\FakeNews00.csv')

import datetime

# Convert "Date" column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%B %d, %Y')

# Filter out dates before February 2019
cutoff_date = datetime.datetime(2019, 2, 1)
df = df[df['Date'] >= cutoff_date]

# Convert "Date" column to new format
df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

import re

# assuming your dataframe is called df and the column with emoji is called "Content"
df["Content"] = df["Content"].apply(lambda x: re.sub(r'[^\x00-\x7F]+', '', x))

df["Headline"] = df["Headline"].apply(lambda x: re.sub(r'[^\x00-\x7F]+', '', x))

# define the regular expression pattern
pattern = r"\([\dixv]+\)|\[[\dixv]+\]"

# apply the regular expression to remove the pattern from the text
df["Content"] = df["Content"].apply(lambda x: re.sub(pattern, "", x))
df["Headline"] = df["Headline"].apply(lambda x: re.sub(pattern, "", x))


def remove_urls(text):
    # regular expression to match URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub('', text)


# apply the function to the 'Content' column
df['Content'] = df['Content'].apply(remove_urls)


def remove_whitespace(text):
    # remove leading/trailing whitespace
    text = text.strip()
    # remove consecutive whitespace characters except single spaces
    text = re.sub(r'[\t\f\r\v]+|[ ]{2,}', ' ', text)
    # separate paragraphs with one newline character if two or more
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text.strip()


df['Content'] = df['Content'].apply(remove_whitespace)


def remove_text(text, strings_to_remove):
    for string_to_remove in strings_to_remove:
        index = text.find(string_to_remove)
        while index != -1:
            text = text[:index]
            index = text.find(string_to_remove)
    return text


remove_strings = [
    "DON'T FORGET TO SHARE!",
    'Sincerely,',
    '. *wink*',
    'For comments',
    'For reactions, ',
    'SOURCES:',

    '[RJ Nieto / ThinkingPinoy]',
    '[RJ Nieto / Thinking Pinoy]',
    '[ThinkingPinoy / RJ Nieto]',
    '[Thinking Pinoy / RJ Nieto]',

    '(RJ Nieto/ThinkingPinoy)',
    '(RJ Nieto / Thinking Pinoy)',
    '(ThinkingPinoy / RJ Nieto)',
    '(Thinking Pinoy / RJ Nieto)',

    '[ThinkingPinoy | RJ Nieto]',
    '[Thinking Pinoy | RJ Nieto]',
    '[RJ Nieto | ThinkingPinoy]',
    '[RJ Nieto | Thinking Pinoy]',

    '(ThinkingPinoy | RJ Nieto)',
    '(Thinking Pinoy | RJ Nieto)',
    '(RJ Nieto | ThinkingPinoy)',
    '(RJ Nieto | Thinking Pinoy)',

    '[ThinkingPinoy/RJ Nieto]',
    '[Thinking Pinoy/RJ Nieto]',
    '[RJ Nieto/ThinkingPinoy]',
    '[RJ Nieto/Thinking Pinoy]',

    '(ThinkingPinoy/RJ Nieto)',
    '(Thinking Pinoy/RJ Nieto)',
    '(RJ Nieto/ThinkingPinoy)',
    '(RJ Nieto/Thinking Pinoy)',

    '[ThinkingPinoy|RJ Nieto]',
    '[Thinking Pinoy|RJ Nieto]',
    '[RJ Nieto|ThinkingPinoy]',
    '[RJ Nieto|Thinking Pinoy]',

    '(ThinkingPinoy|RJ Nieto)',
    '(Thinking Pinoy|RJ Nieto)',
    '(RJ Nieto|ThinkingPinoy)',
    '(RJ Nieto|Thinking Pinoy)',

    '[Thinking Pinoy]',
    '[ThinkingPinoy]',
    '[RJ Nieto]',

    '(Thinking Pinoy)',
    '(ThinkingPinoy)',
    '(RJ Nieto)',
]

df['Content'] = df['Content'].apply(lambda x: remove_text(x, remove_strings))
df.to_csv(r'C:\Users\User\PycharmProjects\Thinkingpinoy\thinking_pinoy.csv', index = False)