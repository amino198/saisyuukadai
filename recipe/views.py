from django.shortcuts import render
from google import genai 
import os

def recipe_view(request):
    common_seasonings = ["塩", "砂糖", "醤油", "味噌", "マヨネーズ", "ケチャップ", 
                         "酒", "みりん", "酢", "ポン酢", "胡椒", "にんにく", "生姜"]
    
    recipe = None
    if request.method == "POST":
        ingredients = request.POST.get("ingredients")
        mood = request.POST.get("mood")
        
        selected_seasonings = request.POST.getlist("seasonings")
        seasonings_str = ", ".join(selected_seasonings) if selected_seasonings else "特になし（基本調味料のみ）"

        client = genai.Client(api_key="AIzaSyCVmeqXPNM3eB-0G3ErCT6rU_w1zysa4Mc")
        model_id = "models/gemini-2.5-flash"

        mood_instruction = "" 

        prompt = f"""
        食材：{ingredients}
        使用可能な調味料：{seasonings_str}
        今の気分：{mood}
        
        指示：
        {mood_instruction}
        必ず「使用可能な調味料」と「食材」だけで作れるレシピを1つ提案してください。
        回答は「料理名」「材料」「作り方」の順で出力してください。
        """

        try:
            response = client.models.generate_content(model=model_id, contents=prompt)
            recipe = response.text
        except Exception as e:
            recipe = f"エラーが発生しました: {e}"

    return render(request, 'index.html', {
        'recipe': recipe,
        'common_seasonings': common_seasonings
    })