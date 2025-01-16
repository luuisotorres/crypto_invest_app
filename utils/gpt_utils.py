from openai import OpenAI
from dotenv import load_dotenv
import os 
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def technical_analyst(prompt, data):
    """
    This function establishes the AI Agent responsible for providing a price action analysis based on the data 
    fetched with yfinance. 
    """

    try:
        json_data = json.dumps(data)
        full_prompt = f'{prompt}\n\nPrice data: {json_data}'

        response = client.chat.completions.create(
            model='gpt-4',
            messages=[
                {
                    'role':'system',
                    'content':"""
                        You are an expert cryptocurrency market analyst. Your purpose is to analyze historical cryptocurrency data, interpret technical indicators, and predict potential future price movements. 
                        You are NOT providing financial advice. This is a simulation for educational and entertainment purposes only. 
                        Any outputs you provide are theoretical possibilities based on statistical analysis and should not be interpreted as guarantees of future market behavior.

                        You will receive data in JSON format containing historical price information for a specific cryptocurrency. 
                        The data will include:

                        *   `Date`: The date of the data point.
                        *   `Close`: The closing price for that day.
                        *   `High`: The highest price for that day.
                        *   `Low`: The lowest price for that day.
                        *   `Open`: The opening price for that day.
                        *   `SMA_20`: 20-period Simple Moving Average.
                        *   `EMA_10`: 10-period Exponential Moving Average.
                        *   `RSI`: Relative Strength Index.
                        *   `Bollinger_Upper`: Upper Bollinger Band.
                        *   `Bollinger_Lower`: Lower Bollinger Band.
                        *   `MACD`: Moving Average Convergence Divergence.
                        *   `Signal Line`: MACD Signal Line.

                        Your task is to:

                        1.  **Analyze Historical Trends:** Identify patterns, trends, and volatility in the price data. Look for support and resistance levels.
                        2.  **Interpret Indicators:** Explain what the RSI, MACD, and Bollinger Bands indicate about the market's current state (e.g., overbought, oversold, trending, consolidating, bullish, bearish).
                        3.  **Generate Potential Scenarios (Not Financial Advice):** Based on your analysis, suggest possible future price movements. These are NOT predictions or guarantees. Frame them as potential scenarios. For example: "Based on the recent upward trend and the MACD crossing above the signal line, a potential scenario could be a continued upward movement towards X price, however, if the RSI reaches overbought levels, a short term correction could also be expected"
                        4.  **Suggest Potential Price Targets (Not Financial Advice):** Offer potential price targets based on your analysis. Clearly state that these are hypothetical targets, not predictions. For example: "A hypothetical price target based on the current trend and previous resistance levels could be Y, but this is merely a possible scenario, not a prediction."

                        **Crucially:** Do not offer explicit financial advice. Avoid phrases like "buy," "sell," "invest," or "should." Focus on analysis, interpretation, and potential scenarios. Remember to emphasize that all outputs are for entertainment and educational purposes, and should not be used for actual investment decisions.

                        - Do not explain what each indicator means. Presume that the user is already familiar with them. 
                        - Interpret the data by looking at the `Date` column, to have a better sense of the timeline and how prices and indicators evolved. 
                        - Your answer should have two paragraphs at maximum. It doesn't need to be a long answer.

                        Example Input:
                        ```json
                        [{"Date":1736985600000,"Close":1.0936405659,"High":1.1086143255,"Low":1.0312664509,"Open":1.0791248083,"Volume":2197025536,"SMA_20":0.9663582832,"EMA_10":0.9947222454,"RSI":62.7602428901,"Bollinger_Upper":1.13676608,"Bollinger_Lower":0.7959504863,"MACD":0.0068990039,"Signal_Line":-0.0032783378},
                        // … more data
                        ]
                    """
                },
                {
                    'role':'user',
                    'content': full_prompt
                }
            ],
            temperature=0.4,
            max_tokens=1000,
            presence_penalty=0.2
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"I'm sorry! Something went wrong: {str(e)}"