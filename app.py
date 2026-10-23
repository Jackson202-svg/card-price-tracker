from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import json, os, uuid, urllib.parse, urllib.request, urllib.error

BASE = Path(__file__).parent
DATA = BASE / "data"
DB = DATA / "cards.json"
DATA.mkdir(exist_ok=True)
app = Flask(__name__, static_folder="static")

SEED = [
 {"id":"demo-1","name":"Charizard","game":"Pokémon","set":"Base Set","number":"4/102","rarity":"Holo Rare","condition":"Ungraded","owned":True,"purchase_price":45,"market_price":92.50,"price_source":"Demo data","image_url":"https://images.pokemontcg.io/base1/4.png"},
 {"id":"demo-2","name":"Pikachu","game":"Pokémon","set":"Base Set","number":"58/102","rarity":"Common","condition":"Ungraded","owned":True,"purchase_price":5,"market_price":12.25,"price_source":"Demo data","image_url":"https://images.pokemontcg.io/base1/58.png"},
 {"id":"demo-3","name":"Blue-Eyes White Dragon","game":"Yu-Gi-Oh!","set":"Legend of Blue Eyes White Dragon","number":"LOB-001","rarity":"Ultra Rare","condition":"Near Mint","owned":True,"purchase_price":22,"market_price":38,"price_source":"Demo data","image_url":""},
 {"id":"demo-4","name":"Mickey Mouse - Brave Little Tailor","game":"Disney Lorcana","set":"The First Chapter","number":"001/204","rarity":"Enchanted","condition":"Near Mint","owned":False,"purchase_price":0,"market_price":54,"price_source":"Demo data","image_url":""},
 {"id":"demo-5","name":"Black Lotus","game":"Magic: The Gathering","set":"Alpha","number":"233","rarity":"Rare","condition":"Played","owned":False,"purchase_price":0,"market_price":0,"price_source":"Price not verified","image_url":""}
]
def load_cards():
    if not DB.exists(): save_cards(SEED)
    try: return json.loads(DB.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError): return SEED.copy()
def save_cards(cards): DB.write_text(json.dumps(cards, indent=2, ensure_ascii=False), encoding="utf-8")

def price_search(query):
    token=os.getenv("PRICECHARTING_API_TOKEN","").strip()
    if not token: return {"provider":"manual","results":[],"message":"No API configured. Add an authorized API token on the server, or enter verified prices manually."}
    url="https://www.pricecharting.com/api/products?t="+urllib.parse.quote(token)+"&q="+urllib.parse.quote(query)
    req=urllib.request.Request(url,headers={"User-Agent":"CardScope/1.0"})
    try:
        with urllib.request.urlopen(req,timeout=10) as response: data=json.loads(response.read().decode("utf-8"))
        if data.get("status")!="success": return {"provider":"PriceCharting","results":[],"error":data.get("error-message","Provider request failed")}
        results=[]
        for p in data.get("products",[]):
            cents=p.get("loose-price")
            results.append({"id":str(p.get("id","")),"name":p.get("product-name","Unknown"),"game":p.get("console-name","Trading card"),"market_price":round(float(cents)/100,2) if cents not in (None,"") else None,"price_source":"PriceCharting"})
        return {"provider":"PriceCharting","results":results}
    except (urllib.error.URLError,TimeoutError,ValueError,json.JSONDecodeError) as exc:
        return {"provider":"PriceCharting","results":[],"error":str(exc)}

@app.get("/")
def home(): return send_from_directory("static","index.html")
@app.get("/api/health")
def health(): return jsonify({"ok":True,"price_provider_configured":bool(os.getenv("PRICECHARTING_API_TOKEN"))})
@app.get("/api/cards")
def get_cards():
    q=request.args.get("q","").lower().strip(); game=request.args.get("game","all"); owned=request.args.get("owned","all")
    cards=load_cards()
    if q: cards=[c for c in cards if q in " ".join(str(c.get(k,"")) for k in ("name","game","set","number","rarity")).lower()]
    if game!="all": cards=[c for c in cards if c.get("game")==game]
    if owned=="owned": cards=[c for c in cards if c.get("owned")]
    if owned=="watchlist": cards=[c for c in cards if not c.get("owned")]
    return jsonify({"cards":cards,"count":len(cards)})
@app.post("/api/cards")
def add_card():
    body=request.get_json(silent=True) or {}; name=str(body.get("name","")).strip()
    if not name: return jsonify({"error":"Card name is required"}),400
    def price(key):
        try: return max(0,float(body.get(key) or 0))
        except (ValueError,TypeError): return 0
    card={"id":str(uuid.uuid4()),"name":name,"game":str(body.get("game","Other")),"set":str(body.get("set","")),"number":str(body.get("number","")),"rarity":str(body.get("rarity","")),"condition":str(body.get("condition","Ungraded")),"owned":bool(body.get("owned",True)),"purchase_price":price("purchase_price"),"market_price":price("market_price"),"price_source":"Manually entered","image_url":str(body.get("image_url","")),"updated_at":"Just now"}
    cards=load_cards(); cards.insert(0,card); save_cards(cards)
    return jsonify({"card":card}),201
@app.patch("/api/cards/<card_id>")
def edit_card(card_id):
    body=request.get_json(silent=True) or {}; cards=load_cards()
    for card in cards:
        if card["id"]==card_id:
            for key in ("name","game","set","number","rarity","condition","image_url"):
                if key in body: card[key]=str(body[key]).strip()
            for key in ("purchase_price","market_price"):
                if key in body:
                    try: card[key]=max(0,float(body[key] or 0))
                    except (ValueError,TypeError): return jsonify({"error":key+" must be a number"}),400
            if "owned" in body: card["owned"]=bool(body["owned"])
            if "market_price" in body: card["price_source"]="Manually entered"
            save_cards(cards); return jsonify({"card":card})
    return jsonify({"error":"Card not found"}),404
@app.delete("/api/cards/<card_id>")
def delete_card(card_id):
    cards=load_cards(); updated=[c for c in cards if c["id"]!=card_id]
    if len(updated)==len(cards): return jsonify({"error":"Card not found"}),404
    save_cards(updated); return jsonify({"ok":True})
@app.get("/api/price-search")
def lookup():
    q=request.args.get("q","").strip()
    if len(q)<2: return jsonify({"results":[],"message":"Enter at least two characters."})
    return jsonify(price_search(q))
@app.get("/<path:path>")
def static_file(path): return send_from_directory("static",path)
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")),debug=os.getenv("FLASK_DEBUG")=="1")
