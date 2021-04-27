# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import os
from fnmatch import fnmatch
from SPARQLWrapper import SPARQLWrapper, JSON
from rasa_core_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHello(Action):

     def name(self) -> Text:
         return "topic_from_course_info1"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        c=str(tracker.slots['course'])
        query="""
            prefix sch: <http://focu.io/schema#/>
            SELECT ?topicn
            WHERE {
             ?topic sch:coveredInCourse sch:"""+c+""".
             ?topic sch:topicName ?topicn.
        }ORDER BY(?topic)
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        t=[]
        #print(results)
        if results['results']['bindings']==[]:
            ans="No related data available!"
        else:
            for result in results['results']['bindings']:
                for key, value in result.items():
                    t.append(str(value['value']))
            ans="The topics are: "
            for i in range(0,len(t)):
                ans=ans+str(t[i])+" ,"
        dispatcher.utter_message(text=ans)

        return []
    

    
class ActionHello(Action):

     def name(self) -> Text:
         return "topic_from_lectureNo_info2"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        from SPARQLWrapper import SPARQLWrapper, JSON
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        course=str(tracker.slots['course'])
        no=str(tracker.slots['number'])
        no="'"+no+"'"
        query="""
                  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  prefix sch: <http://focu.io/schema#/>
        
                   SELECT ?topic_label ?resource
                   WHERE {
                      ?lecture sch:lectNumber """+no+"""^^xsd:int.
                      ?lecture sch:forCourse sch:"""+course+""".
                      ?d rdfs:subClassOf ?lecture.
                      ?d sch:hasTopic ?topic.
                      ?topic rdfs:label ?topic_label.
                      ?d sch:resource ?resource.
                   }ORDER BY(?topic)
                    """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
                    ans="No related data available!"
        else:
                    t=[]
                    #print(results)
                    for result in results['results']['bindings']:
                        for key, value in result.items():
                            t.append(str(value['value']))
                    ans=""
                    i=0
                    while(i<len(t)):
                      ans=ans+t[i]+"-"+t[i+1]+"\n\n"
                      i=i+2
        dispatcher.utter_message(text=ans)

        return []
    
class ActionHello(Action):

     def name(self) -> Text:
         return "content_from_lectureNo_info3"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        course=str(tracker.slots['course'])
        no=str(tracker.slots['number'])
        no="'"+no+"'"
        query="""
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix sch: <http://focu.io/schema#/>
            SELECT ?value
            WHERE {
            ?lecture sch:lectNumber """+no+"""^^xsd:int.
            ?lecture sch:forCourse sch:"""+course+""".
            ?lecture sch:hasContent ?content.
            ?content ?property ?value.
            FILTER(?property!=rdf:type)
            }
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
            ans="No related data available!"
        else:
            t=[]
            #print(results)
            for result in results['results']['bindings']:
                for key, value in result.items():
                    t.append(str(value['value']))
            ans="The contents are: "
            for i in range(0,len(t)):
                ans=ans+str(t[i])+", "
        dispatcher.utter_message(text=ans)

        return []
    
class ActionHello(Action):

     def name(self) -> Text:
         return "content_from_labNo_info4"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        course=str(tracker.slots['course'])
        no=str(tracker.slots['number'])
        no="'"+no+"'"
        query="""
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix sch: <http://focu.io/schema#/>
            SELECT ?value
            WHERE {
            ?lecture sch:forCourse sch:"""+course+""".
            ?lab rdfs:subClassOf ?lecture.
            ?lab sch:labNumber """+no+"""^^xsd:int.
            ?lab sch:Content ?content.
            ?content ?property ?value.
            FILTER(?property!=rdf:type).
            }
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
            ans="No related data available!"
        else:
            t=[]
            #print(results)
            for result in results['results']['bindings']:
                for key, value in result.items():
                    t.append(str(value['value']))
            ans="The contents are: "
            for i in range(0,len(t)):
                ans=ans+str(t[i])+", "
        dispatcher.utter_message(text=ans)

        return []

class ActionHello(Action):

     def name(self) -> Text:
         return "link_from_course_info5"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        course=str(tracker.slots['course'])
        query="""
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix sch: <http://focu.io/schema#/>
            SELECT ?link
            WHERE {
            sch:"""+course+""" rdfs:seeAlso ?link.
            }
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
            ans="No related data available!"
        else:
            t=[]
            #print(results)
            for result in results['results']['bindings']:
                for key, value in result.items():
                    t.append(str(value['value']))
            ans="The link is: "
            for i in range(0,len(t)):
                ans=ans+str(t[i])+"\n"
        dispatcher.utter_message(text=ans)

        return []
    
class ActionHello(Action):

     def name(self) -> Text:
         return "course_from_courseNo_info6"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        subject=str(tracker.slots['subject'])
        subject="'"+subject+"'"
        no=str(tracker.slots['number'])
        no="'"+no+"'"
        query="""
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            prefix sch: <http://focu.io/schema#/>
            SELECT ?name
            WHERE {
            ?course sch:number """+no+"""^^xsd:int.
            ?course sch:subject """+subject+"""^^xsd:string.
            ?course sch:courseName ?name.
            }
            
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
            ans="No related data available!"
        else:
            t=[]
            #print(results)
            for result in results['results']['bindings']:
                for key, value in result.items():
                    t.append(str(value['value']))
            ans="The course is: "
            for i in range(0,len(t)):
                ans=ans+str(t[i])
        dispatcher.utter_message(text=ans)

        return []

class ActionHello(Action):

     def name(self) -> Text:
         return "desc_from_course_info7"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        c=str(tracker.slots['course'])
        query="""
            prefix sch: <http://focu.io/schema#/>
            SELECT ?description
            WHERE {
            sch:"""+c+""" sch:courseDesc ?description.
            }
            
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
            ans="No related data available!"
        else:
            t=[]
            #print(results)
            for result in results['results']['bindings']:
                for key, value in result.items():
                    t.append(str(value['value']))
            ans=''
            for i in range(0,len(t)):
                ans=ans+str(t[i])
        dispatcher.utter_message(text=ans)

        return []
    
class ActionHello(Action):

     def name(self) -> Text:
         return "outline_from_course_info8"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        c=str(tracker.slots['course'])
        query="""
            prefix sch: <http://focu.io/schema#/>
            SELECT ?outline
            WHERE {
            sch:"""+c+""" sch:outline ?outline.
            }     
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
            ans="No related data available!"
        else:
            t=[]
            #print(results)
            for result in results['results']['bindings']:
                for key, value in result.items():
                    t.append(str(value['value']))
            ans=''
            for i in range(0,len(t)):
                ans=ans+str(t[i])
        dispatcher.utter_message(text=ans)

        return []

class ActionHello(Action):

     def name(self) -> Text:
         return "slide_from_course_info9"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        course=str(tracker.slots['course'])
        no=str(tracker.slots['number'])
        no="'"+no+"'"
        query="""
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            prefix sch: <http://focu.io/schema#/>
            SELECT ?slides
            WHERE {
            ?lecture sch:lectNumber """+no+"""^^xsd:int.
            ?lecture sch:forCourse sch:"""+course+""".
            ?lecture sch:hasContent ?content.
            ?content sch:hasSlides ?slides.
            }
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
            ans="No related data available!"
        else:
            t=[]
            #print(results)
            for result in results['results']['bindings']:
                for key, value in result.items():
                    t.append(str(value['value']))
            ans=''
            for i in range(0,len(t)):
                ans=ans+str(t[i])+" ,"
        dispatcher.utter_message(text=ans)

        return []
    
class ActionHello(Action):

     def name(self) -> Text:
         return "worksheet_from_course_info10"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        course=str(tracker.slots['course'])
        no=str(tracker.slots['number'])
        no="'"+no+"'"
        query="""
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            prefix sch: <http://focu.io/schema#/>
            SELECT ?worksheet
            WHERE {
            ?lecture sch:lectNumber """+no+"""^^xsd:int.
            ?lecture sch:forCourse sch:"""+course+""".
            ?lecture sch:hasContent ?content.
            ?content sch:hasWorksheets ?worksheet.
            }
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
            ans="No related data available!"
        else:
            t=[]
            #print(results)
            for result in results['results']['bindings']:
                for key, value in result.items():
                    t.append(str(value['value']))
            ans=''
            for i in range(0,len(t)):
                ans=ans+str(t[i])+" ,"
        dispatcher.utter_message(text=ans)

        return []
    
class ActionHello(Action):

     def name(self) -> Text:
         return "lab_content_from_lecture_info11"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        course=str(tracker.slots['course'])
        no=str(tracker.slots['number'])
        no="'"+no+"'"
        query="""
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                prefix sch: <http://focu.io/schema#/>
                SELECT ?property ?value
                WHERE {
                ?lecture sch:lectNumber """+no+"""^^xsd:int.
                ?lecture sch:forCourse sch:"""+course+""".
                ?lab rdfs:subClassOf ?lecture.
                ?lab sch:Content ?content.
                ?content ?property ?value.
                FILTER(?property!=rdf:type)
                }
                           
            """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
            ans="No related data available!"
        else:
          t=[]
          for result in results['results']['bindings']:
              for key, value in result.items():
                  val=str(value['value'])
                  if val =='http://focu.io/schema#/Readings':
                      t.append('Readings')
                  elif val=='http://focu.io/schema#/Worksheets':
                      t.append('Worksheets')
                  elif val=='http://focu.io/schema#/Slides':
                      t.append('Slides')
                  elif val=='http://focu.io/schema#/OtherMaterial':
                      t.append('OtherMaterial')
                  else:
                      t.append(val)
          ans=''
          i=0
          while(i<len(t)):
              ans=ans+t[i]+"-"+t[i+1]+"\n"
              i=i+2
        dispatcher.utter_message(text=ans)
        return []

class ActionHello(Action):

     def name(self) -> Text:
         return "topic_from_labNo_info15"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        from SPARQLWrapper import SPARQLWrapper, JSON
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        course=str(tracker.slots['course'])
        no=str(tracker.slots['number'])
        no="'"+no+"'"
        query="""
                  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  prefix sch: <http://focu.io/schema#/>
        
                   SELECT ?topic_label ?resource
                   WHERE {
                      
                      ?lecture sch:forCourse sch:"""+course+""".
                      ?lab rdfs:subClassOf ?lecture.
                      ?lab sch:labNumber """+no+"""^^xsd:int.
                      ?d rdfs:subClassOf ?lab.
                      ?d sch:hasTopic ?topic.
                      ?topic rdfs:label ?topic_label.
                      ?d sch:resource ?resource.
                   }ORDER BY(?topic)
                    """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
                    ans="No related data available!"
        else:
                    t=[]
                    for result in results['results']['bindings']:
                        for key, value in result.items():
                            t.append(str(value['value']))
                    ans=""
                    i=0
                    while(i<len(t)):
                      ans=ans+t[i]+"-"+t[i+1]+"\n\n"
                      i=i+2
        dispatcher.utter_message(text=ans)
        return []


class ActionHello(Action):

     def name(self) -> Text:
         return "courses_from_topic_info16"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        from SPARQLWrapper import SPARQLWrapper, JSON
        sparql = SPARQLWrapper("http://localhost:3030/ds")
        topic=str(tracker.slots['topic'])
        topic=topic.replace(' ','_')
        topic="'"+topic+"'"
        query="""
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                prefix sch: <http://focu.io/schema#/>
                SELECT ?courseName ?subject ?courseNumber
                WHERE {
                        ?topic sch:topicName """+topic+"""^^xsd:string.
                  		?topic sch:coveredInCourse ?course.
                  		?course sch:courseName ?courseName.
                  		?course sch:subject ?subject.
                  		?course sch:number  ?courseNumber.
                }ORDER BY(?topic)
                    """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']==[]:
                    ans="No related data available!"
        else:
                    t=[]
                    for result in results['results']['bindings']:
                        for key, value in result.items():
                            t.append(str(value['value']))
                    ans=""
                    i=0
                    while(i<len(t)):
                      ans=ans+t[i]+"-"+t[i+1]+t[i+2]+"\n\n"
                      i=i+3
        dispatcher.utter_message(text=ans)
        return []
