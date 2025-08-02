from flask import Flask, request, render_template, request
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

app = Flask(__name__)

# list of tracking params:
TRACKING_PARAMS = {
    # UTM & Google
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "fbclid", "yclid", "msclkid", "dclid",
    # Mail
    "mc_eid", "mc_cid", "mkt_tok", "hsa_acc", "hsa_cam", "hsa_grp", "hsa_ad", "hsa_src", "hsa_tgt", "hsa_kw", "hsa_net", "hsa_mt", "hsa_ver",
    # Affiliate/referral
    "aff_id", "affid", "affiliate", "ref", "refid", "partnerid", "partner", "pk_campaign",
    # Analytics
    "ga_campaign", "ga_source", "ga_medium", "s_cid", "wickedid",
    # Social
    "igshid", "twclid", "fb_action_ids", "fb_action_types", "fb_ref", "fb_source",
    # Others
    "spm", "soc_src", "soc_trk", "cmpid", "emci", "emdi",
    "trk", "trkCampaign", "trkContact", "redirect_log_mongo_id", "redirect_mongo_id",
    "redirect", "campaignid", "adgroupid", "adid", "ad_set_id", "ad_set_name", "ad_id", "ad_name", "adgroup_name"
}

def clean_url(input_url):
    # parse uerl into its components
    parsed = urlparse(input_url)
    # parse query string into list of keys and values
    params = parse_qsl(parsed.query, keep_blank_values=True)
    # make a new list excluding tracking params
    cleaned_params = []
    for k, v in params:
        if k not in TRACKING_PARAMS:
            cleaned_params.append((k,v))
    # rebuild the query string from the cleaned list
    cleaned_query = urlencode(cleaned_params)
    # reconstruct the full cleaned url
    cleaned_url = urlunparse(parsed._replace(query=cleaned_query))
    # make a list with the removed params 
    removed = []
    for k, v in params:
        if k in TRACKING_PARAMS:
            removed.append((k,v))
    print(f"parsed = {parsed}")
    print(f"params = {params}")
    print(f"cleaned params = {cleaned_params}")
    print(f"cleaned query = {cleaned_query}")
    print(f"cleaned url = {cleaned_url}")
    print(f"removed trackers = {removed}")
    
    return cleaned_url, removed

@app.route("/", methods=['GET', 'POST'])
def index():
    cleaned = None
    removed = []
    input_url = ''
    error = None
    if request.method == 'POST':
        input_url = request.form.get('url')
        if input_url:
            result, removed = clean_url(input_url)
            if result:
                cleaned = result
            else:
                error = "Invalid URL. Please check and try again"

    return render_template('index.html', cleaned=cleaned, removed=removed, input_url=input_url, error=error)

# Add your link cleaning routes here

if __name__ == "__main__":
    app.run()

