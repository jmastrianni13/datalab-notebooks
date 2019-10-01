# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 21:53:58 2019

@author: JMastrianni
"""
    
class TransformTweetPdf:

    def rm_char_repeat(tweet_df, df_column):
        """
        Replaces all consecutive 3+ same char with one char
        in input string
        eg: "helloooo" => "hello"
        """
        import string
        
        df_copy = tweet_df.copy()
        
        REPETITION_REGEX = { ch : 3*ch for ch in string.ascii_lowercase }
        
        for char, pattern in REPETITION_REGEX.items():
            df_copy[df_column] = df_copy[df_column].str.replace(pattern, char, regex = True)
            
            
        return df_copy
    
    def rm_urls(tweet_df, df_column):
        """
        Removes URLs from input string
        """
        
        return tweet_df[df_column].str.replace(r"http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+", "", regex = True)
    
    def rm_emoticons(tweet_df, df_column):
        """
        Removes emoticons from input string
        """
        
        return tweet_df[df_column].str.replace(r'[:=;][oO\-]?[D\)\]\(\]/\\OpP]', "", regex = True)  
    
    
    def rm_ats(tweet_df, df_column):
        """
        Removes @s from input string
        """        
        
        return tweet_df[df_column].str.replace(r'(?:@[\w_]+)', "", regex = True)
    
    
    def tokenize(tweet_df, df_column):
        from sklearn.feature_extraction.text import CountVectorizer
        
        vectorizer = CountVectorizer()
        
        vectorizer.fit(tweet_df[df_column])
        
        tweetvector = vectorizer.transform(tweet_df[df_column])
        
        words = vectorizer.get_feature_names()
        
        return pd.DataFrame(tweetvector.toarray(), columns = words)

if __name__ == '__main__':
    import string
    import pandas as pd
    
    test_list = ["https://www.toremove.com :D @joe just some plain text " + 3*ch for ch in string.ascii_lowercase]
    test_df = pd.DataFrame()
    test_df['tweettext'] = test_list
    
    print("Original", '/n', test_df)
    
    test_df['tweettext'] = TransformTweetPdf.rm_char_repeat(test_df, 'tweettext')
    
    print("Removed repeating characters", '\n',test_df)

    test_df['tweettext'] = TransformTweetPdf.rm_ats(test_df, 'tweettext')

    print("Removed @s", '\n',test_df)
    
    test_df['tweettext'] = TransformTweetPdf.rm_urls(test_df, 'tweettext')
    
    print("Removed urls", '\n',test_df)
        
    test_df['tweettext'] = TransformTweetPdf.rm_emoticons(test_df, 'tweettext')
    
    print("Removed emoticons", '\n', test_df)
    
    test = TransformTweetPdf.tokenize(test_df, 'tweettext')


