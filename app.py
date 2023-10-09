from flask import Flask,request,render_template,jsonify
import os
import numpy as np
from prediction_service import prediction

static_path = os.path.join("webapp","static")
templates_path = os.path.join("webapp","templates")

app = Flask(__name__,
            static_folder=static_path,
            template_folder=templates_path
            )

@app.route("/",methods=["GET","POST"]) # type: ignore
def index():
    if request.method=="POST":
        try:
            if request.form:
                data_req=dict(request.form)
                response=prediction.form_response(data_req)
                return render_template("index.html",response=response)
        
            elif request.json:
                response=prediction.api_response(request.json)
                return jsonify(response)
        
        except Exception as e:
            print (e)
            error={"error":e}
            return render_template("404.html",error=error)
        
    else:
        return render_template("index.html")

if __name__=="__main__":
    app.run(host = "0.0.0.0",port=5000,debug=True)