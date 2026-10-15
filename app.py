import os
import json
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

app = FastAPI(
    title="Infrastructure Inquiry Bot",
    description="API للبحث والاستعلام عن السيرفرات باستخدام الذكاء الاصطناعي",
    version="1.0.0"
)

# قراءة ملف الإكسل عند تشغيل التطبيق
try:
    df = pd.read_excel("Training_Servers_80Rows.xlsx")
    df.columns = df.columns.str.strip()
except Exception as e:
    print(f"Error loading Excel file: {e}")
    df = pd.DataFrame()

class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Infrastructure Inquiry Bot Running"}


@app.get("/api/stats")
def stats():
    if df.empty:
        return {"total_servers": 0, "environments": {}}
    
    return {
        "total_servers": len(df),
        "environments": df["Environment"].value_counts().to_dict() if "Environment" in df.columns else {}
    }


@app.get("/api/server/{server_name}")
def search_server(server_name: str):
    if "Server Name" not in df.columns:
        return {"error": "Column 'Server Name' not found"}
    result = df[df["Server Name"].astype(str).str.contains(server_name, case=False, na=False)]
    return result.to_dict(orient="records")


@app.get("/api/hostname/{hostname}")
def search_hostname(hostname: str):
    if "Hostname" not in df.columns:
        return {"error": "Column 'Hostname' not found"}
    result = df[df["Hostname"].astype(str).str.contains(hostname, case=False, na=False)]
    return result.to_dict(orient="records")


@app.get("/api/source-ip/{ip}")
def search_source_ip(ip: str):
    if "Source IP" not in df.columns:
        return {"error": "Column 'Source IP' not found"}
    result = df[df["Source IP"].astype(str).str.contains(ip, case=False, na=False)]
    return result.to_dict(orient="records")


@app.get("/api/nat-ip/{ip}")
def search_nat_ip(ip: str):
    if "NAT IP" not in df.columns:
        return {"error": "Column 'NAT IP' not found"}
    result = df[df["NAT IP"].astype(str).str.contains(ip, case=False, na=False)]
    return result.to_dict(orient="records")


@app.get("/api/environment/{env}")
def search_environment(env: str):
    if "Environment" not in df.columns:
        return {"error": "Column 'Environment' not found"}
    result = df[df["Environment"].astype(str).str.upper() == env.upper()]
    return result.to_dict(orient="records")


@app.post("/api/query")
def process_natural_language_query(request: QueryRequest):
    if not openai_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI API Key is missing or not configured in .env file."
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty."
        )

    system_prompt = """
    أنت مساعد ذكي متخصص في استعلامات بيانات السيرفرات.
    قم بتحليل السؤال القادم واستخرج المعايير المطلوبة على شكل كائن JSON حصراً بالشكل التالي:
    {
      "intent": "search" أو "stats",
      "params": {
        "server_name": string أو null,
        "hostname": string أو null,
        "source_ip": string أو null,
        "nat_ip": string أو null,
        "environment": string أو null,
        "destination": string أو null
      }
    }
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.question}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )

        parsed_result = json.loads(response.choices[0].message.content)
        intent = parsed_result.get("intent", "search")
        params = parsed_result.get("params", {})

        if intent == "stats":
            data = [stats()]
        else:
            filtered_df = df.copy()
            mapping_keys = {
                "server_name": "Server Name",
                "hostname": "Hostname",
                "source_ip": "Source IP",
                "nat_ip": "NAT IP",
                "environment": "Environment",
                "destination": "Destination"
            }

            for param_key, col_name in mapping_keys.items():
                val = params.get(param_key)
                if val and col_name in filtered_df.columns:
                    filtered_df = filtered_df[
                        filtered_df[col_name].astype(str).str.contains(str(val), case=False, na=False)
                    ]

            data = filtered_df.to_dict(orient="records")

        return {
            "intent": intent,
            "extracted_params": params,
            "results_count": len(data),
            "data": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI processing error: {str(e)}"
        )