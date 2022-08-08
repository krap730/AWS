import json
import boto3

#実行するための情報を記入
comprehend = boto3.client(service_name='comprehend', 
                                             region_name='ap-northeast-1',
                                             aws_access_key_id="*******************",
                                             aws_secret_access_key="*******************")
 
def get_sentiment_score(target):
    sentiment = comprehend.detect_sentiment(Text=target, LanguageCode='ja')
    return sentiment.get('SentimentScore')
 
if __name__ == "__main__":
    try:
        # jsonファイルの読み込み
        json_open = open('sample.json', 'r')
        body = json.load(json_open)
         
        for i in range(len(body)):
            text = body[i]['text']
            # 感情分析を実行
            try:
                body[i].update(get_sentiment_score(text))
            except Exception as e:
                print( e)
                try:
                    # エンコード
                    ebcoded_text = text.encode('utf-8')
                    # 5000bytesまで行ける
                    sliced_text = ebcoded_text[:5000]
                    # デコード
                    decoded_text = sliced_text.decode('utf-8')
                    # 再度実行
                    body[i].update(get_sentiment_score(decoded_text))
                except Exception as e:
                    #それでも無理なら諦め
                    print(e)
                
        content = sorted(body, key=lambda x:x['Positive'], reverse=True) # 降順
        print(content)
         
    except Exception as e:
        print(e)
        raise e