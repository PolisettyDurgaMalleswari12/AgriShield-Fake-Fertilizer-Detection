# AgriShield Final

Simple farmer safety web application using Python, Flask, SQLite, HTML/CSS/JavaScript.

## Features
Farmer login/register, dashboard, direct camera QR/barcode scanning, product verification, batch/MRP/seller/expiry checks, rule-based risk score, history, reports, admin dashboard, English/Telugu/Hindi.

## Install
pip install -r requirements.txt

## Run
python app.py

Open http://127.0.0.1:5000

## Admin
Email: admin@agrishield.com
Password: admin123

## Camera
The browser camera scanner uses the html5-qrcode JavaScript library from a CDN. Allow camera permission when prompted. A scanned code should contain a product ID such as F001 or F006.

The Product ID is filled automatically after scanning. Batch and MRP remain separate verification fields because the demo database treats them as independent checks.

This is an academic/demo system. A risk score is not legal proof of counterfeit status; real deployment requires authorized manufacturer/government data and secure authentication.
