import random
import uuid
from datetime import datetime, timedelta

import firebase_admin
from firebase_admin import credentials, firestore, storage

from constant import constant

# Use a service account
cred = credentials.Certificate(
    './local/paeparo-firebase-adminsdk-c05v5-18426933bc.json')  # replace with your serviceAccount.json
firebase_admin.initialize_app(cred, {
    'storageBucket': 'paeparo.appspot.com'  # replace with your app's bucket name
})
db = firestore.client()
bucket = storage.bucket()


def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))


def upload_image_to_firebase(user_id, post_id, image_path):
    blob = bucket.blob(f'images/{user_id}/{post_id}/{uuid.uuid4()}')
    blob.upload_from_filename(image_path)
    blob.make_public()
    return blob.public_url


def generate_trip_and_post(regions, latlong, titles, users, descriptions, tags, sample_images):
    trip = {}
    trip['region'] = random.choice(regions)
    trip['latitude'] = latlong[trip['region']]['lat']
    trip['longitude'] = latlong[trip['region']]['lon']
    trip['transportation'] = random.choice(["자가용", "대중교통"])
    trip['name'] = random.choice(titles[trip['region']])
    trip['status'] = random.choice(["PLANNING", "ONGOING", "FINISHED"])
    start_date = random_date(datetime(2023, 4, 1), datetime(2023, 10, 31))
    end_date = start_date + timedelta(days=random.randint(2, 5))
    trip['start_date'] = start_date
    trip['end_date'] = end_date
    trip['budget'] = random.randint(100000, 3000000)
    trip['members'] = random.sample(users, random.randint(1, 4))
    if trip['status'] == 'PLANNING':
        trip['invitations'] = random.sample([user for user in users if user not in trip['members']],
                                            random.randint(1, 2))
    else:
        trip['invitations'] = []

    trip_ref = db.collection('trips').document()
    trip_ref.set(trip)

    if trip['status'] == 'FINISHED':
        post = {}
        post['trip_id'] = trip_ref.id
        post['user_id'] = trip['members'][0]
        post['region'] = trip['region']
        post['title'] = trip['name']
        post['description'] = random.choice(descriptions[trip['region']])
        post['created_at'] = end_date + timedelta(hours=random.randint(18, 23))
        post['likes'] = random.randint(1, 1000)
        post['tags'] = random.sample(tags, 5)
        post['images'] = [upload_image_to_firebase(post['user_id'], trip_ref.id, img) for img in
                          random.sample(sample_images[trip['region']], 4)]

        post_ref = db.collection('posts').document()
        post_ref.set(post)

        return trip, post

    return trip, None


for _ in range(80):
    trip, post = generate_trip_and_post(constant.regions, constant.latlong, constant.titles, constant.users, constant.descriptions,
                                        constant.tags, constant.images)
    print(trip)
    if post:
        print(post)
