import requests
import json
import random

class Multilinguist:
  """This class represents a world traveller who knows 
  what languages are spoken in each country around the world
  and can cobble together a sentence in most of them
  (but not very well)
  """

  translatr_base_url = "http://bitmakertranslate.herokuapp.com"
  countries_base_url = "https://restcountries.eu/rest/v2/name"
  #{name}?fullText=true
  #?text=The%20total%20is%2020485&to=ja&from=en

  def __init__(self):
    """Initializes the multilinguist's current_lang to 'en'
    
    Returns
    -------
    Multilinguist
        A new instance of Multilinguist
    """
    self.current_lang = 'en'

  def language_in(self, country_name):
    """Uses the RestCountries API to look up one of the languages
    spoken in a given country

    Parameters
    ----------
    country_name : str
         The full name of a country.

    Returns
    -------
    bool 
        2 letter iso639_1 language code.
    """
    params = {'fullText': 'true'}
    response = requests.get(f"{self.countries_base_url}/{country_name}", params=params)
    json_response = json.loads(response.text)
    return json_response[0]['languages'][0]['iso639_1']

  def travel_to(self, country_name):
    """Sets current_lang to one of the languages spoken
    in a given country

    Parameters
    ----------
    country_name : str
        The full name of a country.

    Returns
    -------
    str
        The new value of current_lang as a 2 letter iso639_1 code.
    """
    local_lang = self.language_in(country_name)
    self.current_lang = local_lang
    return self.current_lang

  def say_in_local_language(self, msg):
    """(Roughly) translates msg into current_lang using the Transltr API

    Parameters
    ----------
    msg : str
        A message to be translated.

    Returns
    -------
    str
        A rough translation of msg.
    """
    params = {'text': msg, 'to': self.current_lang, 'from': 'en'}
    response = requests.get(self.translatr_base_url, params=params)
    json_response = json.loads(response.text)
    return json_response['translationText']

class MathGenius(Multilinguist):

  total_number = 0

  def __init__(self, list_of_numbers):
    super().__init__()
    for number in list_of_numbers:
      self.total_number +=  number

  
  def report_total(self):
    return "The total is {}".format(self.total_number) 

class QuoteCollector(Multilinguist):
  quotes = ["There is nothing permanent except change.", 
          "The secret of getting ahead is getting started.",
          "No act of kindness, no matter how small, is ever wasted.",
          "If you cannot do great things, do small things in a great way."
          ]

  def __init__(self, country_name, msg):
    super().__init__()
    pass 
  
  def add_quote(self, new_quote):
    self.quotes.append(new_quote)

  def report_quote(self):
    return random.choice(self.quotes)


my_numbers = [6, 4, 9]
me = Multilinguist()
print(me.language_in("Canada"))
me.travel_to("India")
print(me.say_in_local_language("Hello"))

you = MathGenius([23,45,676,34,5778,4,23,5465])
you.report_total()

print(you.language_in("Canada"))
you.report_total() # The total is 12048
you.travel_to("Italy")
print(you.report_total()) # È Il totale 1030767
us = QuoteCollector("Canada", "There is nothing permanent except change.")
print(us.language_in("Canada"))
print(us.report_quote())
us.travel_to("France")
print(us.report_quote())