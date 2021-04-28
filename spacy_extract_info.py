from nltk.corpus import stopwords
import re
import spacy
nlp = spacy.load('en_core_web_lg')

def extract_info(sentence):
    
    text = ''
    for i in range(len(sentence)):
        if i < len(sentence)-1:
            if sentence[i].isalpha() and sentence[i+1].isnumeric():
                text = text+sentence[i]+' '
            elif sentence[i+1]=='$':
                text = text+sentence[i]+' '
            else:    
                text = text + sentence[i]  
    
    
    text = re.sub(r'\w+\$', '$', text)
    dates = list(set(' '.join([' '.join(re.findall(r'\d{4}',ent.text)) for ent in nlp(text).ents if ent.label_=='DATE']).split(' ')))
    cagr = [ent.text for ent in nlp(text).ents if ent.label_=='PERCENT']
    market_value = list(set([num[num.index('$'):] for num in [ent.text for ent in nlp(text).ents if ent.label_=='CARDINAL' or ent.label_=='MONEY'] if '$' in num]))
    location = [ent[0].text for ent in nlp(text).ents if ent.label_=='GPE']
    
    forecast_date = None
    current_date = None
    if dates:
        if len(dates)>1:
            for date in dates:
                if date > '2020':
                    forecast_date = date
                elif date <= '2020':
                    current_date = date
        else:
            if dates[0]>'2020':
                forecast_date = dates[0]
            else:
                current_date = dates[0]
                
    if cagr:
        cagr = cagr[0]
    else:
        cagr = None
        
    current_market_value = None
    forecast_market_value = None
    if market_value:
        for val in market_value:
            if current_date is not None and forecast_date is not None:
                current_val = abs(text.index(val) - text.index(current_date))
                forecast_val = abs(text.index(val) - text.index(forecast_date))
                if forecast_val<current_val:
                    forecast_market_value = val
                else:
                    current_market_value = val
            else:
                if forecast_market_value is not None:
                    if text.index(val) > text.index(forecast_market_value):
                        forecast_market_value = val
                        current_market_value = forecast_market_value
                else:
                    forecast_market_value = val
    
  
    if location:
        if 'china' in text.lower():
            location.append('china')
    elif 'global' in text.lower() or 'worldwide'.lower() in text:
        location = 'global'
    else:
        location = None		
		
    
    
    return {'CAGR':cagr, 'Market_value':forecast_market_value, 'Current_year':current_date, 'Forecast_year':forecast_date,
            'location':location}
