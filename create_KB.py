# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 13:06:38 2021

@author: Piyush
"""
#import fetch
import os
import pandas
import spotlight
from tika import parser 
import urllib.parse
import rdflib
from rdflib import Namespace, Graph, RDF, RDFS, URIRef, Literal
from rdflib.namespace import FOAF, XSD, OWL

def code_url(url):
    return urllib.parse.unquote_plus(url)

namespaces_dict = {"dbo": "http://dbpedia.org/ontology/",
                   "dbr": "http://dbpedia.org/resource/",
                   "sch": "http://focu.io/schema#/",
                   "schd": "http://focu.io/data#/"}

dbo = Namespace(namespaces_dict.get("dbo"))
dbr = Namespace(namespaces_dict.get("dbr"))
schema = Namespace(namespaces_dict.get("sch"))
data = Namespace(namespaces_dict.get("schd"))

graph = Graph()

graph.bind('dbo', dbo)
graph.bind('dbr', dbr)
graph.bind('sch', schema)
graph.bind('schd', data)
graph.bind('owl', OWL)
graph.bind('foaf', FOAF)
graph.bind('xsd', XSD)

Concordia_University = URIRef(data.Concordia_University)

def add_university():
    graph.add((Concordia_University, RDF.type, schema.University))
    graph.add((Concordia_University, schema.uniName, Literal("Concordia University", lang="en")))
    graph.add((Concordia_University, RDFS.label, Literal("Concordia University", lang="en")))
    graph.add((Concordia_University, RDFS.comment, Literal("Concordia University is a university.", lang="en")))
    graph.add((Concordia_University,OWL.sameAs, URIRef(dbr.Concordia_University)))


def get_unique_subjects_from_dataset():
    courses_dataframe = pandas.read_csv('Dataset/courses.csv')
    return courses_dataframe['Course Subject'].drop_duplicates().values.tolist()


def get_courses_for_a_subject(subject):
    courses_dataframe = pandas.read_csv('Dataset/courses.csv')
    course_df = courses_dataframe[(courses_dataframe['Course Subject'] == subject)]
    return course_df



def add_subjectsWithCourses():
    subject_list = get_unique_subjects_from_dataset()
    for subject_name in subject_list:
        course_list = get_courses_for_a_subject(subject_name)
        for i in range(len(course_list)):
            add_courses(i, course_list,subject_name)
    graph.add((data.COMP6741, RDFS.seeAlso,
               URIRef("https://moodle.concordia.ca/moodle/course/view.php?id=132738")))  

def add_courses(i, course_list, subject_name):
    course_number = str(course_list.iloc[i]['Course Number'])
    course_name = course_list.iloc[i]['Course Name']
    course_description = course_list.iloc[i]['Course Description']
    course = data[subject_name+str(course_number)]
    graph.add((course, RDF.type, schema.Course))
    graph.add((course, schema.courseName, Literal(course_name, datatype=XSD.string)))
    graph.add((course, schema.subject, Literal(subject_name, datatype=XSD.string)))
    graph.add((course, schema.number, Literal(str(course_number), datatype=XSD.int)))
    graph.add((course,schema.courseDesc, Literal(course_description, datatype=XSD.string)))
    graph.add((course, RDFS.label, Literal(course_number, lang="en")))
    graph.add((course, RDFS.comment,
               Literal(course_number + " is a part of " + subject_name + ".", lang="en")))
    

def generate(path):
  parsed_pdf = parser.from_file(path)
  text = parsed_pdf['content'] 
  try:
      response=(spotlight.annotate('http://localhost:2222/rest/annotate',text,confidence=0.7,support=40))
  except:
      return None
  return response

def addTopic(topic,source,uri,course,lecture,lab,res):
   print(res)
   print()
   link=URIRef(uri)
   graph.add((topic, RDF.type, schema.Topic))
   graph.add((topic,OWL.sameAs, link))
   label=str(source)
   graph.add((topic,RDFS.label, Literal(label, lang="en")))
   graph.add((topic, schema.topicName, Literal(source, datatype=XSD.string)))
   graph.add((topic, schema.coveredInCourse, course))  
   if lecture!=None:
       graph.add((topic, schema.coveredInLecture,lecture))
       top=data[str('Lect-'+lecture+label)]
       graph.add((top, RDF.type, schema.topic))
       graph.add((top, RDFS.subClassOf, lecture))
       graph.add((top, schema.hasTopic, topic))
       graph.add((top, schema.resource, res))
   elif lab!=None:
       graph.add((topic, schema.coveredInLab,lab))
       top=data[str('Lab'+lab+label)]
       graph.add((top, RDF.type, schema.topic))
       graph.add((top, RDFS.subClassOf, lab))
       graph.add((top, schema.hasTopic, topic))
       graph.add((top, schema.resource, res))
   else:
       graph.add((topic, schema.resource, res))
       
def add_lecture(c):
   cd=os.getcwd()
   cd=cd.replace(os.sep, '/')
   course_name=c
   course=URIRef("http://focu.io/data#/"+c)
   p="file:///"
   for roots, dirs1, files1 in os.walk(cd+"/Dataset/CoursesDataset/"+c+"/"):
        for file in files1:
            if "outline" in file:
                outline=URIRef(p+roots+file)
                graph.add((course, schema.outline, outline))
                response=generate(roots+file)
                if response!=None:
                    for res in response:
                        source=str(res['surfaceForm'])
                        source=source.replace(' ', '_')
                        topic=data[str(source)]
                        uri=str(res['URI'])
                        addTopic(topic,source,uri,course,None,None,outline)
                        #graph.add((topic, schema.resource, outline))

                    
   for roots, dirs1, files1 in os.walk(cd+"/Dataset/CoursesDataset/"+c+"/lecture"):
        for d in dirs1:
            s=d.split(".")
            lecture_no=s[0]
            label="Lecture "+str(lecture_no)
            lecture_name=s[1]
            lecture=data[str(course_name+"-l"+lecture_no)]
            graph.add((lecture, RDF.type, schema.lecture))
            graph.add((lecture, schema.forCourse, course))
            graph.add((lecture, schema.lectNumber, Literal(lecture_no, datatype=XSD.int)))
            
            graph.add((lecture, schema.lectName, Literal(lecture_name, datatype=XSD.String)))
            graph.add((lecture, RDFS.label, Literal(label, datatype=XSD.String)))
            content=data[str(course_name+"content-lecture"+lecture_no)]
            graph.add((content, RDF.type, schema.lectContent))
            graph.add((course, schema.courseLectureContent, content))
            graph.add((content,schema.lectureContentCourse, course))
            for root, dirs, files in os.walk(roots+"/"+d+"/"):
                for file in files:
                    flag=0
                    path=(p+root+file)
                    s=URIRef(str(path))
                    if "slides" in file:                        
                        graph.add((s,RDF.type,schema.slide))
                        graph.add((content, schema.hasSlides,s))
                    elif "worksheet" in file:
                        graph.add((s,RDF.type,schema.worksheet))
                        graph.add((content, schema.hasWorksheets,s))
                    elif "readings" in file:
                        graph.add((s,RDF.type,schema.reading))
                        graph.add((content, schema.hasReadings, s))
                    elif "others" in file:
                        flag=1 
                        file1 = open(root+file, 'r')
                        Lines = file1.readlines()
                        for line in Lines:
                            l=line.split('\n')
                            d=URIRef(l[0])
                            graph.add((d,RDF.type,schema.other))
                            graph.add((content, schema.hasOthers, d))
                            s=''
                    if flag==0:
                        response=generate(root+file)
                        if response!=None:
                            for res in response:
                                 source=str(res['surfaceForm'])
                                 uri=str(res['URI'])
                                 source=source.replace(' ', '_')
                                 topic=data[str(source)]
                                 addTopic(topic,source,uri,course,lecture,None,s)
                                 #graph.add((lecture, schema.lectResource, s))
            graph.add((lecture, schema.hasContent,content))
            
def add_labs(c):
   cd=os.getcwd()
   cd=cd.replace(os.sep, '/')
   course_name=c
   course=URIRef("http://focu.io/data#/"+c)
   p="file:///"
   for roots, dirs1, files1 in os.walk(cd+"/Dataset/CoursesDataset/"+c+"/labs"):
        for d in dirs1:
            s=d.split(".")
            lab_no=s[0]
            di=s[1].split("-")
            lab_name=di[0]
            label="Lab "+str(lab_no)
            lecture_no=di[1]
            lecture=URIRef("http://focu.io/data#/"+course_name+"-l"+lecture_no)
            lab=data[str(c+"-lab"+lab_no)]
            graph.add((lab, RDF.type, schema.lab))
            graph.add((lab, RDFS.subClassOf, lecture))
            graph.add((lab, schema.labNumber, Literal(lab_no, datatype=XSD.int)))
            graph.add((lab, schema.labName, Literal(lab_name, datatype=XSD.string)))
            content=data[str(course_name+"content-lab"+lab_no)]
            graph.add((content, RDF.type, schema.labContent))
            graph.add((course, schema.courseLabContent, content))
            graph.add((content,schema.labContentCourse, course))
            graph.add((lab, RDFS.label, Literal(label, datatype=XSD.String)))
            for root, dirs, files in os.walk(roots+"/"+d+"/"):
                for file in files:
                    flag=0
                    path=(p+os.path.join(root, file))
                    s=URIRef(str(path))
                    if "slides" in file:                        
                        graph.add((s,RDF.type,schema.slide))
                        graph.add((content, schema.Slides,s))
                    elif "worksheet" in file:
                        graph.add((s,RDF.type,schema.worksheet))
                        graph.add((content, schema.Worksheets,s))
                    elif "readings" in file:
                        graph.add((s,RDF.type,schema.reading))
                        graph.add((content, schema.Readings, s))
                    elif "others" in file:
                        flag=1 
                        file1 = open(root+file, 'r')
                        Lines = file1.readlines()
                        for line in Lines:
                            l=line.split('\n')
                            d=URIRef(l[0])
                            graph.add((d,RDF.type,schema.other))
                            graph.add((content, schema.hasOthers, d))
                    if flag==0:
                        response=generate(root+file)
                        if response!=None:
                            for res in response:
                                 source=str(res['surfaceForm'])
                                 source=source.replace(' ', '_')
                                 topic=data[str(source)]
                                 uri=str(res['URI'])
                                 addTopic(topic,source,uri,course,None,lab,s)
                                 #graph.add((lab,schema.labResource, s))
            graph.add((lab, schema.Content,content))
            
            
def save_graph():
    graph.serialize(destination='KnowledgeBase1.nt', format='nt')
    print("Knowledge Base saved as:"+os.getcwd()+"\KnowledgeBase.nt")


add_university()
add_subjectsWithCourses()
add_lecture("COMP6741")
add_lecture("SOEN6841")
add_labs("COMP6741")
add_labs("SOEN6841")
save_graph()
