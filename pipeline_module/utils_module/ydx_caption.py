import logging
from collections import deque
from web_server_utils import load_pipeline_progress_from_file, save_pipeline_progress_to_file
from ..generate_YDX_caption_submodule.generate_ydx_caption import GenerateYDXCaption

def run_generate_ydx_caption(video_id, aiUserId,logger = logging.getLogger(__name__)):
    video_runner_obj={
        "video_id": video_id,
        "logger": logger
    }
    generate_YDX_caption = GenerateYDXCaption(video_runner_obj=video_runner_obj)
    save_data = load_pipeline_progress_from_file()
    if save_data is None:
        print("run_generate_ydx_caption :: No data found")
        logging.info("run_generate_ydx_caption :: No data found")
        return
    if video_id not in save_data.keys():
        print("run_generate_ydx_caption :: Video ID not found")
        logging.info("run_generate_ydx_caption :: Video ID not found")
        return
    if aiUserId not in save_data[video_id].keys():
        print("run_generate_ydx_caption :: AI User ID not found")
        logging.info("run_generate_ydx_caption :: AI User ID not found")
        return
    
    save_data[video_id]["status"] = "done"
    save_pipeline_progress_to_file(save_data=save_data)
    
    # Create a copy of the objects list
    objects_list = list(save_data[video_id]["data"][aiUserId])

    for obj in objects_list:
        if(obj["status"] == "done"):
            continue
        
        
        generate_YDX_caption.generateYDXCaption(
            ydx_server=obj.get("ydx_server", None),
            ydx_app_host=obj.get("ydx_app_host", None),
            userId=obj.get("USER_ID", None),
            aiUserId=obj.get("AI_USER_ID", None),
            logger=logger,
        )
        obj["status"] = "done"

        # Update the original data with the modified objects
        save_data[video_id][aiUserId] = objects_list

        # Save the updated data to the file
        save_pipeline_progress_to_file(save_data=save_data)

    save_data[video_id]["data"][aiUserId] = []
    # Finally, save the updated data to the file (this will save the last state of save_data)
    save_pipeline_progress_to_file(save_data=save_data)
        
    return