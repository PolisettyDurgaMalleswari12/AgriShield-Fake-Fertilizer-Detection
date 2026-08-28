from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, add_user, find_user, save_verification, save_report, get_verifications, get_reports, get_user_verifications
import csv

app=Flask(__name__)
app.secret_key="agrishield-demo-secret"
init_db()

def products():
    with open("dataset/products.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def find_product(pid):
    return next((p for p in products() if p["product_id"].lower()==pid.strip().lower()), None)

@app.route("/")
def index():
    return redirect(url_for("dashboard") if session.get("user") else url_for("login"))

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        if not add_user(request.form["name"],request.form["email"],request.form["password"]):
            return render_template("register.html",error="Email already registered.")
        return redirect(url_for("login"))
    return render_template("register.html",error=None)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        user=find_user(request.form["email"],request.form["password"])
        if user:
            session["user"]=dict(user)
            return redirect(url_for("dashboard"))
        return render_template("login.html",error="Invalid email or password.")
    return render_template("login.html",error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if not session.get("user"): return redirect(url_for("login"))
    return render_template("dashboard.html",user=session["user"],history=get_user_verifications(session["user"]["email"])[:5])

@app.route("/verify",methods=["GET","POST"])
def verify():
    if not session.get("user"): return redirect(url_for("login"))
    if request.method=="GET":
        return render_template("verify.html",product_id=request.args.get("product_id",""))
    pid=request.form["product_id"]; batch=request.form["batch_number"]; mrp_text=request.form["mrp"]
    p=find_product(pid)
    if not p:
        return render_template("result.html",found=False,risk=95,result="Highly Suspicious",
                               message="Product ID was not found in the demonstration database.")
    batch_ok=batch.strip().lower()==p["batch_number"].lower()
    try: mrp=float(mrp_text); mrp_ok=mrp==float(p["mrp"])
    except: mrp=0; mrp_ok=False
    seller=int(p["seller_valid"]); expiry=int(p["expiry_valid"]); complaints=int(p["complaints"])
    risk=(0 if batch_ok else 35)+(0 if mrp_ok else 20)+(0 if seller else 25)+(0 if expiry else 15)+(15 if complaints>=5 else 0)
    risk=min(risk,100)
    if risk>=70: result="Highly Suspicious"; message="Several warning signs were found. Verify through an authorized source before use."
    elif risk>=40: result="Suspicious"; message="Some warning signs were found. Please verify before use."
    else: result="Likely Genuine"; message="No major warning signs were found in the available demonstration records."
    save_verification(session["user"]["email"],p["product_name"],p["brand"],batch,mrp,risk,result)
    return render_template("result.html",found=True,product_name=p["product_name"],brand=p["brand"],batch_number=batch,mrp=mrp,
        batch_valid=batch_ok,mrp_valid=mrp_ok,seller_valid=seller,expiry_valid=expiry,complaints=complaints,risk=risk,result=result,message=message)

@app.route("/history")
def history():
    if not session.get("user"): return redirect(url_for("login"))
    return render_template("history.html",history=get_user_verifications(session["user"]["email"]))

@app.route("/report",methods=["GET","POST"])
def report():
    if not session.get("user"): return redirect(url_for("login"))
    if request.method=="POST":
        save_report(session["user"]["email"],request.form["product_name"],request.form["brand"],request.form["batch_number"],request.form["seller"],request.form["reason"])
        return render_template("report.html",submitted=True)
    return render_template("report.html",submitted=False)

@app.route("/admin-login",methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        if request.form["email"]=="admin@agrishield.com" and request.form["password"]=="admin123":
            session["admin"]=True; return redirect(url_for("admin"))
        return render_template("admin_login.html",error="Invalid admin credentials.")
    return render_template("admin_login.html",error=None)

@app.route("/admin")
def admin():
    if not session.get("admin"): return redirect(url_for("admin_login"))
    v=get_verifications(); r=get_reports()
    suspicious=sum(1 for x in v if x["result"]!="Likely Genuine")
    return render_template("admin_dashboard.html",total_products=len(products()),total_verifications=len(v),
        genuine=len(v)-suspicious,suspicious=suspicious,total_reports=len(r),verifications=v,reports=r)

@app.route("/admin-logout")
def admin_logout():
    session.pop("admin",None); return redirect(url_for("admin_login"))

if __name__=="__main__":
    app.run(debug=True)
