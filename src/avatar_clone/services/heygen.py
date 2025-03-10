import requests
from avatar_clone.helper.config import HEYGEN_API_KEY, WEBHOOK_ENDPOINT
import time

BASE_URL = "https://api.heygen.com"


class HeygenService:
    def __init__(self):
        self.api_key = HEYGEN_API_KEY
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": self.api_key,
        }

    def make_request(self, method, endpoint, params=None, json_data=None):
        url = f"{BASE_URL}{endpoint}"
        response = requests.request(
            method, url, headers=self.headers, params=params, json=json_data
        )
        response.raise_for_status()
        return response.json()

    def get_avatars(self):
        return self.make_request("GET", "/v2/avatars")["data"]["avatars"]

    def get_video(self, video_id):
        max_retries = 50
        retry_count = 0
        params = {"video_id": video_id}

        while retry_count < max_retries:
            data = self.make_request("GET", "/v1/video_status.get", params=params)

            if data["data"]["status"] == "failed":
                raise ValueError(
                    f"Failed to avatar video generation: {data['data']['error']['detail']}"
                )

            if data["data"]["status"] == "completed":
                return data["data"]

            print("waiting for heygen video creation...")
            time.sleep(45)
            retry_count += 1

        return data["data"]

    def get_videos(self, video_ids):
        return [
            {"download_url": self.get_video(video_id)["video_url"]}
            for video_id in video_ids
        ]

    def create_video_using_audio(self, audio_url, avatar_id):
        payload = {
            "callback_id": avatar_id,
            "dimension": {"width": 1280, "height": 720},
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": avatar_id,
                        "scale": 1.0,
                        "avatar_style": "normal",
                        "offset": {"x": 0.0, "y": 0.0},
                        "matting": True,
                    },
                    "voice": {
                        "type": "audio",
                        "audio_url": audio_url,
                    },
                }
            ],
            "callback_url": WEBHOOK_ENDPOINT,
        }
        return self.make_request("POST", "/v2/video/generate", json_data=payload)[
            "data"
        ]

    def create_video_using_script(self, script, avatar_id, voice_id):
        payload = {
            "callback_id": avatar_id,
            "dimension": {"width": 1280, "height": 720},
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": avatar_id,
                        "scale": 1.0,
                        "avatar_style": "normal",
                        "offset": {"x": 0.0, "y": 0.0},
                        "matting": True,
                    },
                    "voice": {
                        "type": "text",
                        "voice_id": voice_id,
                        "input_text": script,
                        "speed": 1.0,
                        "pitch": 0,
                        "emotion": "Friendly",
                    },
                }
            ],
            "callback_url": WEBHOOK_ENDPOINT,
        }
        return self.make_request("POST", "/v2/video/generate", json_data=payload)[
            "data"
        ]

    def generate_videos(self, audio_urls, replica_id):
        return [
            {
                "video_id": self.create_video_using_audio(audio_url, replica_id)[
                    "video_id"
                ]
            }
            for audio_url in audio_urls
        ]

    def add_webhook(self, entity_id):
        payload = {
            "url": WEBHOOK_ENDPOINT,
            "events": ["avatar_video.success", "avatar_video.fail"],
            "entity_id": entity_id,
        }
        return self.make_request("POST", "/v2/webhook/endpoint.add", json_data=payload)

    def create_video_with_voice(self, title, audio_urls, template, video_type):
        avatar_id = (
            "83e1ce3cdb21477f9fa07df472ba6214"
            if template == "temp3"
            else "4cfeb3afb1a1497e9274b15197796537"
        )
        dimension = (
            {"width": 1080, "height": 1920}
            if video_type == "shorts"
            else {"width": 1920, "height": 1080}
        )
        aspect_ratio = "16:9" if video_type == "shorts" else "9:16"
        video_inputs = [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar_id,
                    "avatar_style": "normal",
                },
                "voice": {"type": "audio", "audio_url": audio_url},
                "background": {
                    "type": "image",
                    "url": "https://resource.heygen.ai/image/9f0038e172e748a183338b33895632bc/original",
                },
            }
            for audio_url in audio_urls
        ]
        payload = {
            "test": False,
            "caption": True,
            "title": title,
            "dimension": dimension,
            "aspect_ratio": aspect_ratio,
            "video_inputs": video_inputs,
        }
        return self.make_request("POST", "/v2/video/generate", json_data=payload)[
            "data"
        ]["video_id"]

    def get_templates(self):
        return self.make_request("GET", "/v2/templates")["data"]["templates"][0][
            "template_id"
        ]

    def upload_asset(self, path, content_type):
        headers = {"Content-Type": content_type, "x-api-key": self.api_key}
        with open(path, "rb") as f:
            response = requests.post(f"{BASE_URL}/v2/asset", data=f, headers=headers)
        response.raise_for_status()
        return response.json()["data"]["id"]

    def create_avatar_video(
        self,
        video_inputs,
        dimension,
        caption=False,
        title=None,
        callback_id=None,
        callback_url=None,
    ):
        payload = {
            "caption": caption,
            "title": title,
            "callback_id": callback_id,
            "video_inputs": video_inputs,
            "dimension": dimension,
            "callback_url": callback_url,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        return self.make_request("POST", "/v2/video/generate", json_data=payload)

    def create_avatar_group(self, name, image_key, generation_id=None):
        payload = {"name": name, "image_key": image_key}
        if generation_id:
            payload["generation_id"] = generation_id
        return self.make_request(
            "POST", "/photo_avatar/avatar_group/create", json_data=payload
        )

    def add_looks_to_group(self, group_id, image_keys, name=None, generation_id=None):
        payload = {"group_id": group_id, "image_keys": image_keys}
        if name:
            payload["name"] = name
        if generation_id:
            payload["generation_id"] = generation_id
        return self.make_request(
            "POST", "/photo_avatar/avatar_group/add", json_data=payload
        )

    def train_avatar_group(self, group_id):
        payload = {"group_id": group_id}
        return self.make_request("POST", "/photo_avatar/train", json_data=payload)

    def get_avatar_details(self, avatar_id):
        return self.make_request("GET", f"/photo_avatar/{avatar_id}")

    def upload_image(self, file_path):
        url = "https://upload.heygen.com/v1/asset"
        with open(file_path, "rb") as file:
            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "image/jpeg",
            }
            response = requests.post(url, headers=headers, data=file)
            return response.json()


# # Example usage
# if __name__ == "__main__":
#     service = HeygenService()

#     video_inputs = [
#         {
#             "character": {
#                 "type": "avatar",
#                 "avatar_id": "Abigail_expressive_2024112501",
#                 "scale": 1.0,
#                 "avatar_style": "normal",
#                 "offset": {"x": 0.0, "y": 0.0},
#                 "matting": True,
#             },
#             "voice": {
#                 "type": "text",
#                 "voice_id": "1985984feded457b9d013b4f6551ac94",
#                 "input_text": """Hey folks! So, uh, what if I told you there’s a new technology out there... that's like, totally shaking up how we deal with wastewater? Yeah, it's called BioeF – and let me tell you, it’s got some real potential to change the game. Now, imagine, this BioeF thing, it’s a type of electroactive biofilter, and it's getting rid of—ready for it?—80% of pharmaceuticals and between 50 to 75% of herbicides. That’s a big deal compared to, like, the old-school gravel filters. Pretty wild right? And then there's chirality... this chemistry thing that’s kinda like, well, your left hand vs. your right hand. They look alike but aren't identical. This is what allows the BioeF to tweak those contaminants and make 'em more breakable, or, uh, biodegradable. Cool, huh? But it doesn’t just clean. It cleans *smart*! BioeF knocks down the dangers of all these industrial and personal care pollutants, uh, even plastics, so our fish friends can swim safe, and, you know, we get healthier water.""",
#                 "speed": 1.0,
#                 "pitch": 0,
#                 "emotion": "Friendly",
#             },
#             "background": {"type": "color", "value": "#f6f6fc"},
#         }
#     ]

#     dimension = {"width": 1280, "height": 720}

#     result = service.create_avatar_video(
#         video_inputs=video_inputs,
#         dimension=dimension,
#         caption=True,
#         title="Test Video",
#         callback_id="custom_callback_id",
#         callback_url="https://your-callback-url.com",
#     )

#     print(result)
