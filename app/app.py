import streamlit as sl
import streamlit.components.v1 as components

import subprocess
import uuid
from pathlib import Path
import time


linkedin_profile_badge = """
<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
<div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="ameur-b-25a155247" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://dz.linkedin.com/in/ameur-b-25a155247?trk=profile-badge">Ameur B.</a></div>
"""

sl.set_page_config(page_title="El Khabar Spider",page_icon="📰")
tab1, tab2 = sl.tabs(["Spider", "Linkedin"])
with tab2:
    components.html(linkedin_profile_badge)

with tab1: 
    sl.title("El Khabar Spider")
    sl.text("This is a web-based spider using python with scrapy to crawl articles from El Khabar newspaper website.")

    if "process" not in sl.session_state:
        sl.session_state.process = None

    if "crawled" not in sl.session_state:
        sl.session_state.crawled = 0


    sl.session_state.file_type = sl.selectbox("Select File type",options=['CSV','JSON','XML'])
    if sl.button("Crawl"):
        if sl.session_state.process == None:
            sl.session_state.file_name = uuid.uuid4()
            command = [
                "scrapy", "crawl", "elkhabar_spider", 
                "-o", f"{sl.session_state.file_name}.{sl.session_state.file_type.lower()}"
            ]
            sl.session_state.process = subprocess.Popen(command)
            sl.success("Crawling Started")
            sl.toast("Dont intrupt it directly to get your data")
            time.sleep(2)
            sl.error("It takes 2 seconds already to start.")
            sl.session_state.crawled = 1

    if sl.button("Stop"):
        if sl.session_state.process is not None:
            sl.session_state.process.terminate()
            sl.session_state.process.wait() 
            sl.session_state.process = None 
            sl.success("Crawling stopped.")
        else:
            sl.warning("No crawling process is running.")

    if sl.session_state.crawled:
        time.sleep(1)
        sl.header("Download your data")
        
        if Path(f"{sl.session_state.file_name}.{sl.session_state.file_type.lower()}").exists():
            with open(f"{sl.session_state.file_name}.{sl.session_state.file_type.lower()}", "rb") as file:
                sl.download_button(
                    label="Download Data", 
                    data=file, 
                    file_name=f"{sl.session_state.file_name}.{sl.session_state.file_type.lower()}", 
                    mime="text/plain"
            )
            Path(f"{sl.session_state.file_name}.{sl.session_state.file_type.lower()}").unlink()
            
                
            sl.session_state.crawled = None
            sl.session_state.file_name = None
            sl.session_state.file_type = None