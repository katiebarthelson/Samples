from google.cloud import language
from google.cloud import language_v1
from google.cloud.language import enums, types
import csv
import pandas as pd

def analyze_text_sentiment(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    sentiment = response.document_sentiment
    results = [
        ('text', text),
        ('score', sentiment.score),
        ('magnitude', sentiment.magnitude),
    ]
    return results[1:3]

def analyze_text_syntax(text): #Not used at the moment
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_syntax(document=document)
    fmts = '{:10}: {}'
    print(fmts.format('sentences', len(response.sentences)))
    print(fmts.format('tokens', len(response.tokens)))
    for token in response.tokens:
        part_of_speech_tag = enums.PartOfSpeech.Tag(token.part_of_speech.tag)
        print(fmts.format(part_of_speech_tag.name, token.text.content))

def classify(text, verbose=True):
    """Classify the input text into categories. """
    language_client = language_v1.LanguageServiceClient()

    document = types.Document(
        content=text, type=enums.Document.Type.PLAIN_TEXT
    )
    if(len(text.split())>=20):
        response = language_client.classify_text(document=document)
        categories = response.categories
        result = []
        for category in categories:
            result.append((category.name,category.confidence))
        if(len(result)>0):
            return result
        else:
            return [("Unknown",0.0)]
    else:
        return [("Unknown",0.0)]

def analyze_text_entities(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document)
    all_entities = []
    for entity in response.entities:
        results = [
            ('name', entity.name),
            ('type', enums.Entity.Type(entity.type).name),
            ('salience', entity.salience),
            ('wikipedia_url', entity.metadata.get('wikipedia_url', '-')),
            ('mid', entity.metadata.get('mid', '-')),
        ]
        all_entities.append(results)
    return all_entities

def analyze_entity_sentiment(text_content):
    """
    Analyzing Entity Sentiment in a String

    Args:
      text_content The text content to analyze
    """
    client = language_v1.LanguageServiceClient()
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entity_sentiment(document, encoding_type=encoding_type)
    all_entities = []
    for entity in response.entities:
        sentiment = entity.sentiment
        results = [
            ('name', entity.name),
            ('type', enums.Entity.Type(entity.type).name),
            ('salience', entity.salience),
            ('wikipedia_url', entity.metadata.get('wikipedia_url', '-')),
            ('mid', entity.metadata.get('mid', '-')),
            ('sentiment',sentiment.score),
            ('magnitude',sentiment.magnitude)
        ]
        all_entities.append(results)
    return all_entities

def main():
    client = language.LanguageServiceClient.from_service_account_json('Cashification-ca6444f5e291.json')
    df = pd.read_csv('raw_tweets_text.csv')
    df2 = pd.DataFrame(columns =['id','Entity','Type','Salience','EntSentiment','EntMagnitude'])
    df['Sentiment'] = 0
    df['Magnitude'] = 0
    df['Category'] = ''
    df['Confidence'] = 0 #category confidence
    first_few = 0 #counter for testing purposes
    i = 0
    for index, row in df.iterrows():
         score,magnitude = analyze_text_sentiment(row[1])
         sk,sv = score
         mk,mv = magnitude
         category = classify(row[1])
         cat,conf = category[0]
         df.loc[index,['Category']] = cat
         df.loc[index,['Confidence']] = conf
         df.loc[index,['Sentiment']] = sv
         df.loc[index,['Magnitude']] = mv
         entities = analyze_entity_sentiment(row[1])
         for entity in entities:
             i += 1
             df2.loc[i,['id']] = row[0]
             n,ent = entity[0]
             df2.loc[i,['Entity']] = ent
             t,type = entity[1]
             df2.loc[i,['Type']] = type
             s,sal = entity[2]
             df2.loc[i,['Salience']] = sal
             entsent,entsentiment = entity[5]
             df2.loc[i,['EntSentiment']] = entsentiment
             entmag,entmagnitude = entity[6]
             df2.loc[i,['EntMagnitude']] = entmagnitude
         first_few += 1
         if first_few > 1000:
             print(df.head())
             print(df2.head())
             break
    df.to_csv('NLP_Out_RawText.csv', index=False)
    df2.to_csv('Salience_RawText.csv', index=False)

if __name__ == "__main__":
    main()
