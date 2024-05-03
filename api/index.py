from dotenv import load_dotenv
from flask import Flask, jsonify, Response, request
from flask_cors import CORS
import pandas as pd
import os
from vanna.remote import VannaDefault
import sys

load_dotenv()
app = Flask(__name__, static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*"}})

# VANNA INITIALIZATION
vannakey = os.environ.get("VANNA_API_KEY")
model = os.environ.get("VANNA_MODEL")
vn = VannaDefault(model=model, api_key=vannakey)
vn.connect_to_sqlite('D:/TroniQue/tronique/database/TronForumData')

@app.route("/api/v1/generate_questions", methods=["GET"])
def generate_questions():
    return jsonify(
        {
            "type": "question_list",
            "questions": vn.generate_questions(),
            "header": "Here are some questions you can ask:",
        }
    )

@app.route("/api/v1/generate_sql", methods=["GET"])
def generate_sql():
    question = request.args.get("question")
    if question is None:
        return jsonify({"type": "error", "error": "No question provided"})
    sql = vn.generate_sql(question=question)
    return jsonify({"type": "sql", "text": sql})


@app.route("/api/v1/run_sql", methods=["POST"])
def run_sql():
    data = request.get_json()
    sql = data.get("sql") if data else None
    print("sql", sql)
    if sql is None:
        return jsonify({"type": "error", "error": "No SQL query provided", "sql": sql})
    try:
        df = vn.run_sql(sql=sql)
        return jsonify({"type": "df", "df": df.head(10).to_json(orient="records")})
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})


@app.route("/api/v1/download_csv", methods=["POST"])
def download_csv():
    data = request.get_json()
    df_json = data.get("df")
    if df_json is None:
        return jsonify({"type": "error", "error": "No DataFrame provided"})
    df = pd.read_json(df_json, orient="records")
    csv = df.to_csv(index=False)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=data.csv"},
    )

@app.route('/api/v1/generate_plotly_figure', methods=['GET'])
def generate_plotly_figure():
    question = request.args.get('question')
    sql = vn.generate_sql(question=question)
    df = vn.run_sql(sql=sql)

    try:
        code = vn.generate_plotly_code(question=question, sql=sql, df_metadata=f"Running df.dtypes gives:\n {df.dtypes}")
        fig = vn.get_plotly_figure(plotly_code=code, df=df, dark_mode=False)
        fig_json = fig.to_json()

        return jsonify(
            {
                "type": "plotly_figure", 
                "question": question,
                "fig": fig_json,
            })
    except Exception as e:
        # Print the stack trace
        import traceback
        traceback.print_exc()

        return jsonify({"type": "error", "error": str(e)})


@app.route("/api/v1/generate_and_run_sql", methods=["GET"])
def generate_and_run_sql():
    question = request.args.get("question")
    if question is None:
        return jsonify({"type": "error", "error": "No question provided"})
    try:
        sql = vn.generate_sql(question=question)
        df = vn.run_sql(sql=sql)
        return jsonify({"type": "df", "df": df.head(10).to_json(orient="records")})
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})


@app.route("/api/v1/train", methods=["POST"])
def add_training_data():
    data = request.get_json()
    question = data.get("question")
    sql = data.get("sql")
    ddl = data.get("ddl")
    documentation = data.get("documentation")
    try:
        new_id = vn.train(
            question=question, sql=sql, ddl=ddl, documentation=documentation
        )
        return jsonify({"id": new_id})
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
