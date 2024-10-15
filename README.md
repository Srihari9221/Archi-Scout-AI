```
# Archi-Scout-AI

## Project Abstract

Site analysis is a crucial step in the architectural design process that involves assessing a site's physical, environmental, and contextual characteristics. This phase informs design decisions and ensures that the final outcome is functional, sustainable, and aesthetically pleasing. Architects evaluate factors such as topography, climate, local ecology, and existing infrastructure, which significantly influence their design solutions. However, the site analysis process can be time-consuming and complex, often resulting in delays that hinder creativity and limit the time available for developing high-quality designs.

Archi-Scout-AI aims to address these challenges by streamlining the site analysis process for architects. By providing quick access to essential data such as sun path, wind direction, elevation, precipitation, temperature, soil characteristics, air quality, and disturbing factors, Archi-Scout-AI allows architects to make informed decisions efficiently. The chatbot automates data collection and visualization, enabling architects to focus on the creative aspects of their designs while minimizing the time and effort required for site analysis. This innovative solution ultimately empowers architects to deliver high-quality designs in a more timely manner.


## Setup

1. Clone the repository
 
2. Install all the requirements:

   ```bash
   pip install -r requirements.txt
 
   ```
3. Download the spaCy encoding model:
   
   ```bash
   python -m spacy download en_core_web_md
   ```
   
5. Navigate to the SiteAnalysisChatbot directory
   
6. Run the Django project:

   ```bash
   python manage.py runserver
   ```

## Working

1. **Sunpath**  
   ![Screenshot (366)](https://github.com/user-attachments/assets/dc8806a0-849e-4f26-8904-7222a743412d)  
   ![Screenshot (367)](https://github.com/user-attachments/assets/6516a6c6-b605-47d7-ad5b-f0f36dfc9dea)

2. **Air Quality**  
   ![Screenshot (372)](https://github.com/user-attachments/assets/d09161b9-62c2-4747-816c-148fd1ff0add)

3. **Wind Direction**  
   ![Screenshot (368)](https://github.com/user-attachments/assets/ac8179e8-2300-468d-ac09-03f5e9e27a59)

4. **Soil Characteristics**  
   ![Screenshot (371)](https://github.com/user-attachments/assets/02335c52-1705-43fa-aabf-63f1ff61afaa)

5. **Elevation**  
   ![Screenshot (370)](https://github.com/user-attachments/assets/209f6a64-b12a-42cb-ab70-fea2b5d5f1f1)

6. **Disturbing Factors**  
   ![Screenshot (369)](https://github.com/user-attachments/assets/fefa92b4-266a-4c2d-bb0a-969fe97ac358)

7. **Rainfall**  
   ![Screenshot (375)](https://github.com/user-attachments/assets/88e71d63-02be-4660-bbb8-b2ece51d5451)  
   ![Screenshot (373)](https://github.com/user-attachments/assets/1ad05415-4dc5-495c-97f2-dfb1fb0d4ec8)

8. **Temperature**  
   ![Screenshot (374)](https://github.com/user-attachments/assets/8f3c87a8-d267-45fc-aa66-58ea1dc9e0d1)
