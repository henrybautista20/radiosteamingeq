import subprocess
import asyncio
from datetime import datetime
import asyncio
from datetime import datetime
import time
import os
import pandas as pd
import logging
from datetime import datetime, timedelta, time
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

logging.info("Start app.")
out_dir = os.path.join("audios", "radio_stream")
os.makedirs(out_dir, exist_ok=True)

df = pd.read_csv("audios/Radios.csv")
df["last_read"] = ""
container_name = "azureml"


def check_time(hour):
    h,m = hour.split(":")
    now_minute = datetime.now().minute
    if datetime.now().hour == int(h) and now_minute <= int(m) <= now_minute + 10:
        return True
    
def check_time_finish(hour):
    try:
        h,m = hour.split(":")
        if datetime.now().hour >= int(h) and datetime.now().minute >= int(m):
            return True
    except Exception as e:
        logging.error(f"Error checking time finish: {e}")
    return False

def calculate_difference(data):
    time_format = "%H:%M"

    t1 = datetime.strptime(data["utc"], time_format)
    t2 = datetime.strptime(data["utc_final"], time_format)
    difference = t2 - t1
    return int(difference.total_seconds())   


async def grabar_audio(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = data['nombre_radios']
    lugar = data['lugar']
    output_file = f"{nombre}_{timestamp}.wav"
    out_dir = f"audios/radio_stream/{lugar}"
    os.makedirs(out_dir, exist_ok=True)
    try:
        process = await asyncio.create_subprocess_exec(
        "ffmpeg", "-y",
        "-reconnect", "1",
        "-reconnect_streamed", "1",
        "-reconnect_delay_max", "5",
        "-err_detect","ignore_err",
        "-i",data['stream'],
        "-t", "1800",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-loglevel","verbose",
        f"audios/radio_stream/{lugar}/{output_file}",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
        )
        
        await process.communicate()
        #await upload_file(f"radio_stream/{nombre}",output_file)
        logging.info(f"audios/radio_stream/{lugar}/{output_file} guardado")

    except Exception as e:
        logging.error(f"❌ Error with {nombre}: {e}")

    

        
    
async def main():
    logging.info("Main active. 2")
    today = datetime.now().time()
    logging.info(str(df.columns))
    logging.info(str(today) + 'ok')
    while True:
        today = datetime.now().time()
        start = time(0, 0)    # 05:00 AM
        end = time(23, 59)     # 05:00 PM
        tasks = []
        logging.info(str(today) + 'ok')
        for i,data in df.iterrows():
            if start <= today <= end:
                name = data['nombre_radios']
                logging.warning(f"✅  Starting {name} recording cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                tasks.append(grabar_audio(data))
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        # if you are inside an environment with already running loop (e.g. Jupyter)
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())