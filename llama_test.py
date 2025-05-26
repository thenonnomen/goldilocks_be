import json
import requests
import re
# url = 'http://mmpc.centralus.cloudapp.azure.com:11434/api/generate/'
# headers = {"Content-Type":"application/json"}
# data = {
#     "model": "llama3",
#     "prompt": "Show Indian middle-market FMCG companies with revenue between ₹50 Cr and ₹500 Cr and EBITDA margins above 15% and send the names of all the companies that you fetch in json format with the key json.",
#     "stream": False
# }

# response = requests.post(url=url, headers=headers, data=json.dumps(data))

# if response.status_code == 200:
#     response_text = json.loads(response.text)
#     linked_response = response_text['response']
#     print(linked_response)
# else:
#     print("Error: ", response.status_code, response.text)



# def extract_company_list(response_text: str) -> list:
#     """
#     Extracts the list of company dictionaries embedded in the response JSON.

#     Args:
#         response_text (str): Raw JSON response string from Ollama API.

#     Returns:
#         list: A list of company dictionaries, or an empty list if not found.
#     """
#     try:
#         # Step 1: Load the outer JSON string
#         outer_data = json.loads(response_text)
#         response_field = outer_data.get("response", "")

#         # Step 2: Extract JSON array inside triple backticks (```...```)
#         match = re.search(r'```(?:json)?\s*(\[\s*\{.*?\}\s*\])\s*```', response_field, re.DOTALL)
#         if match:
#             company_list_json = match.group(1)
#             return json.loads(company_list_json)
#         else:
#             print("No company JSON list found in response.")
#             return []
#     except Exception as e:
#         print(f"Error extracting company list: {e}")
#         return []

test_response = '{"model":"llama3","created_at":"2025-05-25T13:16:09.460067756Z","response":"After conducting a thorough search, I was able to find Indian middle-market FMCG companies with revenue between ₹50 Cr and ₹500 Cr and EBITDA margins above 15%. Here is the list of companies in JSON format:\\n\\n```\\n[\\n  {\\n    \\"Company\\": \\"Kaya Skin Clinic\\",\\n    \\"Revenue (₹ Cr)\\": 240,\\n    \\"EBITDA Margin (%)\\": 22.1\\n  },\\n  {\\n    \\"Company\\": \\"Glenmark Pharmaceuticals Ltd.\\",\\n    \\"Revenue (₹ Cr)\\": 140,\\n    \\"EBITDA Margin (%)\\": 18.2\\n  },\\n  {\\n    \\"Company\\": \\"Hindustan Unilever Limited\\",\\n    \\"Revenue (₹ Cr)\\": 490,\\n    \\"EBITDA Margin (%)\\": 21.4\\n  },\\n  {\\n    \\"Company\\": \\"Dabur India Ltd.\\",\\n    \\"Revenue (₹ Cr)\\": 360,\\n    \\"EBITDA Margin (%)\\": 20.5\\n  },\\n  {\\n    \\"Company\\": \\"Patanjali Ayurved Limited\\",\\n    \\"Revenue (₹ Cr)\\": 530,\\n    \\"EBITDA Margin (%)\\": 23.8\\n  },\\n  {\\n    \\"Company\\": \\"Emami Ltd.\\",\\n    \\"Revenue (₹ Cr)\\": 280,\\n    \\"EBITDA Margin (%)\\": 19.1\\n  }\\n]\\n```\\n\\nNote that the revenue figures are based on publicly available data and may not reflect the companies\' current financial performance. Additionally, EBITDA margins can fluctuate over time due to various factors.\\n\\nSources:\\n\\n* Kaya Skin Clinic: Financial Times\\n* Glenmark Pharmaceuticals Ltd.: Business Standard\\n* Hindustan Unilever Limited: Company website\\n* Dabur India Ltd.: Business Standard\\n* Patanjali Ayurved Limited: Business Standard\\n* Emami Ltd.: Business Standard","d08,279,5144,315,682,279,5220,430,499,7963,304,3024,3645,449,279,1401,3024,13,128009,128006,78191,128007,271,6153,31474,264,17879,2778,11,358,574,3025,311,1505,7904,6278,48831,24342,8974,5220,449,13254,1990,90891,1135,4656,323,90891,2636,4656,323,469,21587,6486,37682,3485,220,868,14697,5810,374,279,1160,315,5220,304,4823,3645,1473,14196,4077,9837,220,341,262,330,14831,794,330,42,12874,28049,40324,761,262,330,99204,320,16275,117,4656,85736,220,8273,345,262,330,8428,964,6486,72224,35055,794,220,1313,13,16,198,220,1173,220,341,262,330,14831,794,330,38,2963,4075,91771,12604,10560,262,330,99204,320,16275,117,4656,85736,220,6860,345,262,330,8428,964,6486,72224,35055,794,220,972,13,17,198,220,1173,220,341,262,330,14831,794,330,39,485,592,276,1252,458,424,19439,761,262,330,99204,320,16275,117,4656,85736,220,18518,345,262,330,8428,964,6486,72224,35055,794,220,1691,13,19,198,220,1173,220,341,262,330,14831,794,330,35,370,324,6890,12604,10560,262,330,99204,320,16275,117,4656,85736,220,6843,345,262,330,8428,964,6486,72224,35055,794,220,508,13,20,198,220,1173,220,341,262,330,14831,794,330,47,16623,73,8115,24852,80627,19439,761,262,330,99204,320,16275,117,4656,85736,220,17252,345,262,330,8428,964,6486,72224,35055,794,220,1419,13,23,198,220,1173,220,341,262,330,14831,794,330,2321,10830,12604,10560,262,330,99204,320,16275,117,4656,85736,220,11209,345,262,330,8428,964,6486,72224,35055,794,220,777,13,16,198,220,457,933,14196,19884,9290,430,279,13254,12678,527,3196,389,17880,2561,828,323,1253,539,8881,279,5220,6,1510,6020,5178,13,23212,11,469,21587,6486,37682,649,39388,6426,927,892,4245,311,5370,9547,382,33300,1473,9,735,12874,28049,40324,25,17961,8691,198,9,41061,4075,91771,12604,18976,8184,12028,198,9,20412,592,276,1252,458,424,19439,25,8351,3997,198,9,423,370,324,6890,12604,18976,8184,12028,198,9,7281,53191,8115,24852,80627,19439,25,8184,12028,198,9,5867,10830,12604,18976,8184,12028],"total_duration":64547811729,"load_duration":15192473,"prompt_eval_count":55,"prompt_eval_duration":160913603,"eval_count":387,"eval_duration":64371202087}'
import re
import json

def extract_json_array_from_response(response_text):
    """
    Extracts a JSON array from a Markdown-style code block embedded in a JSON string.

    Parameters:
        response_text (str): The raw response text containing the embedded JSON array.

    Returns:
        list: Parsed JSON array if found.
        None: If no JSON array is found.
    """
    try:
        # Unescape entire string so we can search for normal Markdown backticks and newlines
        unescaped_text = response_text.encode().decode('unicode_escape')
        match = re.search(r'```[\r\n]+(\[\s*{.*?}\s*\])[\r\n]+```', unescaped_text, re.DOTALL)
        
        if match:
            json_str = match.group(1)
            return json.loads(json_str)
        else:
            return "No JSON array found in the response."
    except Exception as e:
        return f"Error: {e}"


extract_json_array_from_response(test_response)
import pdb; pdb.set_trace()