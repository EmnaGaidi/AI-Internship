import json
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask("VideoAPI")
api = Api(app)

parser = reqparse.RequestParser()
# it has to be a title whenever we make a request with reqparser
parser.add_argument("title", required=True)
parser.add_argument("uploadDate", required=False, type=int)

videos = {
    "video1": {"title": "Hello video", "uploadDate": 20210917},
    "video2": {"title": "why python is the best language", "uploadDate": 20230711},
}

# read from the file
with open("videos.json", "r") as f:
    videos = json.load(f)


def write_changes_to_file():
    global videos
    videos = {
        k: v
        for k, v in sorted(videos.items(), key=lambda video: video[1]["uploadDate"])
    }
    with open("video.json", "w") as f:
        json.dump(videos, f)


# save everything into the file
write_changes_to_file()


class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    def put(self, video_id):
        args = parser.parse_args()
        new_video = {"title": args["title"], "uploadDate": args["uploadDate"]}
        videos[video_id] = new_video
        write_changes_to_file()
        return {video_id, videos[video_id], 201}

    def delete(self, video_id):
        if video_id not in videos:
            abort(404, message=f"video with this video id {video_id} is not found")
        del videos[video_id]
        write_changes_to_file()


class VideoSchedule(Resource):
    def get(self):
        return videos

    def post(self):
        args = parser.parse_args()
        new_video = {"title": args["title"], "uploadDate": args["uploadDate"]}
        video_id = max(int(v.lstrip("video")) for v in videos.keys()) + 1
        video_id = f"video{video_id}"
        videos[video_id] = new_video
        write_changes_to_file()
        return videos[video_id], 201


api.add_resource(Video, "/video/<video_id>")
api.add_resource(VideoSchedule, "/videos")

if __name__ == "__main__":
    app.run()
