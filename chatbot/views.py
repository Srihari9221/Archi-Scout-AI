from django.shortcuts import render
from django.http import HttpResponse
from .utils.climate_representation_function import get_single_param_input
from .utils.elavation_function import generate_elevation_map
from .utils.wind_path_function import generate_wind_map
from .utils.solar_path_function import get_solar_input
from .utils.soil_property_function import process_all_properties
from .utils.disturbing_factor_function import disturbing_factors
from .utils.air_quality_function import air_quality_index
from django.http import JsonResponse
from .utils.prompts import Solar_Wind_prompt,summary_prompt,Climate_prompt,Elavation_prompt,Soil_properties_prompt,custom_string_to_dict,disturbing_factors_prompt,air_quality_prompt
from langchain.schema import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from django.conf import settings
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.contrib import messages

lat = None
lon = None

chat_history_for_finetuned_llm = []
chat_history_for_finetuned_llm.append(HumanMessage(content="Don't provide extra text just follow the prompt template and give in formate asked, dont provide extra text"))
chat_history_for_summary_llm = []
chat_history_for_summary_llm.append(HumanMessage(content="Please elaborate on the given summary in a concise, point-wise manner. Ensure the points are clear and organized. Avoid excessive text or unnecessary details. Do not use symbols like asterisks to enclose the text."))

# Set API key for ChatGroq
os.environ["GROQ_API_KEY"] = "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"

# Initialize the language model
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
llm_2= ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
# Define the chat prompt template
finetune_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", Solar_Wind_prompt+Climate_prompt+Elavation_prompt+Soil_properties_prompt+disturbing_factors_prompt+air_quality_prompt),
        ("placeholder", "{chat_history_for_finetuned_llm}"),
        ("human", "{input}"),
    ]
)

summary_prompt_for_llm = ChatPromptTemplate.from_messages(
    [
        ("system", summary_prompt ),
        ("placeholder", "{chat_history_for_summary_llm}"),
        ("human", "{input}"),
    ]
)
# Chain the prompt and model
finetuned_llm_model = finetune_prompt | llm

summary_llm_model = summary_prompt_for_llm | llm_2

def chatbot(request):
    global lat,lon
    if request.method == 'POST':
        print(request.POST)
        if 'latitude' in request.POST and 'longitude' in request.POST:
            lat_input = request.POST.get("latitude")
            lon_input = request.POST.get("longitude")
            if lat_input and lon_input:
                lat = float(lat_input)  
                lon = float(lon_input)
                request.session['latitude'] = lat
                request.session['longitude'] = lon
                print(f"Updated session lat/lon: {lat}, {lon}")


    if request.method == 'POST':
          
        if 'message' in request.POST:
            print("hi")
            lat = request.session.get('latitude')
            lon = request.session.get('longitude')
            print("This is message")
            print(lat,lon)
            image_lst =[]
            map_lst =[]
            text_lst=[]
            response = {"text": "", "image": "", "map" : ""}
            input_chat = request.POST.get("message")
            print(input_chat)

            chat_history_for_finetuned_llm.append(HumanMessage(content=input_chat))
            chat_history_for_summary_llm.append(HumanMessage(content=input_chat))
            
            
            text_to_dict = finetuned_llm_model.invoke({
            "chat_history_for_finetuned_llm": chat_history_for_finetuned_llm,
            "input": input_chat,
            })

            # Append AI message to chat history
            print(text_to_dict.content,"<----<<<")
            print(type(text_to_dict.content),"<----<<<")
            prased_response = text_to_dict.content
            chat_history_for_finetuned_llm.append(AIMessage(content=prased_response))
            dict_response = custom_string_to_dict(prased_response)
            print(dict_response,"<----<<<")
            print(type(dict_response),"<----<<<")
        

            if "sunpath" in dict_response:
                    parm_dict = dict_response.get("sunpath")
                    summary , image_path = get_solar_input(lat,lon,parm_dict)
                    image_lst.append(image_path)
                    text_lst.append(summary)
                    map_lst.append("NoData")
                

            if "windpath" in dict_response:
                    parm_dict = dict_response.get("windpath")
                    summary , wind_map= generate_wind_map(lat,lon,parm_dict)
                    text_lst.append(summary)
                    map_lst.append("get-wind-map/")
                    image_lst.append("NoData")

            if "climate" in dict_response:
                    parm_dict = dict_response.get("climate")
                    summary, image_path = get_single_param_input(lat,lon,parm_dict)
                    text_lst.append(summary)
                    image_lst.append(image_path)
                    map_lst.append("NoData")

            if "elavation" in dict_response:
                    
                    summary ,elevation_map= generate_elevation_map(lat,lon)
                    text_lst.append(summary)
                    map_lst.append("get-elevation-map/")
                    image_lst.append("NoData")

            if "soilproperty" in dict_response:
                    parm_dict = dict_response.get("soilproperty")
                    summary_lst ,img_lst,map_list= process_all_properties(lat,lon,parm_dict)
                    text_lst.extend(summary_lst)
                    map_lst.extend(map_list)
                    image_lst.extend(img_lst)

            if "disturbing" in dict_response:
                
                summary = disturbing_factors(lat,lon)
                text_lst.append(summary)
                map_lst.append("get-disturbing-map/")
                image_lst.append("NoData")

            if "airquality" in dict_response:
                    summary , image_path = air_quality_index(lat,lon)
                    text_lst.append(summary)
                    image_lst.append(image_path)
                    map_lst.append("NoData")

            
            response["image"] = image_lst
            response["map"] = map_lst
            response["text"] = text_lst
            return JsonResponse(response) 

    # print(lat,lon)
    return render(request,'index.html')



# View for test.html (main page containing the iframe)
def test(request):
    return render(request, 'test.html')

# View for iframe.html (content inside iframe)
def elevation_map(request):
    return render(request, 'elevation_map.html')

def wind_map(request):
    return render(request, 'wind_map.html')

def disturbing_map(request):
    return render(request, 'disturbing_places_map.html')