import guidance
from dotenv import load_dotenv
import urllib.parse
import streamlit as st

load_dotenv()
guidance.llm = guidance.llms.OpenAI("text-davinci-003") 

def generate_email(email):        
    priorities = ["low priority", "medium priority", "high priority"]

    email_generator = guidance(
'''    
{{#block hidden=True~}}
Here is the customer message we received: {{email}}
Please give it a priority score 
priority score: {{select "priority" options=priorities}}
{{~/block~}}
            
{{#block hidden=True~}}
You are a world class customer support; Your goal is to generate an response based on the customer message and next steps;
Here is the customer message to respond: {{email}}
Generate an opening & one paragraph of response to the customer message at {{priority}}:
{{gen 'email'}} 
{{~/block~}}

{{email}}

{{#if priority=='high priority'}}Would love to setup a call this/next week, here is the calendly link: https://calendly.com/jason-zhou{{/if}}

Best regards

Jason
''')

    email_response = email_generator(email=email, priorities=priorities)
    print(email_response)

    return email_response

    

def generate_story(story_idea):
        
    story = guidance('''
{{#block hidden=True~}}
You are a world class story teller; Your goal is to generate a short tiny story less than 200 words based on a story idea;

Here is the story idea: {{story_idea}}
Story: {{gen 'story' temperature=0}}
{{/block~}}

{{#block hidden=True~}}
You are a world class AI artiest who are great at generating text to image prompts for the story; 
Your goal is to generate a good text to image prompt and put it in a url that can generate image from the prompt;

Story: You find yourself standing on the deck of a pirate ship in the middle of the ocean. You are checking if there are still people on the ship
Image url markdown: ![Image](https://image.pollinations.ai/prompt/a%203d%20render%20of%20a%20man%20standing%20on%20the%20deck%20of%20a%20pirate%20ship%20in%20the%20middle%20of%20the%20ocean)
                
Story: {{story}}
Image url markdown: {{gen 'image_url' temperature=0 max_tokens=500}})
{{~/block~}}
                     
Story: {{~story~}}
{{image_url}}
''')

    story = story(story_idea=story_idea)
    print(story)
    return story


def generate_chart(query):
    
    def parse_chart_link(chart_details):
        encoded_chart_details = urllib.parse.quote(chart_details, safe='')

        output = "![](https://quickchart.io/chart?c=" + encoded_chart_details + ")"

        return output
    
    examples = [
        {
            'input': "Make a chart of the 5 tallest mountains",
            'output': {"type":"bar","data":{"labels":["Mount Everest","K2","Kangchenjunga","Lhotse","Makalu"], "datasets":[{"label":"Height (m)","data":[8848,8611,8586,8516,8485]}]}}
        },
        {
            'input': "Create a pie chart showing the population of the world by continent",
            'output': {"type":"pie","data":{"labels":["Africa","Asia","Europe","North America","South America","Oceania"], "datasets":[{"label":"Population (millions)","data": [1235.5,4436.6,738.8,571.4,422.5,41.3]}]}}
        }
    ]

    guidance.llm = guidance.llms.OpenAI("text-davinci-003") 

    chart = guidance(
    '''    
    {{#block hidden=True~}}
        You are a world class data analyst, You will generate chart output based on a natural language;

        {{~#each examples}}
        Q:{{this.input}}
        A:{{this.output}}
        ---
        {{~/each}}
        Q:{{query}}
        A:{{gen 'chart' temperature=0 max_tokens=500}}    
    {{/block~}}
    Hello here is the chart you want
    {{parse_chart_link chart}}
    ''')

    return chart(query=query, examples=examples, parse_chart_link=parse_chart_link)



def main():
    st.set_page_config(page_title="Programmable prompts", page_icon=":bird:")

    tab1, tab2, tab3 = st.tabs(["Chart generator", "Story generator", "generate email"])  

    with tab1:
        st.header("Chart generator")
        prompt = st.text_input("Enter a query")
        if prompt:
            chart = generate_chart(prompt)            
            st.markdown(chart)
    
    with tab2:
        st.header("Story generator")
        prompt = st.text_input("Enter a story idea")
        if prompt:
            story = generate_story(prompt)            
            st.markdown(story)

    with tab3:
        st.header("Email generator")
        email = st.text_area("Customer email to respond")
        if email:
            email_response = generate_email(email)            
            st.write(email_response)  

if __name__ == '__main__':
    main()